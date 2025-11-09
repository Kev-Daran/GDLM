let conversationId = null;

chrome.runtime.onInstalled.addListener(() => {
  console.log('JobWeaver installed');
  conversationId = generateId();
  chrome.storage.local.set({ conversationId });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'CHECK_CONNECTION') {
    sendResponse({ status: 'ok' });
  }

  // Get the current conversation ID
  if (request.type === 'GET_CONVERSATION_ID') {
    chrome.storage.local.get('conversationId', (data) => {
      if (!data.conversationId) {
        const newId = generateId();
        chrome.storage.local.set({ conversationId: newId });
        sendResponse({ conversationId: newId });
      } else {
        sendResponse({ conversationId: data.conversationId });
      }
    });
    return true; // keep message channel open for async response
  }

  // Reset the conversation (optional)
  if (request.type === 'RESET_CONVERSATION') {
    const newId = generateId();
    chrome.storage.local.set({ conversationId: newId });
    sendResponse({ conversationId: newId });
  }

  return true;
});

function generateId() {
  return 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}
