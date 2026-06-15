const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1400,
    minHeight: 900,
    frame: true,
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#0d1550',
      symbolColor: '#f5d252',
      height: 36
    },
    title: 'Camp Koronis Jeopardy!',
    webPreferences: {
      contextIsolation: false,
      nodeIntegration: true
    },
    backgroundColor: '#0d2b1a',
    show: false
  });

  win.loadFile(path.join(__dirname, 'index.html'));

  win.once('ready-to-show', () => {
    win.maximize();
    win.show();
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
