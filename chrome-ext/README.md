# LinkedIn Easy Apply Automator

This Chrome extension helps automate the process of applying for jobs on LinkedIn using the "Easy Apply" feature with AI-powered form filling.

## 🚀 Quick Start

### Installation (30 seconds)
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select this folder
5. Click extension icon → Options → Add your resume

### Usage
**Two modes available:**
- **Single Job Mode**: Click "Apply on This Page" when viewing a job
- **Bulk Mode**: Check "Auto Apply" and click "Search Jobs" to process multiple jobs

📖 **[Read QUICK_START.md for detailed instructions](QUICK_START.md)**

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICK_START.md](QUICK_START.md)** | Complete beginner guide with step-by-step instructions |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Solutions for all common errors |
| **[ANALYSIS.md](ANALYSIS.md)** | Technical code analysis and architecture |
| **[VERIFICATION.md](VERIFICATION.md)** | QA report and testing status |

---

## ⚠️ Important Notes

### Security Warning
**CRITICAL**: The API key is currently hardcoded in `background.js` line 4. This is a security risk. Either:
- Move the key to the options page (let users enter their own)
- Use environment variables for private use
- Implement a backend proxy

### LinkedIn Terms of Service
Using automation may violate LinkedIn's Terms of Service. Use at your own risk and responsibly.

---

## ✅ Current Status (v0.013)

- ✅ All critical bugs fixed (6/6)
- ✅ Core functionality complete
- ✅ Form filling supports all input types
- ⚠️ API key security needs attention
- ⏳ Ready for manual testing

---

## 🆘 Getting Help

**Having issues?**
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common errors
2. Open DevTools (F12) and check console logs
3. Make sure you're on a LinkedIn jobs page
4. Reload the page if the extension was just installed

**Most common fixes:**
- Reload the LinkedIn page (F5)
- Make sure you're on `linkedin.com/jobs/view/...`
- Add your resume in extension options
- Check that extension is enabled in `chrome://extensions/`

---

## 🛠️ Development

### Tech Stack
- Chrome Extension Manifest V3
- Vanilla JavaScript
- ZHIPU AI API integration

### Project Structure
```
chrome-ext/
├── manifest.json       # Extension config
├── background.js       # Service worker (job queue, AI calls)
├── content.js         # Content script (DOM interaction)
├── popup.html/js      # Extension popup UI
├── options.html/js    # Resume configuration
└── images/           # Extension icons
```

See [ANALYSIS.md](ANALYSIS.md) for detailed code documentation.

---

*Version: 0.013*  
*Last updated: 2025-11-26*
