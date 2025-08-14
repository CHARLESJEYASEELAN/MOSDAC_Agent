// Chatbot JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const chatSidebar = document.getElementById('chatSidebar');
    const chatHistoryContent = document.getElementById('chatHistoryContent');

    let isTyping = false;

    // Handle chat form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        
        if (!message || isTyping) return;
        
        await sendMessage(message);
        messageInput.value = '';
        messageInput.focus();
    });

    // Handle input events
    messageInput.addEventListener('input', function() {
        const hasContent = this.value.trim().length > 0;
        sendButton.disabled = !hasContent || isTyping;
    });

    // Send message function
    async function sendMessage(message) {
        // Add user message to chat
        addMessage(message, 'user');
        
        // Show typing indicator
        showTypingIndicator();
        
        // Disable input
        setInputState(false);
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
            // Simulate typing delay for better UX
            setTimeout(() => {
                hideTypingIndicator();
                addMessage(data.response, 'bot');
                setInputState(true);
            }, 1000 + Math.random() * 1000); // Random delay between 1-2 seconds
            
        } catch (error) {
            console.error('Chat error:', error);
            hideTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again later.', 'bot', true);
            setInputState(true);
        }
    }

    // Add message to chat
    function addMessage(content, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = `${sender}-avatar`;
        
        if (sender === 'bot') {
            avatar.innerHTML = '<i class="fas fa-robot"></i>';
        } else {
            avatar.innerHTML = '<i class="fas fa-user"></i>';
        }
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (isError) {
            messageContent.style.background = '#f8d7da';
            messageContent.style.color = '#721c24';
            messageContent.style.border = '1px solid #f5c6cb';
        }
        
        // Format message content
        messageContent.innerHTML = formatMessage(content);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        scrollToBottom();
        
        // Add animation
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            messageDiv.style.transition = 'all 0.3s ease';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }, 100);
    }

    // Format message content (simple markdown-like formatting)
    function formatMessage(content) {
        // Convert line breaks to <br>
        content = content.replace(/\n/g, '<br>');
        
        // Bold text **text**
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic text *text*
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Simple list detection
        if (content.includes('- ')) {
            const lines = content.split('<br>');
            let formattedContent = '';
            let inList = false;
            
            lines.forEach(line => {
                if (line.trim().startsWith('- ')) {
                    if (!inList) {
                        formattedContent += '<ul>';
                        inList = true;
                    }
                    formattedContent += `<li>${line.trim().substring(2)}</li>`;
                } else {
                    if (inList) {
                        formattedContent += '</ul>';
                        inList = false;
                    }
                    formattedContent += line + '<br>';
                }
            });
            
            if (inList) {
                formattedContent += '</ul>';
            }
            
            content = formattedContent;
        }
        
        return content;
    }

    // Show typing indicator
    function showTypingIndicator() {
        isTyping = true;
        typingIndicator.style.display = 'flex';
        scrollToBottom();
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        isTyping = false;
        typingIndicator.style.display = 'none';
    }

    // Set input state
    function setInputState(enabled) {
        messageInput.disabled = !enabled;
        sendButton.disabled = !enabled || messageInput.value.trim().length === 0;
        
        if (enabled) {
            messageInput.focus();
        }
    }

    // Scroll to bottom of chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Send suggestion
    window.sendSuggestion = function(suggestion) {
        messageInput.value = suggestion;
        messageInput.focus();
        sendMessage(suggestion);
    };

    // Toggle chat history sidebar
    window.toggleHistory = function() {
        chatSidebar.classList.toggle('active');
        if (chatSidebar.classList.contains('active')) {
            loadChatHistory();
        }
    };

    // Load chat history
    async function loadChatHistory() {
        chatHistoryContent.innerHTML = '<div class="loading">Loading history...</div>';
        
        try {
            const response = await fetch('/chat_history');
            const data = await response.json();
            
            if (data.chats && data.chats.length > 0) {
                displayChatHistory(data.chats);
            } else {
                chatHistoryContent.innerHTML = '<p style="text-align: center; color: #7f8c8d; padding: 1rem;">No chat history found.</p>';
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
            chatHistoryContent.innerHTML = '<p style="text-align: center; color: #e74c3c; padding: 1rem;">Error loading history.</p>';
        }
    }

    // Display chat history
    function displayChatHistory(chats) {
        let historyHTML = '';
        
        chats.forEach((chat, index) => {
            const date = new Date(chat.timestamp);
            const timeString = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            const dateString = date.toLocaleDateString();
            
            historyHTML += `
                <div class="history-item" onclick="restoreChat('${chat.user_message}', '${chat.bot_response}')">
                    <div class="history-time">${dateString} ${timeString}</div>
                    <div class="history-preview">${chat.user_message.substring(0, 50)}${chat.user_message.length > 50 ? '...' : ''}</div>
                </div>
            `;
        });
        
        chatHistoryContent.innerHTML = historyHTML;
        
        // Add CSS for history items
        const style = document.createElement('style');
        style.textContent = `
            .history-item {
                padding: 0.75rem;
                border-bottom: 1px solid #e9ecef;
                cursor: pointer;
                transition: background 0.3s ease;
            }
            .history-item:hover {
                background: #f8f9fa;
            }
            .history-time {
                font-size: 0.8rem;
                color: #6c757d;
                margin-bottom: 0.25rem;
            }
            .history-preview {
                font-size: 0.9rem;
                color: #495057;
            }
        `;
        document.head.appendChild(style);
    }

    // Restore chat from history
    window.restoreChat = function(userMessage, botResponse) {
        // Close sidebar
        chatSidebar.classList.remove('active');
        
        // Add messages to chat
        addMessage(userMessage, 'user');
        setTimeout(() => {
            addMessage(botResponse, 'bot');
        }, 500);
    };

    // Clear chat
    window.clearChat = function() {
        if (confirm('Are you sure you want to clear the chat?')) {
            const messages = chatMessages.querySelectorAll('.message');
            messages.forEach(message => {
                if (!message.classList.contains('welcome-message')) {
                    message.remove();
                }
            });
        }
    };

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl + Enter to send message
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            if (messageInput.value.trim() && !isTyping) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to close sidebar
        if (e.key === 'Escape') {
            chatSidebar.classList.remove('active');
        }
        
        // Ctrl + L to clear chat
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            clearChat();
        }
        
        // Ctrl + H to toggle history
        if (e.ctrlKey && e.key === 'h') {
            e.preventDefault();
            toggleHistory();
        }
    });

    // Auto-resize input
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    });

    // Focus input on page load
    messageInput.focus();

    // Add some initial suggestions based on context
    const suggestionChips = document.querySelectorAll('.suggestion-chip');
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', function() {
            const suggestion = this.textContent.trim();
            sendSuggestion(suggestion);
        });
    });

    // Auto-scroll to bottom on window resize
    window.addEventListener('resize', function() {
        setTimeout(scrollToBottom, 100);
    });

    // Connection status monitoring
    let isOnline = navigator.onLine;
    
    window.addEventListener('online', function() {
        isOnline = true;
        updateConnectionStatus();
    });
    
    window.addEventListener('offline', function() {
        isOnline = false;
        updateConnectionStatus();
    });
    
    function updateConnectionStatus() {
        const statusDot = document.querySelector('.status-dot');
        const statusText = statusDot.nextElementSibling;
        
        if (isOnline) {
            statusDot.className = 'status-dot online';
            statusText.textContent = 'Online';
        } else {
            statusDot.className = 'status-dot offline';
            statusText.textContent = 'Offline';
        }
    }

    // Add CSS for offline status
    const offlineStyle = document.createElement('style');
    offlineStyle.textContent = `
        .status-dot.offline {
            background: #e74c3c;
        }
    `;
    document.head.appendChild(offlineStyle);
});

// Service Worker registration for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}
