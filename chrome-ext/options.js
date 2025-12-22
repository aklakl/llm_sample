const resumeTextarea = document.getElementById("resume");
const apiKeyInput = document.getElementById("apiKey");
const saveButton = document.getElementById("save");
const status = document.getElementById("status");

// Load the saved settings
chrome.storage.local.get(["resume", "apiKey"], (data) => {
  if (data.resume) {
    resumeTextarea.value = data.resume;
  }
  if (data.apiKey) {
    apiKeyInput.value = data.apiKey;
  }
});

// Save the settings
saveButton.addEventListener("click", () => {
  const resume = resumeTextarea.value;
  const apiKey = apiKeyInput.value.trim();

  chrome.storage.local.set({ resume, apiKey }, () => {
    status.textContent = "Settings saved.";
    setTimeout(() => {
      status.textContent = "";
    }, 2000);
  });
});
