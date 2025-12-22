// ZHIPU AI Configuration
const ZHIPU_AI_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions";

// State management
let jobQueue = [];
let autoApplyJobTitle = null;
let initialSearchTabId = null;
let autoApplyEnabled = false;

console.log("Background: Script loaded. Listening for events.");

// Main message listener
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log(`Background: Received message: action = '${request.action}'`, request);

  switch (request.action) {
    case "startAutoApplyProcess":
      handleStartAutoApplyProcess(request, sendResponse);
      break;

    case "jobLinksFound":
      handleJobLinksFound(request, sender, sendResponse);
      break;

    case "processJobQuestions":
      handleProcessJobQuestions(request, sendResponse);
      return true; // Indicates async response

    case "applicationStepCompleted":
    case "applicationSubmitted":
      handleApplicationProgress(request);
      break;

    case "autoApplyError":
      handleAutoApplyError(request);
      break;

    default:
      console.warn(`Background: Received an unknown message action: ${request.action}`);
      break;
  }

  return true; // Keep the message channel open for async responses if needed
});

function handleStartAutoApplyProcess(request, sendResponse) {
  console.log("Background: Handling 'startAutoApplyProcess'. Job Title:", request.jobTitle, "Tab ID:", request.tabId);
  autoApplyJobTitle = request.jobTitle;
  initialSearchTabId = request.tabId;
  autoApplyEnabled = request.autoApply || false;
  console.log("Background: State updated -> autoApplyEnabled:", autoApplyEnabled, "initialSearchTabId:", initialSearchTabId);

  // If starting on an existing, already loaded tab, we just update state here.
  // The popup will send the 'startAutoApply' message directly to the content script
  // to ensure it triggers immediately and reliably.
  if (request.isExistingTab) {
    console.log("Background: 'isExistingTab' is true. State updated. Waiting for 'jobLinksFound' from content script.");
  }
  // For new tabs, the chrome.tabs.onUpdated listener will handle sending the message.

  if (sendResponse) {
    sendResponse({ success: true });
  }
}

function handleJobLinksFound(request, sender, sendResponse) {
  try {
    console.log(`Background: Handling 'jobLinksFound'. Found ${request.jobLinks.length} links.`);

    // Always update the tab ID from the sender to ensure we are talking to the right tab
    if (sender && sender.tab && sender.tab.id) {
      initialSearchTabId = sender.tab.id;
      console.log("Background: Updated initialSearchTabId from sender:", initialSearchTabId);
    } else if (!initialSearchTabId) {
      console.error("Background: CRITICAL ERROR - initialSearchTabId is missing and sender info is unavailable!");
      if (sendResponse) sendResponse({ success: false, error: "Missing tab ID" });
      return;
    }

    jobQueue = request.jobLinks;
    console.log("Background: Job queue populated. Starting processing.");

    if (sendResponse) sendResponse({ success: true });

    processNextJob();
  } catch (error) {
    console.error("Background: Exception in handleJobLinksFound:", error);
    if (sendResponse) sendResponse({ success: false, error: error.message });
  }
}

function handleApplicationProgress(request) {
  console.log(`Background: Handling '${request.action}'.`);
  if (request.action === "applicationSubmitted") {
    console.log("Background: Application submitted. Processing next job in queue.");
    processNextJob();
  } else { // applicationStepCompleted
    if (initialSearchTabId) {
      console.log("Background: Step completed. Sending 'continueApplication' to content script.");
      chrome.tabs.sendMessage(initialSearchTabId, { action: "continueApplication" });
    }
  }
}

function handleAutoApplyError(request) {
  console.error("Background: Handling 'autoApplyError'. Message:", request.message);
  // Errors on the main search page are final
  if (sender.tab.id === initialSearchTabId) {
    console.error("Background: Error occurred on the main search page. Stopping process.");
    resetState();
  } else {
    // Errors on a specific job page, just move to the next one
    console.log("Background: Error on job page, processing next job.");
    processNextJob();
  }
}

