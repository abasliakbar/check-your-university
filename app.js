const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

const graduation = $('#graduation');
const block = $('#block');
const validation = $('#validation-message');
const eligibleOnly = $('#eligible-only');
const searchInput = $('#search');
const uniFilter = $('#university-filter');
const tableBody = $('#table-body');
const emptyState = $('#empty-state');
const tableWrap = $('.table-wrap');
const groupTabs = $$('.group-tab');

let currentGroup = 1;
let currentTotal = null;
let currentGroupData = null;
let allPrograms = [];

// Folding map for Azerbaijani search
const azMap = { 'ə': 'e', 'ı': 'i', 'ö': 'o', 'ü': 'u', 'ş': 's', 'ç': 'c', 'ğ': 'g' };
const normalizeText = (text) => {
    if (!text) return '';
    let lower = text.toLocaleLowerCase('az-AZ');
    return lower.replace(/[əıöüşçğ]/g, match => azMap[match]);
};

// Fetch data for a given group
async function loadGroup(groupId) {
    try {
        const res = await fetch(`data/groups/group-${groupId}.json`);
        currentGroupData = await res.json();
        
        // Flatten programs for easier filtering, add university reference
        allPrograms = [];
        uniFilter.innerHTML = '<option value="">Bütün universitetlər</option>';
        
        currentGroupData.universities.forEach(u => {
            uniFilter.add(new Option(u.name, u.name));
            u.programs.forEach(p => {
                allPrograms.push({
                    ...p,
                    university: u.name,
                    searchKey: normalizeText(`${p.programName} ${u.name} ${p.branch || ''} ${p.languageOfInstruction || ''}`)
                });
            });
        });
        
        render();
    } catch (e) {
        console.error("Failed to load group data", e);
        tableBody.innerHTML = `<tr><td colspan="6" class="error-cell">Məlumat yüklənərkən xəta baş verdi.</td></tr>`;
    }
}

function clamp(input, max) {
    let n = Number(input.value);
    let msg = '';
    if (!input.value.trim()) return { value: 0, msg };
    if (n < 0) { n = 0; msg = 'Bal 0-dan aşağı ola bilməz.'; }
    if (n > max) { n = max; msg = `Bu sahədə maksimum ${max} bal qəbul edilir.`; }
    input.value = n;
    input.setAttribute('aria-invalid', !!msg);
    return { value: n, msg };
}

function formatScore(score) {
    return score == null ? '—' : score.toLocaleString('az-AZ', { minimumFractionDigits: 1 });
}

function render() {
    if (!currentGroupData) return;

    const term = normalizeText(searchInput.value);
    const uni = uniFilter.value;
    const showEligible = eligibleOnly.checked;

    // Group filtered results by university to render headers
    const resultsByUni = new Map();
    let resultCount = 0;

    allPrograms.forEach(p => {
        if (uni && p.university !== uni) return;
        if (term && !p.searchKey.includes(term)) return;
        if (showEligible && (currentTotal == null || p.currentScore == null || currentTotal < p.currentScore)) return;

        if (!resultsByUni.has(p.university)) {
            resultsByUni.set(p.university, []);
        }
        resultsByUni.get(p.university).push(p);
        resultCount++;
    });

    tableWrap.hidden = resultCount === 0;
    emptyState.hidden = resultCount > 0;

    if (resultCount === 0) {
        tableBody.innerHTML = '';
        return;
    }

    let html = '';
    let rowIndex = 0;

    for (const [uniName, programs] of resultsByUni.entries()) {
        // Render University Header (sticky section header on mobile, section row on desktop)
        html += `<tr class="uni-header"><td colspan="6"><div class="uni-header-inner"><span class="uni-name">${uniName}</span><span class="uni-count">${programs.length} ixtisas</span></div></td></tr>`;

        // Render Programs
        programs.forEach(p => {
            const ok = currentTotal !== null && p.currentScore !== null && currentTotal >= p.currentScore;
            const eligibleBadge = ok ? '<span class="badge badge-eligible">✓ Keçirsiniz</span>' : '';
            const aptitudeBadge = p.requiresAptitudeExam ? '<span class="badge badge-aptitude">Qabiliyyət</span>' : '';
            const branchNote = p.branch ? `<span class="branch-name">(${p.branch})</span>` : '';
            const rowClass = `${ok ? 'eligible' : ''} ${p.isSubBachelor ? 'sub-bachelor' : ''}`.trim();

            const lang = p.languageOfInstruction ? p.languageOfInstruction : 'Azərbaycan';

            html += `<tr class="program-row ${rowClass}" style="--row-index: ${rowIndex + 1}">
                <td class="col-specialty">
                    <div class="specialty-head">
                        <span class="specialty-name">${p.programName}</span>${branchNote}${aptitudeBadge}${eligibleBadge}
                    </div>
                    <div class="mobile-meta">
                        <span class="meta-tag">${p.studyForm}</span>
                        <span class="meta-tag">${lang}</span>
                        ${p.isSubBachelor ? '<span class="meta-tag meta-sub">Subbakalavr</span>' : ''}
                        <span class="mobile-score-prev">2025: <span class="mono">${formatScore(p.previousScore)}</span></span>
                    </div>
                </td>
                <td class="col-form" data-label="Forma"><span class="pill">${p.studyForm}</span></td>
                <td class="col-lang" data-label="Dil"><span class="pill">${lang}</span></td>
                <td class="col-score-2026" data-label="Keçid balı (2026)">
                    <span class="score-2026-val mono">${formatScore(p.currentScore)}</span>
                    <span class="mobile-score-label">2026</span>
                </td>
                <td class="col-score-2025" data-label="Keçid balı (2025)"><span class="mono">${formatScore(p.previousScore)}</span></td>
                <td class="col-note" data-label="Qeyd"><span class="mono">${p.isSubBachelor ? 'Subbakalavr' : '—'}</span></td>
            </tr>`;
            rowIndex++;
        });
    }

    tableBody.innerHTML = html;
}

// Event Listeners
graduation.oninput = () => validation.textContent = clamp(graduation, 300).msg;
block.oninput = () => validation.textContent = clamp(block, 400).msg;

$('#calculate').onclick = () => {
    let a = clamp(graduation, 300);
    let b = clamp(block, 400);
    if (!graduation.value || !block.value || a.msg || b.msg) {
        validation.textContent = a.msg || b.msg || 'Hər iki balı daxil edin.';
        return;
    }
    currentTotal = a.value + b.value;
    $('#score-total').textContent = currentTotal;
    $('#gauge-fill').style.strokeDashoffset = 283 * (1 - currentTotal / 700);
    $('#score-caption').textContent = 'Nəticənə uyğun seçimləri araşdır.';
    eligibleOnly.disabled = false;

    // Add pulse animation to result panel
    const resultPanel = $('.result-panel');
    resultPanel.classList.add('pulse-animate');
    setTimeout(() => {
        resultPanel.classList.remove('pulse-animate');
    }, 200);

    render();
};

[uniFilter, searchInput, eligibleOnly].forEach(el => el.oninput = render);

groupTabs.forEach(tab => {
    tab.onclick = () => {
        groupTabs.forEach(t => {
            t.classList.remove('active');
            t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');
        
        currentGroup = tab.dataset.group;
        loadGroup(currentGroup);
    };
});

// Initial load
loadGroup(currentGroup);
