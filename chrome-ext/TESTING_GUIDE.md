# LinkedIn Easy Apply Automator - Testing Guide

## 🧪 **PRE-DEPLOYMENT CHECKLIST**

### Prerequisites
- [ ] Chrome browser installed
- [ ] LinkedIn account with active job searches
- [ ] ZHIPU AI API key (currently hardcoded - see security notes)

---

## 📋 **INSTALLATION STEPS**

### 1. Load Extension in Chrome

```powershell
# Navigate to Chrome Extensions page
# Method 1: Type in address bar
chrome://extensions/

# Method 2: Menu → Extensions → Manage Extensions
```

**Steps:**
1. Enable "Developer mode" (toggle in top-right corner)
2. Click "Load unpacked"
3. Select the folder: `d:\work\repo\tmp\mingwork\llm_sample\chrome-ext`
4. Extension should appear in the list with LinkedIn icon

### 2. Configure Resume

1. Click on the extension icon in Chrome toolbar
2. Right-click → "Options" (or click the gear icon)
3. Paste your resume in the text area
4. Click "Save"
5. Verify "Resume saved." message appears

---

## 🧪 **MANUAL TESTING SCENARIOS**

### **Test 1: Basic Extension Loading**

**Steps:**
1. Navigate to any LinkedIn page
2. Open Chrome DevTools (F12)
3. Go to Console tab
4. Look for content script messages (should see injected logs)

**Expected Result:**
✅ No errors in console
✅ Content script loads automatically on LinkedIn pages

**Troubleshooting:**
- If no logs appear, refresh the LinkedIn page
- Check extension is enabled in chrome://extensions/
- Verify manifest.json has correct content_scripts URL patterns

---

### **Test 2: Apply to Single Job (Manual Mode)**

**Steps:**
1. Navigate to a LinkedIn job page with "Easy Apply" button
   - Example URL pattern: `https://www.linkedin.com/jobs/view/1234567890/`
2. Click the extension icon in toolbar
3. Click "Apply on This Page" button
4. Watch the DevTools console for logs

**Expected Result:**
✅ Sees "Content: Clicking the main Easy Apply button"
✅ LinkedIn Easy Apply modal opens
✅ Extension extracts questions
✅ Calls ZHIPU AI API
✅ Fills in form fields automatically
✅ Clicks "Next" or "Submit" button

**Troubleshooting:**
- **"Easy Apply button not found"**: Job may not have Easy Apply option
- **"No resume found"**: Go to options page and add resume
- **API errors**: Check API key is valid (check background.js line 4)
- **Form not filling**: Check DevTools console for selector errors

---

### **Test 3: Search Jobs (No Auto-Apply)**

**Steps:**
1. Click extension icon
2. Enter job title: "Software Engineer" (or any title)
3. **Uncheck** "Auto Apply" checkbox
4. Click "Search Jobs" button

**Expected Result:**
✅ New tab opens with LinkedIn search results
✅ URL is: `https://www.linkedin.com/jobs/search/?keywords=Software+Engineer`
✅ No automation happens (just opens search)

**Troubleshooting:**
- If tab doesn't open, check popup console (F12 on popup)
- Verify job title input has value

---

### **Test 4: Auto-Apply from Search (FULL AUTOMATION)**

⚠️ **WARNING**: This will automatically apply to multiple jobs. Use carefully!

**Steps:**
1. Click extension icon
2. Enter job title: "Senior backend engineer" (default value)
3. **Check** "Auto Apply (Use with caution!)" checkbox
4. Click "Search Jobs" button
5. Watch the automation process in DevTools

**Expected Result:**
✅ Search tab opens
✅ Extension clicks "All filters" button
✅ Enables "Easy Apply" filter
✅ Clicks "Show results"
✅ Extracts job links matching the title
✅ Closes search tab
✅ Opens first job in background tab
✅ Applies to job automatically
✅ Closes job tab
✅ Opens next job in queue
✅ Repeats until queue is empty

**Troubleshooting:**
- **"All filters button not found"**: LinkedIn UI may have changed
- **"No matching job links found"**: Check job title filter is working
- **Stops after first job**: Check for errors in console
- **Applies to wrong jobs**: Job title filter may need adjustment

---

### **Test 5: Form Field Types**

Create a test checklist for different input types:

**Prepare:** Find jobs with Easy Apply that have various question types

- [ ] **Text input**: "What is your current job title?"
  - Expected: AI fills with text from resume
  
- [ ] **Textarea**: "Why are you interested in this position?"
  - Expected: AI generates answer based on resume
  
- [ ] **Radio buttons**: "Are you legally authorized to work in the US? Yes/No"
  - Expected: AI selects appropriate radio button
  
- [ ] **Dropdown/Select**: "How many years of experience do you have?"
  - Expected: AI selects matching option from dropdown
  
- [ ] **Checkbox**: "I agree to the terms and conditions"
  - Expected: AI checks/unchecks based on answer (Yes/No/True/False)
  
- [ ] **Number input**: "Expected salary (USD)"
  - Expected: AI fills numeric value

**Verification:**
- Open DevTools → Console
- Look for "Content: Filling text/number for..." messages
- Manually verify filled values are reasonable

---

## 🔍 **VALIDATION CHECKS**