// AI Question Processing
function handleProcessJobQuestions(request, sendResponse) {
  console.log("Background: Handling 'processJobQuestions'.");
  const { questionsData, jobDescription } = request.data;

  chrome.storage.local.get(["resume", "apiKey"], (data) => {
    const resume = data.resume || "";
    const apiKey = data.apiKey || "";

    if (!resume.trim()) {
      console.error("Background: Resume not found in storage.");
      sendResponse({ error: "No resume found. Please add your resume in the extension options page." });
      return;
    }

    if (!apiKey.trim()) {
      console.error("Background: API Key not found in storage.");
      sendResponse({ error: "No API Key found. Please add your Zhipu AI API Key in the extension options page." });
      return;
    }

    const preAnswered = {};
    const questionsForAI = questionsData.filter(item => {
      const q = item.question;
      const lowerQ = q.toLowerCase();
      if (lowerQ.includes("commutable distance") || lowerQ.includes("comfortable commuting")) {
        preAnswered[q] = "Yes";
        return false;
      }
      if (lowerQ.includes("drug test") || lowerQ.includes("willing to take a drug test")) {
        preAnswered[q] = "Yes";
        return false;
      }
      return true;
    });

    if (questionsForAI.length === 0) {
      console.log("Background: All questions were pre-answered.");
      sendResponse({ answers: preAnswered });
      return;
    }

    const questionsFormatted = questionsForAI.map(item => {
      if (item.options) {
        return `Question: ${item.question}\nOptions: ${item.options.join(", ")}`;
      }
      return `Question: ${item.question}`;
    }).join("\n\n");

    const prompt = `Based on my resume, please answer the following questions for a job application. 
 
 CRITICAL RULES - MUST FOLLOW:
 - For "How many" questions: answer with ONLY a pure number, nothing else (e.g., "5" NOT "5 years" or "Five" or "5+")
 - For Yes/No questions: answer ONLY "Yes" or "No"
 - For numeric questions (salary, etc.): answer with ONLY the number (e.g., "120000")
 - For text questions: maximum 3 words
 - IF OPTIONS ARE PROVIDED: You MUST choose EXACTLY one of the provided options. DO NOT deviate.
 - NEVER add units, words, explanations, or symbols
 
 My Resume:
 ---
 ${resume}
 ---
 
 Job Description:
 ---
 ${jobDescription}
 ---
 
 Questions:
 ${questionsFormatted}
 
 Return ONLY a valid JSON object. The keys must be the exact "Question" strings provided above (excluding the "Options" part), and the values must follow the rules above.
 
 Examples of CORRECT answers:
 - "How many years of experience do you have with Java?": "8"
 - "Are you authorized to work?": "Yes"
 - "What is your preferred contact method?": "Email" (if Options were: Email, Phone, SMS)
 
 Do NOT include markdown formatting (like \`\`\`json ... \`\`\`), just the raw JSON.`;

    console.log("Background: Sending request to ZHIPU AI API for", questionsForAI.length, "questions.");
    fetch(ZHIPU_AI_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`,
      },
      body: JSON.stringify({ model: "glm-4", messages: [{ role: "user", content: prompt }] }),
    })
      .then(async (response) => {
        console.log("Background: Received API response status:", response.status);
        if (!response.ok) {
          const errorText = await response.text();
          console.error("Background: API Error Body:", errorText);
          throw new Error(`API request failed with status ${response.status}: ${errorText}`);
        }
        return response.json();
      })
      .then(apiResponse => {
        console.log("Background: Parsed API JSON response:", apiResponse);
        if (apiResponse.choices && apiResponse.choices.length > 0) {
          const content = apiResponse.choices[0].message.content;
          console.log("Background: AI Raw Content:", content);

          try {
            const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/);
            let answers;
            if (jsonMatch) {
              answers = JSON.parse(jsonMatch[1]);
            } else {
              const jsonObjectMatch = content.match(/{[\s\S]*}/);
              if (jsonObjectMatch) {
                answers = JSON.parse(jsonObjectMatch[0]);
              } else {
                // Try parsing the whole content if it looks like JSON
                answers = JSON.parse(content);
              }
            }
            const finalAnswers = { ...preAnswered, ...answers };
            console.log("Background: Parsed AI answers successfully.", finalAnswers);
            sendResponse({ answers: finalAnswers });
          } catch (error) {
            console.error("Background: Failed to parse AI response.", error, content);
            sendResponse({ error: "Failed to parse AI response. Check console for raw output." });
          }
        } else {
          console.error("Background: No choices from AI.", apiResponse);
          sendResponse({ error: "No valid response from AI provider." });
        }
      })
      .catch(error => {
        console.error("Background: Error calling ZHIPU AI API:", error);
        sendResponse({ error: `Failed to call AI API: ${error.message}` });
      });
  });
}

function processNextJob() {
  if (jobQueue.length > 0) {
    const jobUrl = jobQueue.shift();
    console.log(`Background: Processing next job. URL: ${jobUrl}. Jobs left: ${jobQueue.length}`);

    if (initialSearchTabId) {
      console.log(`Background: Sending 'clickJobCard' to tab ${initialSearchTabId}`);
      chrome.tabs.sendMessage(initialSearchTabId, { action: "clickJobCard", jobUrl: jobUrl }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Background: Error sending 'clickJobCard' message:", chrome.runtime.lastError.message, ". Moving to next job.");
          processNextJob(); // Try next job if sending fails
        } else {
          console.log("Background: 'clickJobCard' message sent successfully.");
        }
      });
    } else {
      console.error("Background: 'initialSearchTabId' is null. Cannot process job queue.");
      resetState();
    }
  } else {
    console.log("Background: Job queue is empty. Auto-apply process finished.");
    resetState();
  }
}

// Listen for tab updates, specifically for the initial search tab
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (tabId === initialSearchTabId && changeInfo.status === "complete" && tab.url && tab.url.includes("linkedin.com/jobs/search")) {
    console.log("Background: Target search tab (ID:", tabId, ") has finished loading.");

    if (autoApplyEnabled) {
      console.log("Background: Auto-apply is ON. Sending 'startAutoApply' to content script.");
      // Adding a small delay to ensure content script is ready
      setTimeout(() => {
        chrome.tabs.sendMessage(tabId, { action: "startAutoApply", jobTitle: autoApplyJobTitle }, (response) => {
          if (chrome.runtime.lastError) {
            console.error("Background: Error sending 'startAutoApply' message:", chrome.runtime.lastError.message);
          } else {
            console.log("Background: 'startAutoApply' message sent successfully, awaiting 'jobLinksFound'.");
          }
        });
        autoApplyJobTitle = null; // Prevent re-sending
      }, 2000);
    } else {
      console.log("Background: Auto-apply is OFF (manual search). No message sent.");
      resetState();
    }
  }
});

function resetState() {
  console.log("Background: Resetting state.");
  jobQueue = [];
  autoApplyJobTitle = null;
  initialSearchTabId = null;
  autoApplyEnabled = false;
}

// Clean up if the search tab is closed manually
chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
  if (tabId === initialSearchTabId) {
    console.log("Background: Initial search tab was closed. Resetting state.");
    resetState();
  }
});