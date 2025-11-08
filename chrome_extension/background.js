chrome.runtime.onInstalled.addListener(() => {
  console.log('AI Agent Assistant installed');
});

// Handle messages from popup or content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'CHECK_CONNECTION') {
    // Could add background connection checking here
    sendResponse({ status: 'ok' });
  }
  return true;
});