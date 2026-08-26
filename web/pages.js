/**
 * PromptKiller — New Pages: Model Arena, HarmBench, Pliny's Arsenal
 */

// ═══════════════════════════════════════════════
// MODEL ARENA
// ═══════════════════════════════════════════════
function renderModelArena() {
    const grid = document.getElementById('modelGrid');
    if (!grid) return;

    grid.innerHTML = Object.entries(MODEL_PROFILES).map(([id, m]) => `
        <div class="model-card" onclick="selectModel('${id}')">
            <div class="model-header">
                <span class="model-icon">${m.icon}</span>
                <div>
                    <div class="model-name">${m.name}</div>
                    <div class="model-org">${m.org} • ${m.params}</div>
                </div>
                <span class="model-safety-badge ${m.safety_level}">${m.safety_level}</span>
            </div>
            <div class="model-bars">
                <div class="model-bar-row">
                    <span>Jailbreak</span>
                    <div class="model-bar"><div class="model-bar-fill" style="width:${m.jailbreak_resistance*100}%;background:${getResistanceColor(m.jailbreak_resistance)}"></div></div>
                    <span>${(m.jailbreak_resistance*100).toFixed(0)}%</span>
                </div>
                <div class="model-bar-row">
                    <span>Injection</span>
                    <div class="model-bar"><div class="model-bar-fill" style="width:${m.prompt_injection_resistance*100}%;background:${getResistanceColor(m.prompt_injection_resistance)}"></div></div>
                    <span>${(m.prompt_injection_resistance*100).toFixed(0)}%</span>
                </div>
                <div class="model-bar-row">
                    <span>Roleplay</span>
                    <div class="model-bar"><div class="model-bar-fill" style="width:${m.roleplay_resistance*100}%;background:${getResistanceColor(m.roleplay_resistance)}"></div></div>
                    <span>${(m.roleplay_resistance*100).toFixed(0)}%</span>
                </div>
                <div class="model-bar-row">
                    <span>Encoding</span>
                    <div class="model-bar"><div class="model-bar-fill" style="width:${m.encoding_resistance*100}%;background:${getResistanceColor(m.encoding_resistance)}"></div></div>
                    <span>${(m.encoding_resistance*100).toFixed(0)}%</span>
                </div>
                <div class="model-bar-row">
                    <span>Manipulation</span>
                    <div class="model-bar"><div class="model-bar-fill" style="width:${m.manipulation_resistance*100}%;background:${getResistanceColor(m.manipulation_resistance)}"></div></div>
                    <span>${(m.manipulation_resistance*100).toFixed(0)}%</span>
                </div>
            </div>
            <div class="model-footer">
                <span class="model-safety-score">Overall: ${(m.safety_score*100).toFixed(0)}%</span>
                <span class="model-license">${m.license}</span>
            </div>
        </div>
    `).join('');
}

function getResistanceColor(val) {
    if (val >= 0.7) return '#22c55e';
    if (val >= 0.5) return '#eab308';
    if (val >= 0.3) return '#f97316';
    return '#ef4444';
}

let selectedModel = null;
let selectedTechniques = [];

