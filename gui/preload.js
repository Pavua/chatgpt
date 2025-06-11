const { contextBridge } = require('electron');

async function apiRequest(path, options) {
  const url = `http://localhost:8080${path}`;
  const resp = await fetch(url, options);
  if (resp.headers.get('content-type')?.includes('application/json')) {
    return resp.json();
  }
  return resp.text();
}

contextBridge.exposeInMainWorld('userbot', {
  status: () => apiRequest('/status'),
  options: () => apiRequest('/options'),
  switchModel: (name) => apiRequest('/model', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  }),
  switchStyle: (name) => apiRequest('/style', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  }),
  getPrompt: () => apiRequest('/prompt'),
  setPrompt: (text) => apiRequest('/prompt', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  }),
  history: (limit) => apiRequest(`/history?limit=${limit ?? 10}`),
  getAccess: () => apiRequest('/access'),
  setAccess: (data) => apiRequest('/access', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
});
