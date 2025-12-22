// Log to confirm the script is injected and running
console.log("Content Script: Injected and running on", window.location.href);

// URL Monitoring: Auto-redirect if navigated to job detail page
// This prevents getting stuck on individual job pages instead of the search results
let lastKnownSearchUrl = null;
if (window.location.href.includes('/jobs/search')) {
  lastKnownSearchUrl = window.location.href;
  console.log("Content: Saved search URL:", lastKnownSearchUrl);
}

// Monitor URL changes (for single-page app navigation)
let currentUrl = window.location.href;
setInterval(() => {
  if (window.location.href !== currentUrl) {
    currentUrl = window.location.href;
    console.log("Content: URL changed to:", currentUrl);

    // If we're on a job detail page and we have a saved search URL, redirect back
    if (currentUrl.includes('/jobs/view/') && lastKnownSearchUrl) {
      console.warn("Content: Unwanted navigation to job detail page detected! Redirecting back to:", lastKnownSearchUrl);
      setTimeout(() => {
        window.location.href = lastKnownSearchUrl;
      }, 1000); // Small delay to ensure current navigation completes
    } else if (currentUrl.includes('/jobs/search')) {
      lastKnownSearchUrl = currentUrl;
      console.log("Content: Updated saved search URL:", lastKnownSearchUrl);
    }
  }
}, 500); // Check every 500ms


chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log(`Content: Received message: action = '${request.action}'`, request);

  switch (request.action) {
    case "ping":
      sendResponse({ status: "pong" });
      break;

    case "startAutoApply":
      autoApplyProcess(request.jobTitle);
      sendResponse({ status: "started" });
      break;

    case "startApplication":
      startApplication();
      sendResponse({ status: "started" });
      break;

    case "clickJobCard":
      clickJobCard(request.jobUrl);
      sendResponse({ status: "clicked" });
      break;

    case "continueApplication":
      processApplicationModal();
      sendResponse({ status: "continuing" });
      break;

    default:
      console.warn(`Content: Received an unknown message action: ${request.action}`);
      break;
  }

  return true; // Keep message channel open for async responses
});

async function clickJobCard(jobUrl) {
  console.log("Content (clickJobCard): Trying to click job card for URL:", jobUrl);

  // More robust regex to capture ID, handling query parameters or trailing slashes
  const jobIDMatch = jobUrl.match(/view\/(\d+)/);
  if (!jobIDMatch) {
    console.error("Content (clickJobCard): Could not extract job ID from URL:", jobUrl);
    chrome.runtime.sendMessage({ action: "autoApplyError", message: "Invalid Job URL format." });
    return;
  }
  const jobID = jobIDMatch[1];
  console.log("Content (clickJobCard): Extracted Job ID:", jobID);

  // Try multiple strategies to find the job card element by ID
  let jobCardElement =
    document.querySelector(`li[data-occludable-job-id="${jobID}"]`) ||
    document.querySelector(`div[data-job-id="${jobID}"]`) ||
    document.querySelector(`li.jobs-search-results__list-item:has(a[href*="${jobID}"])`); // Use :has() if supported

  if (jobCardElement) {
    console.log("Content (clickJobCard): Found job card element:", jobCardElement);

    // Scroll the card into view
    jobCardElement.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Brief highlight to visually confirm
    const originalBg = jobCardElement.style.backgroundColor;
    jobCardElement.style.backgroundColor = 'yellow';

    setTimeout(() => {
      jobCardElement.style.backgroundColor = originalBg;

      // CRITICAL: Prevent navigation by clicking the card container, NOT the link
      // Find all links in the card and prevent their default behavior
      const links = jobCardElement.querySelectorAll('a');
      const preventNav = (e) => {
        console.log("Content (clickJobCard): Preventing link navigation");
        e.preventDefault();
        e.stopPropagation();
        return false;
      };

      // Temporarily attach preventDefault to all links
      links.forEach(link => {
        link.addEventListener('click', preventNav, { capture: true, once: true });
      });

      // Click the card container itself (not any link inside it)
      console.log("Content (clickJobCard): Clicking card container");

      // Use MouseEvent to simulate a click on the container
      const clickEvent = new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window,
        detail: 1
      });
      jobCardElement.dispatchEvent(clickEvent);

      // Also try direct click as fallback
      setTimeout(() => {
        // Remove the event listeners after a delay
        links.forEach(link => {
          link.removeEventListener('click', preventNav, { capture: true });
        });
      }, 1000);

      console.log("Content (clickJobCard): Clicked. Waiting for job details to load.");

      // Wait for the job details panel to update
      setTimeout(startApplication, 3000); // 3-second wait
    }, 1000);
  } else {
    console.error("Content (clickJobCard): Could not find job card for Job ID:", jobID);

    // Fallback: Try to find any visible card and click it
    console.log("Content (clickJobCard): Attempting fallback - looking for any link with this job ID");
    const anyLink = document.querySelector(`a[href*="/jobs/view/${jobID}"]`);
    if (anyLink) {
      const parentCard = anyLink.closest('li.jobs-search-results__list-item') ||
        anyLink.closest('div.job-card-container');

      if (parentCard) {
        console.log("Content (clickJobCard): Found parent card via link, clicking it");
        parentCard.scrollIntoView({ behavior: 'smooth', block: 'center' });

        setTimeout(() => {
          // Prevent link navigation
          anyLink.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
          }, { capture: true, once: true });

          // Click the parent card
          parentCard.click();

          setTimeout(startApplication, 3000);
        }, 1000);
        return;
      }
    }

    console.error("Content (clickJobCard): All methods failed. Skipping this job.");
    chrome.runtime.sendMessage({ action: "autoApplyError", message: "Could not find job card on page." });
  }
}

