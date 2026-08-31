import os
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URLS = [
    (1, "https://qebulol.az/1-ci-qrup-kecid-ballari-2026/"),
    (2, "https://qebulol.az/2-ci-qrup-kecid-ballari-2026/"),
    (3, "https://qebulol.az/3-cu-qrup-kecid-ballari-2026/"),
    (4, "https://qebulol.az/4-cu-qrup-kecid-ballari-2026/"),
    (5, "https://qebulol.az/5-ci-qrup-kecid-ballari-2026/")
]

def parse_score(val):
    if val in ('-', '–', ''):
        return None
    try:
        return float(val)
    except:
        return None

def extract_properties(name):
    props = {
        'requiresAptitudeExam': False,
        'languageOfInstruction': 'Azərbaycan',
        'branch': None
    }
    if '@' in name or '♦' in name:
        props['requiresAptitudeExam'] = True

    # Branch
    branch_match = re.search(r'\(([^)]+ filialı|Gəncə şəhəri)\)', name)
    if branch_match:
        props['branch'] = branch_match.group(1)
        name = name[:branch_match.start()] + name[branch_match.end():]

    # Language
    lang_match = re.search(r'\(tədris ([^ ]+) dilində\)', name)
    if lang_match:
        lang_str = lang_match.group(1).lower()
        if 'ingilis' in lang_str:
            props['languageOfInstruction'] = 'İngilis'
        elif 'türk' in lang_str:
            props['languageOfInstruction'] = 'Türk'
        elif 'rus' in lang_str:
            props['languageOfInstruction'] = 'Rus'
        elif 'alman' in lang_str:
            props['languageOfInstruction'] = 'Alman'
        name = name[:lang_match.start()] + name[lang_match.end():]

    name = re.sub(r'\s+', ' ', name)
    name = name.replace('()', '').strip()
    return name, props

def scrape_group(group_id, url):
    print(f"Scraping Group {group_id}...")
    # Add a simple user-agent to avoid blocking
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    content = soup.find(class_='entry-content')

    universities = []
    current_uni = None
    current_program = None

    lines = []
    for el in content.find_all(['p', 'h2', 'h3', 'h4']):
        text = el.get_text(separator='\n').strip()
        if text:
            lines.extend([l.strip() for l in text.split('\n') if l.strip()])

    score_pattern = re.compile(r'(?:^|\s)(?P<form>Ə|Q)\s*(?P<score1>\d+(?:\.\d+)?|-|–)\s*\(\s*(?P<score2>\d+(?:\.\d+)?|-|–)\s*\)')

    for line in lines:
        if not line or line in ('[konkurs]', 'Reklam', '______________________________'):
            continue
        if line.startswith('Reklam'):
            continue

        m = score_pattern.search(line)
        if m:
            form_str = m.group('form')
            score1 = parse_score(m.group('score1'))
            score2 = parse_score(m.group('score2'))
            
            # The remaining is the name
            raw_name = line[:m.start()] + line[m.end():]
            raw_name = re.sub(r'\s+', ' ', raw_name).strip()

            is_sub = False
            if raw_name.lower().startswith('subbakalavrlar'):
                is_sub = True
            
            if is_sub:
                if current_program and current_uni:
                    sub_prog = current_program.copy()
                    sub_prog['currentScore'] = score1
                    sub_prog['previousScore'] = score2
                    sub_prog['isSubBachelor'] = True
                    current_uni['programs'].append(sub_prog)
            else:
                # New program
                name, props = extract_properties(raw_name)
                
                # clean final name
                name_clean = name.replace('▶', '').replace('@', '').replace('♦', '').strip()
                name_clean = re.sub(r'^I?\d+\s+', '', name_clean)
                name_clean = name_clean.replace('Maşm', 'Maşın').strip()
                
                prog = {
                    'programName': name_clean,
                    'studyForm': 'Əyani' if form_str == 'Ə' else 'Qiyabi',
                    'requiresAptitudeExam': props['requiresAptitudeExam'],
                    'currentScore': score1,
                    'previousScore': score2,
                    'isSubBachelor': False
                }
                if props['languageOfInstruction'] != 'Azərbaycan':
                    prog['languageOfInstruction'] = props['languageOfInstruction']
                if props['branch']:
                    prog['branch'] = props['branch']
                
                if current_uni:
                    current_uni['programs'].append(prog)
                current_program = prog

        else:
            # No score pattern
            # Check if it's a new university
            is_university = any(kw in line for kw in ['Universitet', 'Akademiya', 'Məktəb', 'İnstitut', 'Kolleci'])
            
            if is_university or (not current_uni):
                # New university
                name = line.strip()
                if current_uni and current_uni['name'] == name:
                    pass
                else:
                    current_uni = {'name': name, 'programs': []}
                    universities.append(current_uni)
                    current_program = None
            else:
                # Continuation line
                if current_program:
                    append_text = line.strip()
                    full_raw_name = current_program['programName'] + ' ' + append_text
                    
                    new_name, new_props = extract_properties(full_raw_name)
                    
                    name_clean = new_name.replace('▶', '').replace('@', '').replace('♦', '').strip()
                    name_clean = re.sub(r'^I?\d+\s+', '', name_clean)
                    name_clean = name_clean.replace('Maşm', 'Maşın').strip()
                    
                    current_program['programName'] = name_clean
                    
                    if new_props['languageOfInstruction'] != 'Azərbaycan':
                        current_program['languageOfInstruction'] = new_props['languageOfInstruction']
                    if new_props['branch']:
                        current_program['branch'] = new_props['branch']
                    if new_props['requiresAptitudeExam']:
                        current_program['requiresAptitudeExam'] = True
                elif current_uni:
                    current_uni['name'] += ' ' + line.strip()

    # Clean up empty universities
    universities = [u for u in universities if len(u['programs']) > 0]

    return {
        'id': group_id,
        'label': f"{group_id}-ci qrup",
        'year': 2026,
        'sourceUrl': url,
        'scrapedAt': datetime.utcnow().isoformat() + 'Z',
        'universities': universities
    }

if __name__ == "__main__":
    os.makedirs("../data/groups", exist_ok=True)
    for gid, url in URLS:
        data = scrape_group(gid, url)
        out_path = f"../data/groups/group-{gid}.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved Group {gid} with {len(data['universities'])} universities and {sum(len(u['programs']) for u in data['universities'])} programs to {out_path}")
