import React, { useState, useEffect, useRef } from 'react';
import './AIChatbot.css';

const AIChatbot = ({ selectedText = null, onTextSelected = null, backendUrl = null }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI tutor for the Physical AI Book. How can I help you with robotics and AI concepts today?", sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState(selectedText || '');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (selectedText) {
      setInputValue(selectedText);
      if (!isOpen) {
        setIsOpen(true);
      }
    }
  }, [selectedText, isOpen]);

  const handleSend = async () => {
    if (inputValue.trim() === '') return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    if (onTextSelected && selectedText) {
      onTextSelected(null);
    }

    let fullUrl = '';

    try {
      const apiUrl = backendUrl ||
                    (typeof window !== 'undefined' && window.chatbotConfig && window.chatbotConfig.API_URL ? window.chatbotConfig.API_URL : null);

      if (apiUrl) {
        fullUrl = apiUrl.endsWith('/api/v1/chat') ? apiUrl : `${apiUrl}/api/v1/chat`;
      } else {
        fullUrl = '/api/v1/chat';
      }

      const response = await fetch(fullUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          session_id: localStorage.getItem('session_id') || null
        })
      });

      if (!response.ok) {
        let errorDetail = '';
        try {
          const errorData = await response.json();
          errorDetail = errorData.detail || errorData.message || JSON.stringify(errorData);
        } catch (e) {
          errorDetail = await response.text();
        }
        throw new Error(`API error: ${response.status} - ${errorDetail}`);
      }

      const data = await response.json();
      const botResponse = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot'
      };
      setMessages(prev => [...prev, botResponse]);

      if (data.session_id) {
        localStorage.setItem('session_id', data.session_id);
      }
    } catch (error) {
      console.error('Chat API error:', error);
      const botResponse = {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error: ${error.message}`,
        sender: 'bot'
      };
      setMessages(prev => [...prev, botResponse]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="ai-chatbot">
      {isOpen ? (
        <div className="ai-chatbot-window">
          <div className="ai-chatbot-header">
            <h4 className="ai-chatbot-title">AI Tutor</h4>
            <button
              className="ai-chatbot-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>
          <div className="ai-chatbot-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender}-message`}
              >
                {message.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="ai-chatbot-input-area">
            <textarea
              className="ai-chatbot-input"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about robotics/AI concepts..."
              rows="2"
            />
            <button
              className="ai-chatbot-send"
              onClick={handleSend}
              disabled={!inputValue.trim()}
            >
              Send
            </button>
          </div>
        </div>
      ) : null}

      <button
        className={`ai-chatbot-button ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 2H4C2.9 2 2.01 2.9 2.01 4L2 22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM9 12H7V10H9V12ZM17 12H15V10H17V12ZM13 12H11V10H13V12Z" fill="white"/>
        </svg>
      </button>
    </div>
  );
};

export default AIChatbot;