let isProcessing = false;
let stepRetryCount = 0;
const MAX_STEP_RETRIES = 3;
let validationRetryCount = 0;
const MAX_VALIDATION_RETRIES = 3;

async function autoApplyProcess(jobTitleFilter) {
  if (isProcessing) {
    console.log("Content (autoApplyProcess): Already processing. Ignoring request.");
    return;
  }
  isProcessing = true;
  stepRetryCount = 0; // Reset retry counter for new job
  console.log("Content (autoApplyProcess): Starting for filter:", jobTitleFilter);

  const jobCardSelectors = [
    'div.job-card-container--clickable',
    'li.jobs-search-results__list-item',
    'div[data-job-id]'
  ];
  let jobCards = [];

  // Polling mechanism: Wait up to 10 seconds for job cards to appear
  const maxRetries = 20;
  const interval = 500; // 500ms * 20 = 10 seconds

  for (let i = 0; i < maxRetries; i++) {
    for (const selector of jobCardSelectors) {
      jobCards = document.querySelectorAll(selector);
      if (jobCards.length > 0) {
        console.log(`Content (autoApplyProcess): Found ${jobCards.length} elements using selector "${selector}" on attempt ${i + 1}.`);
        break;
      }
    }
    if (jobCards.length > 0) break;

    console.log(`Content (autoApplyProcess): No job cards found yet. Waiting... (${i + 1}/${maxRetries})`);
    await new Promise(resolve => setTimeout(resolve, interval));
  }

  if (jobCards.length === 0) {
    console.error("Content (autoApplyProcess): No job cards found after waiting. LinkedIn UI may have changed.");
    chrome.runtime.sendMessage({ action: "autoApplyError", message: "No job cards found on the search results page." });
    return;
  }

  console.log(`Content (autoApplyProcess): Found ${jobCards.length} total potential job cards.`);

  const jobLinks = [];
  const titleLinkSelectors = [
    'a.job-card-list__title',
    'a.job-card-container__link',
    'a[href*="/jobs/view/"]'
  ];

  if (!jobTitleFilter) {
    console.warn("Content (autoApplyProcess): jobTitleFilter is missing. Defaulting to empty string for safety.");
    jobTitleFilter = "";
  }

  const filterWords = jobTitleFilter.toLowerCase().split(/\s+/).filter(w => w.length > 0);
  console.log("Content (autoApplyProcess): Filter words (Ignored for filtering):", filterWords);

  jobCards.forEach((card, index) => {
    let titleLinkElement = null;
    for (const selector of titleLinkSelectors) {
      titleLinkElement = card.querySelector(selector);
      if (titleLinkElement) break;
    }

    if (titleLinkElement && titleLinkElement.href) {
      const title = (titleLinkElement.innerText || "").toLowerCase().trim();
      const link = titleLinkElement.href;

      console.log(`Content (autoApplyProcess): [${index + 1}/${jobCards.length}] Processing card. Title: "${title}", Link: "${link}"`);

      // Check if job has already been applied to
      const appliedButton = card.querySelector('.jobs-apply-button--applied') ||
        Array.from(card.querySelectorAll('button, span')).find(el =>
          el.textContent.trim() === 'Applied' || el.textContent.trim().includes('Applied')
        );

      if (appliedButton) {
        console.log(`Content (autoApplyProcess): ⚠️ Job already applied. Looking for dismiss button...`);

        // Trigger hover to make dismiss button visible (it might be hidden)
        const hoverEvent = new MouseEvent('mouseenter', { bubbles: true, cancelable: true });
        card.dispatchEvent(hoverEvent);

        // Wait a bit for hover effects
        setTimeout(() => {
          // Try multiple selectors for the dismiss button
          let dismissButton = null;

          const selectors = [
            'button[aria-label*="Dismiss"]',
            'button[data-control-name="discard_job_card"]',
            'button.job-card-container__action',
            'button.jobs-save-button',
            'button[data-test-job-card-dismiss-button]',
            'button.artdeco-button--circle',
            'button > svg[data-test-icon="close-small"]',
            'button[aria-label*="close"]'
          ];

          for (const selector of selectors) {
            dismissButton = card.querySelector(selector);
            if (dismissButton) {
              console.log(`Content (autoApplyProcess): ✓ Found dismiss button with selector: ${selector}`);
              break;
            }
          }

          if (!dismissButton) {
            // Fallback: find any button with close/dismiss icon
            const buttons = card.querySelectorAll('button');
            dismissButton = Array.from(buttons).find(btn => {
              const svg = btn.querySelector('svg');
              return svg && (
                svg.getAttribute('data-test-icon') === 'close-small' ||
                svg.querySelector('use[href*="close"]') ||
                btn.getAttribute('aria-label')?.toLowerCase().includes('dismiss')
              );
            });

            if (dismissButton) {
              console.log(`Content (autoApplyProcess): ✓ Found dismiss button via SVG fallback`);
            }
          }

          if (dismissButton) {
            console.log(`Content (autoApplyProcess): ✓ Clicking dismiss button to hide applied job.`);
            dismissButton.click();
          } else {
            console.log(`Content (autoApplyProcess): ⚠️ Dismiss button not found for applied job. Tried all selectors.`);
            console.log(`Content (autoApplyProcess): Card HTML:`, card.outerHTML.substring(0, 500));
          }
        }, 200);

        // Skip adding this job to the list
        return;
      }

      // DIRECTLY ADD TO JOB LINKS - REMOVED FILTERING LOGIC
      console.log(`Content (autoApplyProcess): ✓ Adding job to list (Filtering disabled).`);
      jobLinks.push(link);
    } else {
      console.log(`Content (autoApplyProcess): [${index + 1}/${jobCards.length}] Could not find a valid title/link element in this card.`);
    }
  });

  console.log(`Content (autoApplyProcess): Found ${jobLinks.length} matching jobs.`);

  if (jobLinks.length > 0) {
    console.log("Content (autoApplyProcess): Sending 'jobLinksFound' to background script.");
    chrome.runtime.sendMessage({ action: "jobLinksFound", jobLinks: jobLinks }, (response) => {
      if (chrome.runtime.lastError) {
        console.error("Content (autoApplyProcess): Error sending jobLinksFound:", chrome.runtime.lastError.message);
      } else {
        console.log("Content (autoApplyProcess): jobLinksFound sent successfully.");
      }
    });
  } else {
    console.error("Content (autoApplyProcess): No matching jobs found for the filter.");
    chrome.runtime.sendMessage({
      action: "autoApplyError",
      message: `No jobs found matching "${jobTitleFilter}".`
    });
  }
  isProcessing = false;
}

