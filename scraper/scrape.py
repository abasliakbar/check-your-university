import json
import os
import re
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

URLS = [
    (1, "https://qebulol.az/1-ci-qrup-kecid-ballari-2027/"),
    (2, "https://qebulol.az/2-ci-qrup-kecid-ballari-2027/"),
    (3, "https://qebulol.az/3-cu-qrup-kecid-ballari-2027/"),
    (4, "https://qebulol.az/4-cu-qrup-kecid-ballari-2027/"),
    (5, "https://qebulol.az/5-ci-qrup-kecid-ballari-2027/")
]


def parse_score(value):
    if value in ('-', '–', '—', ''):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def extract_properties(name):
    requires_aptitude_exam = bool(re.search(r'Qabiliyyət imtahanı', name, re.IGNORECASE))
    props = {
        'requiresAptitudeExam': requires_aptitude_exam or '@' in name or '♦' in name,
        'languageOfInstruction': 'Azərbaycan',
        'branch': None
    }

    branch_match = re.search(r'\(([^)]+ filialı|Gəncə şəhəri)\)', name)
    if branch_match:
        props['branch'] = branch_match.group(1)
        name = name[:branch_match.start()] + name[branch_match.end():]

    language_match = re.search(r'\b(İngilis|Türk|Rus|Alman) dilində\b', name, re.IGNORECASE)
    if language_match:
        props['languageOfInstruction'] = language_match.group(1).capitalize()
        name = name[:language_match.start()] + name[language_match.end():]

    name = re.sub(r'\s*Qabiliyyət imtahanı\s*', ' ', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name)
    name = name.replace('()', '').strip()
    return name, props


def get_cell_text(cell):
    own_content = ''.join(
        str(child) for child in cell.contents
        if getattr(child, 'name', None) != 'td'
    )
    return BeautifulSoup(own_content, 'html.parser').get_text(' ', strip=True)


def scrape_group(group_id, url):
    print(f"Scraping Group {group_id}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find(class_='entry-content')
    if content is None:
        raise ValueError(f"Could not find article content at {url}")

    universities = []
    for table in content.find_all('table'):
        header = table.find('thead')
        if header is None:
            continue

        headers = [cell.get_text(' ', strip=True).lower() for cell in header.find_all(['th', 'td'])]
        if len(headers) < 4 or 'xtisas' not in headers[0] or 'ödənişli' not in headers[2]:
            continue

        heading = table.find_previous(['h2', 'h3', 'h4'])
        if heading is None:
            continue

        university = {'name': heading.get_text(' ', strip=True), 'programs': []}
        body = table.find('tbody')
        for row in body.find_all('tr') if body else []:
            cells = row.find_all('td')
            if len(cells) < 4:
                continue

            raw_name, study_form, paid_score, funded_score = [
                get_cell_text(cell) for cell in cells[:4]
            ]
            if not raw_name:
                continue

            program_name, props = extract_properties(raw_name)
            program_name = program_name.replace('▶', '').replace('@', '').replace('♦', '').strip()
            program = {
                'programName': program_name,
                'studyForm': study_form,
                'requiresAptitudeExam': props['requiresAptitudeExam'],
                'paidScore': parse_score(paid_score),
                'fundedScore': parse_score(funded_score),
                'isSubBachelor': raw_name.lower().startswith('subbakalavrlar')
            }
            if props['languageOfInstruction'] != 'Azərbaycan':
                program['languageOfInstruction'] = props['languageOfInstruction']
            if props['branch']:
                program['branch'] = props['branch']

            university['programs'].append(program)

        if university['programs']:
            universities.append(university)

    program_count = sum(len(university['programs']) for university in universities)
    if not program_count:
        raise ValueError(f"No program rows found at {url}; refusing to save empty data")

    return {
        'id': group_id,
        'label': f"{group_id}-ci qrup",
        'year': 2027,
        'sourceUrl': url,
        'scrapedAt': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'universities': universities
    }


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'groups')
    os.makedirs(output_dir, exist_ok=True)
    for group_id, url in URLS:
        data = scrape_group(group_id, url)
        output_path = os.path.join(output_dir, f"group-{group_id}.json")
        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=2)
        program_count = sum(len(university['programs']) for university in data['universities'])
        print(
            f"Saved Group {group_id} with {len(data['universities'])} universities "
            f"and {program_count} programs to {output_path}"
        )
