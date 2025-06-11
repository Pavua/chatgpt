const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  ipcMain.handle('save-file', async (event, { defaultName, data }) => {
    const { filePath } = await dialog.showSaveDialog({ defaultPath: defaultName });
    if (filePath) {
      fs.writeFileSync(filePath, data);
      return filePath;
    }
    return null;
  });
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