async function startApplication() {
  console.log("Content (startApplication): Starting application on current view.");

  // Wait for the details panel to be ready
  await new Promise(resolve => setTimeout(resolve, 1500));

  const easyApplyButton =
    document.querySelector('.jobs-apply-button:not(.jobs-apply-button--applied)') ||
    document.querySelector('button[aria-label*="Easy Apply"]') ||
    Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Easy Apply'));

  if (easyApplyButton) {
    console.log("Content (startApplication): Easy Apply button found. Clicking it.");
    easyApplyButton.click();
    setTimeout(processApplicationModal, 2000); // Wait for modal
  } else {
    console.log("Content (startApplication): Easy Apply button not found or already applied. Skipping.");
    chrome.runtime.sendMessage({ action: "autoApplyError", message: "Easy Apply button not found or already applied." });
  }
}

async function processApplicationModal() {
  console.log("Content (processApplicationModal): Processing step.");

  // Check if we're stuck in a loop
  stepRetryCount++;
  if (stepRetryCount > MAX_STEP_RETRIES) {
    console.error(`Content (processApplicationModal): Exceeded ${MAX_STEP_RETRIES} retries on this step. Skipping job.`);
    chrome.runtime.sendMessage({
      action: "autoApplyError",
      message: "Stuck in loop - unable to complete application form."
    });
    stepRetryCount = 0;
    return;
  }

  await new Promise(resolve => setTimeout(resolve, 1500));

  const jobDescription = document.querySelector('.jobs-box__html-content')?.innerHTML || document.querySelector('.job-details-jobs-unified-top-card__primary-description-container')?.innerText || '';
  const formElementSelectors = '.fb-dash-form-element, .fb-form-element, .jobs-easy-apply-form-section__grouping, .jobs-easy-apply-form-element';
  const questionElements = document.querySelectorAll(formElementSelectors);
  const questionsData = Array.from(questionElements).map(q => {
    const label = q.querySelector('label')?.innerText.trim();
    if (!label) return null;

    const options = [];
    // Standard Select
    const select = q.querySelector('select');
    if (select) {
      Array.from(select.options).forEach(opt => {
        const text = opt.innerText.trim();
        if (text && !text.toLowerCase().includes('select an option') && !text.toLowerCase().includes('choose')) {
          options.push(text);
        }
      });
    }
    // Radio buttons
    const radios = q.querySelectorAll('input[type="radio"]');
    radios.forEach(r => {
      const rLabel = document.querySelector(`label[for='${r.id}']`)?.innerText.trim();
      if (rLabel) options.push(rLabel);
    });

    return { question: label, options: options.length > 0 ? options : null };
  }).filter(Boolean);

  console.log(`Content (processApplicationModal): Found ${questionsData.length} questions.`);

  if (questionsData.length > 0) {
    console.log("Content (processApplicationModal): Sending questions to background for AI processing.");
    chrome.runtime.sendMessage({ action: "processJobQuestions", data: { questionsData, jobDescription } }, async (response) => {
      if (response && response.answers) {
        console.log("Content (processApplicationModal): Received AI answers. Filling form.", response.answers);
        await fillForm(response.answers);
        await clickNextOrSubmit();
      } else {
        console.warn("Content (processApplicationModal): Failed to get answers from AI. Response:", JSON.stringify(response));
        console.log("Content (processApplicationModal): Attempting to click Next/Submit anyway (form might be pre-filled).");
        // Fallback: Try to click next even if AI failed
        await clickNextOrSubmit();
      }
    });
  } else {
    console.log("Content (processApplicationModal): No questions found. Clicking next/submit.");
    await clickNextOrSubmit();
  }
}

