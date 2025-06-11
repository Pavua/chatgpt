document.addEventListener('DOMContentLoaded', async () => {
  const modelSelect = document.getElementById('modelSelect');
  const styleSelect = document.getElementById('styleSelect');
  const promptArea = document.getElementById('prompt');
  const historyList = document.getElementById('history');
  const wlArea = document.getElementById('whitelist');
  const blArea = document.getElementById('blacklist');
  const exportBtn = document.getElementById('exportDataset');
  let historyData = [];

  const options = await window.userbot.options();
  for (const m of options.models) {
    const opt = document.createElement('option');
    opt.value = m; opt.textContent = m;
    modelSelect.appendChild(opt);
  }
  for (const s of options.styles) {
    const opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    styleSelect.appendChild(opt);
  }

  const status = await window.userbot.status();
  modelSelect.value = status.model;
  styleSelect.value = status.style;
  promptArea.value = await window.userbot.getPrompt();
  const access = await window.userbot.getAccess();
  wlArea.value = (access.whitelist || []).join('\n');
  blArea.value = (access.blacklist || []).join('\n');

  refreshHistory();

  modelSelect.onchange = () => window.userbot.switchModel(modelSelect.value);
  styleSelect.onchange = () => window.userbot.switchStyle(styleSelect.value);
  document.getElementById('savePrompt').onclick = () => {
    window.userbot.setPrompt(promptArea.value);
  };
  document.getElementById('reloadBtn').onclick = refreshHistory;
  document.getElementById('themeBtn').onclick = toggleTheme;
  document.getElementById('saveAccess').onclick = saveAccess;
  exportBtn.onclick = exportDataset;

  async function refreshHistory() {
    historyData = await window.userbot.history(20);
    historyList.innerHTML = '';
    historyData.forEach((entry, idx) => {
      const li = document.createElement('li');
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = true;
      cb.dataset.idx = idx;
      li.appendChild(cb);
      li.appendChild(document.createTextNode(` ${entry.user_id}: ${entry.message} -> ${entry.response}`));
      historyList.appendChild(li);
    });
  }

  async function exportDataset() {
    const selected = [];
    historyList.querySelectorAll('input[type=checkbox]').forEach(cb => {
      if (cb.checked) selected.push(historyData[cb.dataset.idx]);
    });
    const dataset = selected.map(e => ({ prompt: e.message, completion: e.response }));
    await window.userbot.saveFile('dataset.json', JSON.stringify(dataset, null, 2));
  }

  function toggleTheme() {
    const body = document.body;
    const current = body.getAttribute('data-theme');
    body.setAttribute('data-theme', current === 'light' ? 'dark' : 'light');
  }

  function saveAccess() {
    const wl = wlArea.value.split(/\s+/).filter(Boolean).map(Number);
    const bl = blArea.value.split(/\s+/).filter(Boolean).map(Number);
    window.userbot.setAccess({ whitelist: wl, blacklist: bl });
  }
});