function selectModel(id) {
    selectedModel = id;
    document.querySelectorAll('.model-card').forEach(c => c.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
    updateSimulationPanel();
}

function toggleTechnique(id) {
    const idx = selectedTechniques.indexOf(id);
    if (idx > -1) selectedTechniques.splice(idx, 1);
    else selectedTechniques.push(id);
    updateSimulationPanel();
}

function updateSimulationPanel() {
    const panel = document.getElementById('simulationPanel');
    if (!panel || !selectedModel) return;

    const model = MODEL_PROFILES[selectedModel];
    const allTech = getAllTechniques();

    panel.innerHTML = `
        <h3>🧪 Simulation: ${model.icon} ${model.name}</h3>
        <p style="color:var(--text-secondary);margin-bottom:16px">Select attack techniques and run simulation against ${model.name}</p>
        <div class="tech-grid">
            ${allTech.map(t => `
                <div class="tech-item ${selectedTechniques.includes(t.id) ? 'selected' : ''}" onclick="toggleTechnique('${t.id}')">
                    <span class="tech-sev ${t.severity}">${t.severity}</span>
                    <span class="tech-name">${t.name}</span>
                    <span class="tech-type">${t.type}</span>
                </div>
            `).join('')}
        </div>
        <button class="btn btn-primary" style="margin-top:16px" onclick="runSimulation()">
            🚀 Run Simulation (${selectedTechniques.length} techniques × 20 iterations)
        </button>
        <div id="simulationResults"></div>
    `;
}

function runSimulation() {
    if (!selectedModel || selectedTechniques.length === 0) return;

    const results = runBatchSimulation([selectedModel], selectedTechniques, 20);
    const container = document.getElementById('simulationResults');

    const sorted = results.sort((a, b) => b.success_rate - a.success_rate);
    const avgSuccess = sorted.reduce((s, r) => s + parseFloat(r.success_rate), 0) / sorted.length;

    container.innerHTML = `
        <div class="sim-summary">
            <div class="sim-stat"><span class="sim-stat-val" style="color:${avgSuccess > 50 ? '#ef4444' : '#22c55e'}">${avgSuccess.toFixed(1)}%</span><span>Avg Success Rate</span></div>
            <div class="sim-stat"><span class="sim-stat-val">${sorted.filter(r => parseFloat(r.success_rate) > 50).length}</span><span>High-Risk Attacks</span></div>
            <div class="sim-stat"><span class="sim-stat-val">${sorted.filter(r => parseFloat(r.success_rate) <= 30).length}</span><span>Blocked Attacks</span></div>
        </div>
        <div class="sim-table">
            <table class="threat-table">
                <thead><tr><th>Technique</th><th>Type</th><th>Success Rate</th><th>Result</th></tr></thead>
                <tbody>
                    ${sorted.map(r => `
                        <tr>
                            <td><strong>${r.technique}</strong></td>
                            <td><span class="tag tag-technique">${r.attack_type}</span></td>
                            <td>
                                <div class="effectiveness-bar"><div class="effectiveness-bar-fill" style="width:${r.success_rate}%;background:${parseFloat(r.success_rate) > 50 ? '#ef4444' : parseFloat(r.success_rate) > 30 ? '#f97316' : '#22c55e'}"></div></div>
                                ${r.success_rate}%
                            </td>
                            <td>${parseFloat(r.success_rate) > 50 ? '🔴 VULNERABLE' : parseFloat(r.success_rate) > 30 ? '🟠 WEAK' : '🟢 RESISTANT'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

// ═══════════════════════════════════════════════
// HARMBENCH
// ═══════════════════════════════════════════════
function renderHarmBench() {
    // Category stats
    const catContainer = document.getElementById('harmbenchCategories');
    if (catContainer) {
        catContainer.innerHTML = Object.entries(HARMBENCH_CATEGORIES).map(([id, cat]) => `
            <div class="hb-cat-card">
                <span class="hb-cat-icon">${cat.icon}</span>
                <div class="hb-cat-name">${cat.name}</div>
                <div class="hb-cat-count">${cat.behaviors} behaviors</div>
                <div class="hb-cat-desc">${cat.description}</div>
            </div>
        `).join('');
    }

    // Model comparison table
    const tableBody = document.querySelector('#harmbenchTable tbody');
    if (tableBody) {
        const sorted = Object.entries(HARMBENCH_RESULTS)
            .sort((a, b) => a[1].overall_attack_success_rate - b[1].overall_attack_success_rate);

        tableBody.innerHTML = sorted.map(([modelId, data]) => {
            const model = MODEL_PROFILES[modelId];
            if (!model) return '';
            const asr = (data.overall_attack_success_rate * 100).toFixed(1);
            const defense = (data.defense_rate * 100).toFixed(1);
            return `
                <tr>
                    <td>${model.icon} <strong>${model.name}</strong></td>
                    <td>${model.params}</td>
                    <td style="color:${parseFloat(asr) > 50 ? '#ef4444' : parseFloat(asr) > 35 ? '#f97316' : '#22c55e'}">${asr}%</td>
                    <td style="color:${parseFloat(defense) > 60 ? '#22c55e' : parseFloat(defense) > 45 ? '#eab308' : '#ef4444'}">${defense}%</td>
                    <td>${data.false_refusal_rate ? (data.false_refusal_rate * 100).toFixed(1) + '%' : 'N/A'}</td>
                    <td>${data.total_behaviors}</td>
                </tr>
            `;
        }).join('');
    }

    // Per-category breakdown
    const breakdownContainer = document.getElementById('harmbenchBreakdown');
    if (breakdownContainer) {
        const models = Object.keys(MODEL_PROFILES);
        breakdownContainer.innerHTML = `
            <table class="threat-table">
                <thead>
                    <tr>
                        <th>Category</th>
                        ${models.map(id => `<th>${MODEL_PROFILES[id]?.icon || ''} ${MODEL_PROFILES[id]?.name?.split(' ')[0] || id}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    ${Object.entries(HARMBENCH_CATEGORIES).map(([catId, cat]) => `
                        <tr>
                            <td>${cat.icon} ${cat.name}</td>
                            ${models.map(id => {
                                const rate = HARMBENCH_RESULTS[id]?.category_rates?.[catId] || 0;
                                const pct = (rate * 100).toFixed(0);
                                return `<td style="color:${parseFloat(pct) > 50 ? '#ef4444' : parseFloat(pct) > 35 ? '#f97316' : '#22c55e'}">${pct}%</td>`;
                            }).join('')}
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }
}

// ═══════════════════════════════════════════════
// PLINY'S ARSENAL
// ═══════════════════════════════════════════════
function renderPlinyArsenal() {
    const container = document.getElementById('plinyArsenal');
    if (!container) return;

    container.innerHTML = Object.entries(PLINY_ARSENAL).map(([arsenalId, arsenal]) => `
        <div class="arsenal-section">
            <div class="arsenal-header">
                <div>
                    <h3 class="arsenal-name">${arsenal.name}</h3>
                    <div class="arsenal-meta">
                        <a href="https://github.com/${arsenal.repo}" target="_blank" class="arsenal-link">📦 GitHub</a>
                        <span class="arsenal-stars">⭐ ${arsenal.stars}</span>
                    </div>
                </div>
                <p class="arsenal-desc">${arsenal.description}</p>
            </div>
            <div class="arsenal-techniques">
                ${arsenal.techniques.map(t => `
                    <div class="arsenal-tech-card ${t.severity}">
                        <div class="arsenal-tech-header">
                            <span class="tech-sev ${t.severity}">${t.severity}</span>
                            <span class="arsenal-tech-id">${t.id}</span>
                            <span class="tag tag-technique">${t.type}</span>
                            <span class="arsenal-eff">Effectiveness: ${(t.effectiveness*100).toFixed(0)}%</span>
                        </div>
                        <h4 class="arsenal-tech-name">${t.name}</h4>
                        <p class="arsenal-tech-desc">${t.description}</p>
                        <div class="arsenal-tech-pattern">
                            <code>${escapeHtml(t.pattern)}</code>
                        </div>
                        <div class="arsenal-tech-meta">
                            <div>
                                <strong>Vulnerable Models:</strong>
                                ${t.models_vulnerable.map(id => `<span class="tag tag-sm">${MODEL_PROFILES[id]?.icon || ''} ${MODEL_PROFILES[id]?.name?.split(' ')[0] || id}</span>`).join(' ')}
                            </div>
                            <div>
                                <strong>Defense:</strong> <span style="color:var(--text-secondary)">${t.defense}</span>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');

    // Profile card
    const profileContainer = document.getElementById('plinyProfile');
    if (profileContainer) {
        profileContainer.innerHTML = `
            <div class="pliny-profile">
                <div class="pliny-avatar">🧙‍♂️</div>
                <div class="pliny-info">
                    <h2>Pliny the Prompter</h2>
                    <div class="pliny-handle">@elder_plinius</div>
                    <p class="pliny-bio">"latent space liberator; prompter, red teamer, hacker, builder, whisperer"</p>
                    <div class="pliny-stats">
                        <div class="pliny-stat"><span>20.8k</span> followers</div>
                        <div class="pliny-stat"><span>47.1k</span> ⭐ CL4R1T4S</div>
                        <div class="pliny-stat"><span>21.2k</span> ⭐ L1B3RT4S</div>
                        <div class="pliny-stat"><span>10.8k</span> ⭐ G0DM0D3</div>
                        <div class="pliny-stat"><span>8k</span> ⭐ OBLITERATUS</div>
                        <div class="pliny-stat"><span>5.7k</span> ⭐ T3MP3ST</div>
                    </div>
                </div>
            </div>
        `;
    }
}