async function fillForm(answers) {
  console.log("Content (fillForm): Starting to fill form fields.");
  const formElementSelectors = '.fb-dash-form-element, .fb-form-element, .jobs-easy-apply-form-section__grouping, .jobs-easy-apply-form-element';
  const questionElements = document.querySelectorAll(formElementSelectors);

  for (const qElement of questionElements) {
    const label = qElement.querySelector('label')?.innerText.trim();
    if (label) {
      // Fuzzy match the label with keys in answers
      const answerKey = Object.keys(answers).find(key => key.toLowerCase().trim() === label.toLowerCase());

      if (answerKey) {
        const answer = answers[answerKey];
        console.log(`Content (fillForm): Found answer for '${label}': '${answer}'`);

        // Try to fill various input types
        const textInput = qElement.querySelector('input[type="text"], input[type="number"], textarea');
        const radioButtons = qElement.querySelectorAll('input[type="radio"]');
        const checkbox = qElement.querySelector('input[type="checkbox"]');
        const select = qElement.querySelector('select');

        // LinkedIn custom dropdown (artdeco-dropdown, select-button pattern)
        const customDropdownButton = qElement.querySelector('select[data-test-text-entity-list-form-select]') ||
          qElement.querySelector('button[aria-haspopup="listbox"]') ||
          qElement.querySelector('button[role="combobox"]') ||
          qElement.querySelector('.artdeco-dropdown__trigger');

        if (textInput) {
          console.log(`Content (fillForm): Filling text for '${label}' with '${answer}'`);
          textInput.value = answer;
          textInput.dispatchEvent(new Event('input', { bubbles: true }));
        } else if (radioButtons.length > 0) {
          console.log(`Content (fillForm): Matching radio buttons for '${label}' against '${answer}'`);
          let matched = false;
          for (const radio of radioButtons) {
            const radioLabel = (document.querySelector(`label[for='${radio.id}']`)?.innerText || "").trim().toLowerCase();
            const normalizedAnswer = answer.toLowerCase().trim();

            if (radioLabel === normalizedAnswer ||
              radioLabel.includes(normalizedAnswer) ||
              normalizedAnswer.includes(radioLabel)) {
              console.log(`Content (fillForm): Selecting radio '${radioLabel}' for '${label}'`);
              radio.click();
              radio.dispatchEvent(new Event('change', { bubbles: true }));
              matched = true;
              break;
            }
          }
          if (!matched) {
            console.warn(`Content (fillForm): ⚠️ No matching radio found for '${label}'. Answer: '${answer}'`);
          }
        } else if (checkbox) {
          // For checkboxes, assume "Yes" or "True" means check it
          const shouldCheck = ['yes', 'true', 'agree'].includes(answer.toLowerCase());
          if (shouldCheck && !checkbox.checked) {
            console.log(`Content (fillForm): Checking checkbox for '${label}'`);
            checkbox.click();
            checkbox.dispatchEvent(new Event('change', { bubbles: true }));
          }
        } else if (select) {
          console.log(`Content (fillForm): Selecting standard dropdown option '${answer}' for '${label}'`);
          let optionFound = false;
          for (const option of select.options) {
            if (option.text.toLowerCase().includes(answer.toLowerCase()) ||
              answer.toLowerCase().includes(option.text.toLowerCase()) ||
              option.value.toLowerCase() === answer.toLowerCase()) {
              select.value = option.value;
              select.dispatchEvent(new Event('change', { bubbles: true }));
              console.log(`Content (fillForm): ✓ Selected option: '${option.text}'`);
              optionFound = true;
              break;
            }
          }
          if (!optionFound) {
            console.warn(`Content (fillForm): ⚠️ No matching option found in standard select for '${label}'. Answer: '${answer}'`);
          }
        } else if (customDropdownButton) {
          console.log(`Content (fillForm): Found LinkedIn custom dropdown for '${label}'. Attempting to select '${answer}'`);
          await fillCustomDropdown(qElement, customDropdownButton, answer, label);
        } else {
          console.warn(`Content (fillForm): ⚠️ No input element found for question: '${label}'`);
        }
      } else {
        console.warn(`Content (fillForm): No matching answer found for question: '${label}'`);
      }
    }
  }
  await new Promise(resolve => setTimeout(resolve, 500));
}

