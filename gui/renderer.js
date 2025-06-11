document.addEventListener('DOMContentLoaded', async () => {
  const modelSelect = document.getElementById('modelSelect');
  const styleSelect = document.getElementById('styleSelect');
  const promptArea = document.getElementById('prompt');
  const historyList = document.getElementById('history');

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

  refreshHistory();

  modelSelect.onchange = () => window.userbot.switchModel(modelSelect.value);
  styleSelect.onchange = () => window.userbot.switchStyle(styleSelect.value);
  document.getElementById('savePrompt').onclick = () => {
    window.userbot.setPrompt(promptArea.value);
  };
  document.getElementById('reloadBtn').onclick = refreshHistory;
  document.getElementById('themeBtn').onclick = toggleTheme;

  async function refreshHistory() {
    const hist = await window.userbot.history(10);
    historyList.innerHTML = '';
    hist.forEach(entry => {
      const li = document.createElement('li');
      li.textContent = `${entry.user_id}: ${entry.message} -> ${entry.response}`;
      historyList.appendChild(li);
    });
  }

  function toggleTheme() {
    const body = document.body;
    const current = body.getAttribute('data-theme');
    body.setAttribute('data-theme', current === 'light' ? 'dark' : 'light');
  }
});
