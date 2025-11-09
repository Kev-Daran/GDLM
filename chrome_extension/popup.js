function generateId() {
  return 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

const API_URL = CONFIG.API_URL;
let conversationId = generateId();

document.addEventListener('DOMContentLoaded', () => {
  const userInput = document.getElementById('userInput');
  const sendBtn = document.getElementById('sendBtn');
  const messages = document.getElementById('messages');
  const uploadBtn = document.getElementById('uploadBtn');
  const resumeUpload = document.getElementById('resumeUpload');
  const quickBtns = document.querySelectorAll('.quick-btn');
  const statusText = document.getElementById('statusText');
  const connectionStatus = document.getElementById('connectionStatus');

  // Check connection on load
  checkConnection();

  // Event Listeners
  sendBtn.addEventListener('click', () => handleSend());
  userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });

  uploadBtn.addEventListener('click', () => resumeUpload.click());
  resumeUpload.addEventListener('change', handleResumeUpload);

  quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      userInput.value = btn.dataset.message;
      handleSend();
    });
  });

  // Functions
  async function checkConnection() {
    try {
      const response = await fetch(`${API_URL}/api/health`);
      if (response.ok) {
        updateStatus('connected', 'Connected');
      } else {
        updateStatus('error', 'Connection Error');
      }
    } catch (error) {
      updateStatus('error', 'Offline');
    }
  }

  function updateStatus(status, text) {
    connectionStatus.className = `status-indicator ${status}`;
    statusText.textContent = text;
  }

  async function handleSend() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';
    
    const loadingId = addMessage('Thinking...', 'agent', true);
    
    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: message,
          conversation_id: conversationId
        })
      });

      const data = await response.json();
      
      removeMessage(loadingId);
      
      if (data.status === 'success') {
        addMessage(data.response, 'agent');
        updateAgentInfo(data.response);
      } else {
        addMessage('Error: ' + (data.detail || 'Unknown error'), 'error');
      }
    } catch (error) {
      removeMessage(loadingId);
      addMessage('⚠️ Connection error. Please check if the backend is running.', 'error');
      updateStatus('error', 'Connection Lost');
    }
  }

  async function handleResumeUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.pdf')) {
      addMessage('Please upload a PDF file', 'error');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const loadingId = addMessage('Uploading resume...', 'agent', true);

    try {
      const response = await fetch(`${API_URL}/api/upload-resume`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      removeMessage(loadingId);

      if (data.status === 'success') {
        addMessage('✅ Resume uploaded successfully!', 'success');
      } else {
        addMessage('❌ Upload failed: ' + data.message, 'error');
      }
    } catch (error) {
      removeMessage(loadingId);
      addMessage('❌ Upload error. Please try again.', 'error');
    }

    resumeUpload.value = '';
  }

function addMessage(text, type, isLoading = false) {
  const msgId = generateId();
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${type}`;
  msgDiv.id = msgId;

  if (isLoading) {
    msgDiv.innerHTML = `${text}`;
  } else {
    const jsonMatch = text.match(/```(?:json)?([\s\S]*?)```/i);

    if (jsonMatch) {
      // Handle JSON data (like LinkedIn search)
      try {
        const parsed = JSON.parse(jsonMatch[1].trim());
        if (Array.isArray(parsed)) {
          msgDiv.innerHTML = `
            <h4>Found Professionals</h4>
            ${parsed.map(person => `
              <div class="profile-card">
                <p><strong>${person.name}</strong> — ${person.title}</p>
                <p>${person.location}</p>
                ${person.skills && person.skills.length > 0 
                  ? `<p><strong>Skills:</strong> ${person.skills.join(', ')}</p>` 
                  : ''}
                <a href="${person.linkedin_url}" target="_blank">LinkedIn Profile</a>
              </div>
            `).join('')}
          `;
        } else {
          msgDiv.innerHTML = `<pre>${JSON.stringify(parsed, null, 2)}</pre>`;
        }
      } catch (err) {
        msgDiv.textContent = text;
      }

    } else {
      // Handle formatted markdown-like text
      let formatted = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>')              // italics
        .replace(/(\n|\r)+/g, '<br>')                      // newlines
        .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>'); // links

      msgDiv.innerHTML = formatted;
    }
  }

  messages.appendChild(msgDiv);
  messages.scrollTop = messages.scrollHeight;
  return msgId;
}



  function removeMessage(id) {
    const msg = document.getElementById(id);
    if (msg) msg.remove();
  }

  function updateAgentInfo(response) {
    const agentInfo = document.getElementById('currentAgent');
    if (response.toLowerCase().includes('resume')) {
      agentInfo.textContent = 'Resume Support Agent';
    } else if (response.toLowerCase().includes('search') || response.toLowerCase().includes('linkedin')) {
      agentInfo.textContent = 'Searcher Agent';
    } else {
      agentInfo.textContent = 'Root Agent';
    }
  }


});