async function fillCustomDropdown(qElement, dropdownButton, answer, label) {
  try {
    console.log(`Content (fillCustomDropdown): Opening dropdown for '${label}'`);

    // Click the dropdown button to open it
    dropdownButton.click();

    // Wait for dropdown menu to appear
    await new Promise(resolve => setTimeout(resolve, 500));

    // Try multiple selectors to find the dropdown options
    const optionSelectors = [
      'ul[role="listbox"] li',
      'div[role="listbox"] div[role="option"]',
      'ul.artdeco-dropdown__content-inner li',
      '.artdeco-dropdown__item',
      'select[data-test-text-entity-list-form-select] option'
    ];

    let options = [];
    for (const selector of optionSelectors) {
      // Look for options either in the qElement or in the document (dropdown might be portaled)
      options = Array.from(qElement.querySelectorAll(selector));
      if (options.length === 0) {
        options = Array.from(document.querySelectorAll(selector));
      }
      if (options.length > 0) {
        console.log(`Content (fillCustomDropdown): Found ${options.length} options using selector: ${selector}`);
        break;
      }
    }

    if (options.length === 0) {
      console.error(`Content (fillCustomDropdown): ⚠️ No dropdown options found for '${label}'`);
      // Try to close dropdown if we opened it
      dropdownButton.click();
      return;
    }

    console.log(`Content (fillCustomDropdown): Searching for option matching '${answer}' in ${options.length} options`);

    // Find matching option (fuzzy match)
    const normalizedAnswer = answer.toLowerCase().trim();
    let matchedOption = null;

    for (const option of options) {
      const optionText = (option.innerText || option.textContent || '').toLowerCase().trim();
      console.log(`Content (fillCustomDropdown):   - Checking option: '${optionText}'`);

      // Try exact match, contains match, or partial match
      if (optionText === normalizedAnswer ||
        optionText.includes(normalizedAnswer) ||
        normalizedAnswer.includes(optionText)) {
        matchedOption = option;
        console.log(`Content (fillCustomDropdown): ✓ Found matching option: '${optionText}'`);
        break;
      }
    }

    if (matchedOption) {
      console.log(`Content (fillCustomDropdown): Clicking matched option`);
      matchedOption.click();

      // Dispatch change event on the original select element if it exists
      const selectElement = qElement.querySelector('select');
      if (selectElement) {
        selectElement.dispatchEvent(new Event('change', { bubbles: true }));
      }

      await new Promise(resolve => setTimeout(resolve, 300));
    } else {
      console.warn(`Content (fillCustomDropdown): ⚠️ No matching option found for '${label}'. Answer: '${answer}'`);
      console.log(`Content (fillCustomDropdown): Available options were:`, options.map(o => o.innerText || o.textContent).join(', '));

      // Close dropdown since we didn't find a match
      dropdownButton.click();
    }
  } catch (error) {
    console.error(`Content (fillCustomDropdown): Error filling custom dropdown for '${label}':`, error);
  }
}