### **Code Quality**
```powershell
# Check for syntax errors
node -c background.js
node -c content.js
node -c popup.js
node -c options.js
```

### **Manifest Validation**
1. Go to chrome://extensions/
2. Look for any errors under the extension card
3. Click "Details" → Check "Errors" section

### **Console Logs to Monitor**

**Popup Console (when clicking extension icon):**
```
Popup: 'Apply on This Page' button clicked.
Popup: Sending ping to content script.
Popup: Received pong. Sending 'startApplication' message.
```

**Background Console (chrome://extensions/ → Details → Inspect service worker):**
```
Background: Received 'processJobQuestions' message.
Background: Sending request to ZHIPU AI API.
Background: Received response from ZHIPU AI API: {...}
Background: Parsed AI answers: {...}
```

**Content Script Console (F12 on LinkedIn page):**
```
Content: Received 'startApplication'.
Content: Starting application process on this page.
Content: Clicking the main Easy Apply button.
Content: Processing application modal step.
Content: Found X questions.
Content: Received AI answers, filling form.
Content: Filling text/number for 'Question' with 'Answer'
Content: Clicking Next button.
```

---

## 🐛 **COMMON ERRORS & FIXES**

### Error: "Uncaught ReferenceError: questions is not defined"
**Status:** ✅ FIXED in content.js line 176
**Fix:** Already applied - questions array is now declared

### Error: "startAutomation action not recognized"
**Status:** ✅ FIXED in popup.js line 40
**Fix:** Changed to 'startApplication'

### Error: "Cannot read property 'click' of null"
**Cause:** LinkedIn changed their UI selectors
**Fix:** Update selectors in content.js to match current LinkedIn DOM

### Error: "Failed to parse AI response"
**Cause:** AI returned malformed JSON
**Debug:** Check background console for raw AI response
**Fix:** Improve prompt or add better JSON extraction

### Error: "No resume found"
**Cause:** User hasn't added resume in options
**Fix:** Go to extension options page and paste resume

---

## 📊 **SUCCESS METRICS**

Your extension is working correctly if:

✅ **Zero console errors** during normal operation
✅ **Resume loads** from storage (check background logs)
✅ **Questions extracted** correctly (check content logs)
✅ **AI responds** with valid JSON (check background logs)
✅ **Form fields filled** automatically (visually verify)
✅ **Navigation works** (Next/Review/Submit buttons clicked)
✅ **Job queue processes** (for auto-apply mode)

---

## ⚠️ **CRITICAL SECURITY NOTE**

### **BEFORE FIRST USE:**

**The hardcoded API key MUST be secured!**

Current code (background.js line 4):
```javascript
const ZHIPU_AI_API_KEY = "30362898458c4f4a864acf2feae672c2.hhHauUMXLySfFGdS";
```

**Option 1: Move to Options Page (Recommended)**
1. Remove hardcoded key from background.js
2. Add API key input field to options.html
3. Store in chrome.storage.local
4. Retrieve from storage in background.js

**Option 2: Rotate the Key Immediately**
1. Go to ZHIPU AI dashboard
2. Revoke the exposed key
3. Generate new key
4. Update background.js (temporary until Option 1 is implemented)

**DO NOT distribute this extension with the current hardcoded key!**

---

## 🎯 **TESTING PRIORITY ORDER**

1. **High Priority** (before any real use):
   - [ ] Test 1: Extension loads without errors
   - [ ] Test 2: Single job application works
   - [ ] Resume is properly stored and retrieved
   - [ ] API key security addressed

2. **Medium Priority** (before bulk automation):
   - [ ] Test 4: Auto-apply from search works
   - [ ] All form field types are handled
   - [ ] Error handling works properly

3. **Low Priority** (nice to have):
   - [ ] Test 3: Search without auto-apply
   - [ ] Performance with many jobs
   - [ ] Edge case handling

---

## 📝 **TEST RESULTS LOG**

Create a simple log of your test results:

```
Date: ____________
Tester: ____________

Test 1 (Extension Loading): [ PASS / FAIL ]
Notes: _________________________________

Test 2 (Single Job Apply): [ PASS / FAIL ]
Notes: _________________________________

Test 3 (Search Only): [ PASS / FAIL ]
Notes: _________________________________

Test 4 (Auto-Apply): [ PASS / FAIL ]
Notes: _________________________________

Test 5 (Form Fields):
- Text input: [ PASS / FAIL ]
- Textarea: [ PASS / FAIL ]
- Radio buttons: [ PASS / FAIL ]
- Dropdown: [ PASS / FAIL ]
- Checkbox: [ PASS / FAIL ]
- Number input: [ PASS / FAIL ]

Overall Status: [ READY / NEEDS WORK ]
```

---

## 🚀 **NEXT STEPS AFTER TESTING**

If all tests pass:
1. Document any LinkedIn UI changes needed for selectors
2. Add rate limiting (delay between applications)
3. Implement API key security fix
4. Add user notifications for progress
5. Create production build

If tests fail:
1. Note all failures in test log
2. Check console errors
3. Review ANALYSIS.md for known issues
4. Update selectors if LinkedIn UI changed
5. Re-test after fixes

---

*Testing guide created: 2025-11-26*
*Version: 1.0*
