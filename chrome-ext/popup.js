// DOM元素
const startSmartApplyButton = document.getElementById("start-smart-apply");
const manualSearchButton = document.getElementById("manual-search");
const applyCurrentPageButton = document.getElementById("apply-current-page");
const jobTitleInput = document.getElementById("job-title");
const statusMessage = document.getElementById("status-message");
const openOptionsLink = document.getElementById("open-options");

// 加载保存的职位名称
chrome.storage.local.get(["jobTitle"], (data) => {
  if (data.jobTitle) {
    jobTitleInput.value = data.jobTitle;
  }
});

// 保存职位名称
jobTitleInput.addEventListener("change", () => {
  chrome.storage.local.set({ jobTitle: jobTitleInput.value.trim() });
});

// 显示状态消息
function showStatus(message, duration = 3000) {
  statusMessage.textContent = message;
  statusMessage.style.display = "block";
  if (duration > 0) {
    setTimeout(() => {
      statusMessage.style.display = "none";
    }, duration);
  }
}

// 1. 智能自动申请按钮
// 1. 智能自动申请按钮
startSmartApplyButton.addEventListener("click", () => {
  console.log("Popup: 'Smart Auto Apply' button clicked.");
  const jobTitle = jobTitleInput.value.trim();

  if (!jobTitle) {
    alert("⚠️ 请先输入职位名称！\n\nPlease enter a job title first.");
    return;
  }

  // 保存职位名称
  chrome.storage.local.set({ jobTitle: jobTitle });

  // 检查当前标签页
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];
    const currentUrl = currentTab.url || "";

    // 判断当前是否已经是LinkedIn的Easy Apply搜索页
    if ((currentUrl.includes("linkedin.com/jobs/search/") && currentUrl.includes("f_AL=true")) || currentUrl.includes("linkedin.com/jobs/search-results/")) {
      console.log("Popup: Current tab is already a LinkedIn Easy Apply search page.");

      // Try to ping the content script to see if it's alive
      chrome.tabs.sendMessage(currentTab.id, { action: "ping" }, (response) => {
        if (chrome.runtime.lastError) {
          console.warn("Popup: Content script not responding (likely dead after extension reload). Reloading page.");
          showStatus("🔄 刷新页面以加载脚本...", 4000);

          // Tell background to expect a reload and start auto-apply after it finishes
          chrome.runtime.sendMessage({
            action: "startAutoApplyProcess",
            jobTitle: jobTitle,
            tabId: currentTab.id,
            autoApply: true,
            isExistingTab: false // Treat as new load so background waits for 'complete' status
          });

          chrome.tabs.reload(currentTab.id);
        } else {
          console.log("Popup: Content script is alive. Starting process immediately.");
          showStatus("▶️ 在当前页面启动...", 2000);

          // 1. Tell background to update state (fire and forget, or log success)
          chrome.runtime.sendMessage({
            action: "startAutoApplyProcess",
            jobTitle: jobTitle,
            tabId: currentTab.id,
            autoApply: true,
            isExistingTab: true
          }, (response) => {
            if (chrome.runtime.lastError) {
              console.error("Popup: Error updating background:", chrome.runtime.lastError.message);
            } else {
              console.log("Popup: Background state updated.");
            }
          });

          // 2. Send start command directly to content script IMMEDIATELY
          console.log("Popup: Sending 'startAutoApply' directly to content script.");
          chrome.tabs.sendMessage(currentTab.id, {
            action: "startAutoApply",
            jobTitle: jobTitle
          });
        }
      });

    } else {
      // 打开新页面
      const searchUrl = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(jobTitle)}&f_AL=true`;
      console.log("Popup: Opening new LinkedIn search tab:", searchUrl);
      showStatus("🚀 正在打开LinkedIn...", 2000);

      chrome.tabs.create({ url: searchUrl }, (newTab) => {
        console.log("Popup: New tab created, sending 'startAutoApplyProcess' to background.");
        chrome.runtime.sendMessage({
          action: "startAutoApplyProcess",
          jobTitle: jobTitle,
          tabId: newTab.id,
          autoApply: true,
          isExistingTab: false
        });
      });
    }
  });
});

// 2. 仅打开搜索页按钮（不自动申请）
manualSearchButton.addEventListener("click", () => {
  console.log("Popup: 'Manual Search' button clicked.");
  const jobTitle = jobTitleInput.value.trim();

  if (!jobTitle) {
    alert("⚠️ 请先输入职位名称！\n\nPlease enter a job title first.");
    return;
  }

  // 保存职位名称
  chrome.storage.local.set({ jobTitle: jobTitle });

  // 构建LinkedIn搜索URL（带Easy Apply筛选）
  const searchUrl = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(jobTitle)}&f_AL=true`;

  console.log("Popup: Opening LinkedIn search (manual mode):", searchUrl);
  showStatus("🔍 正在打开搜索页...", 2000);

  chrome.tabs.create({ url: searchUrl });
});

// 3. 申请当前页面按钮
applyCurrentPageButton.addEventListener("click", () => {
  console.log("Popup: 'Apply Current Page' button clicked.");

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs.length === 0) {
      console.error("Popup: No active tab found.");
      alert("❌ 错误：未找到活动标签页。\n\nError: No active tab found.");
      return;
    }

    const tab = tabs[0];
    const tabId = tab.id;
    const url = tab.url || "";

    // 检查是否在LinkedIn职位页面
    if (!url.includes("linkedin.com/jobs/view/")) {
      alert("⚠️ 请先打开LinkedIn职位详情页！\n\nPlease navigate to a LinkedIn job detail page first!\n\nThis feature only works on:\n• linkedin.com/jobs/view/...\n\nCurrent page: " + (url.length > 50 ? url.substring(0, 50) + "..." : url));
      return;
    }

    console.log("Popup: Sending ping to content script.");
    showStatus("📡 正在连接...", 0);

    chrome.tabs.sendMessage(tabId, { action: "ping" }, (response) => {
      if (chrome.runtime.lastError) {
        console.error("Popup: Could not establish connection.", chrome.runtime.lastError.message);
        showStatus("", 0);
        alert("⚠️ 内容脚本未加载。\n\nContent script not loaded.\n\n请刷新LinkedIn页面后重试。\nPlease RELOAD the LinkedIn page and try again.\n\nIf the problem persists:\n1. Check that the extension is enabled\n2. Try closing and reopening the tab");
        return;
      }

      if (response && response.status === "pong") {
        console.log("Popup: Received pong. Sending 'startApplication' message.");
        showStatus("✨ 正在申请...", 0);

        chrome.tabs.sendMessage(tabId, { action: "startApplication" }, (response) => {
          if (chrome.runtime.lastError) {
            console.error("Popup: Error sending startApplication:", chrome.runtime.lastError.message);
            showStatus("❌ 申请失败", 3000);
          } else {
            showStatus("✅ 申请流程已启动！", 3000);
          }
        });
      } else {
        console.error("Popup: Received an invalid response from content script:", response);
        showStatus("", 0);
        alert("⚠️ 收到意外响应。\n\nUnexpected response from content script.\n\n请刷新页面后重试。\nPlease reload the page and try again.");
      }
    });
  });
});

// 4. 打开设置页面
openOptionsLink.addEventListener("click", (e) => {
  e.preventDefault();
  chrome.runtime.openOptionsPage();
});