// Detect validation errors in the application modal
function detectValidationErrors() {
  console.log("Content (detectValidationErrors): Checking for validation errors.");

  // Look for validation error messages
  const errorMessages = Array.from(document.querySelectorAll('.artdeco-inline-feedback--error, .fb-form-element-label__error'));
  const errorText = Array.from(document.querySelectorAll('*')).filter(el =>
    el.textContent.includes('Please enter a valid answer') ||
    el.textContent.includes('Please enter an answer') ||
    el.textContent.includes('This field is required') ||
    el.textContent.includes('Please make a selection')
  );

  if (errorMessages.length === 0 && errorText.length === 0) {
    console.log("Content (detectValidationErrors): No validation errors found.");
    return [];
  }

  console.log(`Content (detectValidationErrors): Found ${errorMessages.length + errorText.length} validation error indicator(s).`);

  // Find form elements with errors
  const fieldsWithErrors = [];
  const formElementSelectors = '.fb-dash-form-element, .fb-form-element, .jobs-easy-apply-form-section__grouping, .jobs-easy-apply-form-element';
  const questionElements = document.querySelectorAll(formElementSelectors);

  questionElements.forEach(qElement => {
    // Check if this element has error indicators
    const hasError = qElement.querySelector('.artdeco-inline-feedback--error') ||
      qElement.querySelector('.fb-form-element-label__error') ||
      qElement.classList.contains('artdeco-text-input--error') ||
      Array.from(qElement.querySelectorAll('*')).some(el =>
        el.textContent.includes('Please enter a valid answer') ||
        el.textContent.includes('Please enter an answer')
      );

    if (hasError) {
      const label = qElement.querySelector('label')?.innerText.trim() ||
        qElement.querySelector('.fb-form-element-label')?.innerText.trim();
      console.log(`Content (detectValidationErrors): Field with error found: "${label}"`);
      fieldsWithErrors.push({ element: qElement, label: label });
    }
  });

  console.log(`Content (detectValidationErrors): Total fields with errors: ${fieldsWithErrors.length}`);
  return fieldsWithErrors;
}

// Handle validation errors by re-filling problematic fields
async function handleValidationErrors(fieldsWithErrors) {
  console.log(`Content (handleValidationErrors): Attempting to fix ${fieldsWithErrors.length} field(s) with errors.`);

  for (const field of fieldsWithErrors) {
    const qElement = field.element;
    const label = field.label;

    console.log(`Content (handleValidationErrors): Processing field: "${label}"`);

    // Check for different input types
    const select = qElement.querySelector('select');
    const customDropdownButton = qElement.querySelector('select[data-test-text-entity-list-form-select]') ||
      qElement.querySelector('button[aria-haspopup="listbox"]') ||
      qElement.querySelector('button[role="combobox"]') ||
      qElement.querySelector('.artdeco-dropdown__trigger');
    const radioButtons = qElement.querySelectorAll('input[type="radio"]');
    const textInput = qElement.querySelector('input[type="text"], input[type="number"], textarea');

    // For select/dropdown fields, try to select the first valid option
    if (select && !customDropdownButton) {
      console.log(`Content (handleValidationErrors): Found standard select for "${label}". Selecting first valid option.`);
      // Skip placeholder options like "Select an option"
      for (let i = 0; i < select.options.length; i++) {
        const option = select.options[i];
        if (option.value && option.value !== '' && !option.disabled) {
          select.value = option.value;
          select.dispatchEvent(new Event('change', { bubbles: true }));
          console.log(`Content (handleValidationErrors): ✓ Selected "${option.text}"`);
          break;
        }
      }
    } else if (customDropdownButton) {
      console.log(`Content (handleValidationErrors): Found custom dropdown for "${label}". Attempting to select first valid option.`);
      await fillCustomDropdownFirstValid(qElement, customDropdownButton, label);
    } else if (radioButtons.length > 0) {
      console.log(`Content (handleValidationErrors): Found radio buttons for "${label}". Selecting first option.`);
      if (radioButtons[0]) {
        radioButtons[0].click();
        radioButtons[0].dispatchEvent(new Event('change', { bubbles: true }));
        console.log(`Content (handleValidationErrors): ✓ Selected first radio option`);
      }
    } else if (textInput) {
      console.log(`Content (handleValidationErrors): Found text input for "${label}". Current value: "${textInput.value}"`);
      // For numeric fields, try putting 1 or 0
      if (textInput.type === 'number' || label.toLowerCase().includes('years') || label.toLowerCase().includes('how many')) {
        textInput.value = '1';
      } else {
        textInput.value = 'Yes'; // Common fallback for text questions
      }
      textInput.dispatchEvent(new Event('input', { bubbles: true }));
      textInput.dispatchEvent(new Event('change', { bubbles: true }));
      textInput.dispatchEvent(new Event('blur', { bubbles: true }));
      console.log(`Content (handleValidationErrors): ✓ Set fallback value "${textInput.value}"`);
    }
  }

  await new Promise(resolve => setTimeout(resolve, 800));
  console.log("Content (handleValidationErrors): Finished fixing validation errors.");
}

// Fill custom dropdown with first valid option
async function fillCustomDropdownFirstValid(qElement, dropdownButton, label) {
  try {
    console.log(`Content (fillCustomDropdownFirstValid): Opening dropdown for "${label}"`);
    dropdownButton.click();
    await new Promise(resolve => setTimeout(resolve, 500));

    const optionSelectors = [
      'ul[role="listbox"] li',
      'div[role="listbox"] div[role="option"]',
      'ul.artdeco-dropdown__content-inner li',
      '.artdeco-dropdown__item',
      'select[data-test-text-entity-list-form-select] option'
    ];

    let options = [];
    for (const selector of optionSelectors) {
      options = Array.from(qElement.querySelectorAll(selector));
      if (options.length === 0) {
        options = Array.from(document.querySelectorAll(selector));
      }
      if (options.length > 0) {
        console.log(`Content (fillCustomDropdownFirstValid): Found ${options.length} options`);
        break;
      }
    }

    if (options.length > 0) {
      // Find first valid option (skip placeholders)
      for (const option of options) {
        const optionText = (option.innerText || option.textContent || '').trim();
        // Skip empty or placeholder options
        if (optionText &&
          !optionText.toLowerCase().includes('select') &&
          !optionText.toLowerCase().includes('choose') &&
          optionText !== '--') {
          console.log(`Content (fillCustomDropdownFirstValid): Selecting "${optionText}"`);
          option.click();
          await new Promise(resolve => setTimeout(resolve, 300));
          return;
        }
      }
    }

    // Close dropdown if no valid option found
    dropdownButton.click();
    console.log(`Content (fillCustomDropdownFirstValid): No valid option found, dropdown closed.`);
  } catch (error) {
    console.error(`Content (fillCustomDropdownFirstValid): Error:`, error);
  }
}

async function clickNextOrSubmit() {
  const submitButton = document.querySelector('button[aria-label="Submit application"]');
  const reviewButton = document.querySelector('button[aria-label="Review your application"]');
  const nextButton = document.querySelector('button[aria-label="Continue to next step"]');

  // Check for "Done" button in success modal
  const doneButton = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Done') ||
    Array.from(document.querySelectorAll('button span')).find(s => s.innerText.trim() === 'Done')?.closest('button') ||
    document.querySelector('button[aria-label="Dismiss"]');

  if (submitButton) {
    console.log("Content (clickNextOrSubmit): Clicking 'Submit' button.");
    stepRetryCount = 0; // Reset on successful submission
    submitButton.click();

    // Wait for validation to run, then check for errors
    await new Promise(resolve => setTimeout(resolve, 800));
    const fieldsWithErrors = detectValidationErrors();

    if (fieldsWithErrors.length > 0) {
      console.warn(`Content (clickNextOrSubmit): Validation errors detected after clicking Submit. Retry count: ${validationRetryCount}`);

      if (validationRetryCount < MAX_VALIDATION_RETRIES) {
        validationRetryCount++;
        await handleValidationErrors(fieldsWithErrors);
        // Retry clicking submit
        console.log("Content (clickNextOrSubmit): Retrying Submit after fixing errors.");
        await clickNextOrSubmit();
        return;
      } else {
        console.error("Content (clickNextOrSubmit): Max validation retries reached. Skipping this job.");
        validationRetryCount = 0;
        chrome.runtime.sendMessage({ action: "autoApplyError", message: "Unable to fix validation errors after multiple attempts." });
        return;
      }
    }

    validationRetryCount = 0; // Reset on success
    // Wait for the success modal to appear before sending submitted
    setTimeout(() => {
      chrome.runtime.sendMessage({ action: "applicationSubmitted" });
    }, 2000);
  } else if (reviewButton) {
    console.log("Content (clickNextOrSubmit): Clicking 'Review' button.");
    stepRetryCount = 0; // Reset on progression
    reviewButton.click();

    // Wait for validation to run, then check for errors
    await new Promise(resolve => setTimeout(resolve, 800));
    const fieldsWithErrors = detectValidationErrors();

    if (fieldsWithErrors.length > 0) {
      console.warn(`Content (clickNextOrSubmit): Validation errors detected after clicking Review. Retry count: ${validationRetryCount}`);

      if (validationRetryCount < MAX_VALIDATION_RETRIES) {
        validationRetryCount++;
        await handleValidationErrors(fieldsWithErrors);
        // Retry clicking review
        console.log("Content (clickNextOrSubmit): Retrying Review after fixing errors.");
        await clickNextOrSubmit();
        return;
      } else {
        console.error("Content (clickNextOrSubmit): Max validation retries reached. Skipping this job.");
        validationRetryCount = 0;
        chrome.runtime.sendMessage({ action: "autoApplyError", message: "Unable to fix validation errors after multiple attempts." });
        return;
      }
    }

    validationRetryCount = 0; // Reset on success
    chrome.runtime.sendMessage({ action: "applicationStepCompleted" });
  } else if (nextButton) {
    console.log("Content (clickNextOrSubmit): Clicking 'Next' button.");
    // Don't reset counter here - we need to detect if we're stuck on the same step
    nextButton.click();

    // Wait for validation to run, then check for errors
    await new Promise(resolve => setTimeout(resolve, 800));
    const fieldsWithErrors = detectValidationErrors();

    if (fieldsWithErrors.length > 0) {
      console.warn(`Content (clickNextOrSubmit): Validation errors detected after clicking Next. Retry count: ${validationRetryCount}`);

      if (validationRetryCount < MAX_VALIDATION_RETRIES) {
        validationRetryCount++;
        await handleValidationErrors(fieldsWithErrors);
        // Retry clicking next
        console.log("Content (clickNextOrSubmit): Retrying Next after fixing errors.");
        await clickNextOrSubmit();
        return;
      } else {
        console.error("Content (clickNextOrSubmit): Max validation retries reached. Skipping this job.");
        validationRetryCount = 0;
        chrome.runtime.sendMessage({ action: "autoApplyError", message: "Unable to fix validation errors after multiple attempts." });
        return;
      }
    }

    validationRetryCount = 0; // Reset on success
    chrome.runtime.sendMessage({ action: "applicationStepCompleted" });
  } else if (doneButton) {
    console.log("Content (clickNextOrSubmit): Clicking 'Done' button to close modal.");
    stepRetryCount = 0; // Reset on completion
    validationRetryCount = 0; // Reset validation counter
    doneButton.click();
    chrome.runtime.sendMessage({ action: "applicationSubmitted" });
  } else {
    console.error("Content (clickNextOrSubmit): Could not find Next, Review, Submit, or Done button.");

    // Check for success header as a fallback
    if (document.querySelector('.artdeco-modal__header--success')) {
      console.log("Content: Success modal detected (header). Assuming application was submitted.");
      // Try to find the dismiss icon if the button isn't obvious
      const dismissIcon = document.querySelector('button[data-test-modal-close-btn]');
      if (dismissIcon) dismissIcon.click();

      validationRetryCount = 0; // Reset validation counter
      chrome.runtime.sendMessage({ action: "applicationSubmitted" });
    } else {
      chrome.runtime.sendMessage({ action: "autoApplyError", message: "Could not find next step button in modal." });
    }
  }
}