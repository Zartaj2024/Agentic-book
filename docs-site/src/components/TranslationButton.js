import React, { useState, useEffect } from 'react';
import './TranslationButton.css'; // We'll create this CSS file

const TranslationButton = ({ chapterId = 'default', backendUrl = null }) => {
  const [isTranslated, setIsTranslated] = useState(false);
  const [originalContent, setOriginalContent] = useState('');
  const [translatedContent, setTranslatedContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get original content from the DOM when component mounts
  useEffect(() => {
    const contentElement = document.querySelector('.theme-doc-markdown');
    if (contentElement) {
      // Store the original HTML content
      setOriginalContent(contentElement.innerHTML);
    }
  }, []);

  const translateText = async (text) => {
    setIsLoading(true);
    setError(null);

    try {
      // Call the backend API - priority: props > window config > fallback
      const apiUrl = backendUrl ||
                    (typeof window !== 'undefined' && window.chatbotConfig ? window.chatbotConfig.API_URL : null) ||
                    'http://localhost:8000';

      // Ensure the URL has the correct path
      const fullUrl = apiUrl.endsWith('/api/v1/translate') ? apiUrl : `${apiUrl}/api/v1/translate`;

      const response = await fetch(fullUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          target_language: 'ur',
          source_language: 'en'
        })
      });

      if (!response.ok) {
        throw new Error(`Translation API error: ${response.status}`);
      }

      const data = await response.json();
      return data.translated_text;
    } catch (err) {
      console.error('Translation error:', err);
      setError(err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const handleTranslate = async () => {
    if (isTranslated) {
      // Switch back to original content
      const contentElement = document.querySelector('.theme-doc-markdown');
      if (contentElement && originalContent) {
        contentElement.innerHTML = originalContent;
      }
      setIsTranslated(false);
      return;
    }

    try {
      // Get the content to translate
      const contentElement = document.querySelector('.theme-doc-markdown');
      if (!contentElement) {
        setError('No content found to translate');
        return;
      }

      // Get the text content to send for translation (excluding any existing buttons)
      const textToTranslate = contentElement.innerText || contentElement.textContent || '';

      if (!textToTranslate.trim()) {
        setError('No content found to translate');
        return;
      }

      // Perform translation
      const translated = await translateText(textToTranslate);
      setTranslatedContent(translated);

      // Update the DOM with translated content
      contentElement.innerHTML = `<div class="urdu-content translated-content">${translated}</div>`;
      setIsTranslated(true);
    } catch (err) {
      console.error('Translation failed:', err);
    }
  };

  const getButtonText = () => {
    if (isLoading) {
      return 'Translating...';
    }
    return isTranslated ? 'Show in English' : 'Translate to Urdu';
  };

  const getButtonIcon = () => {
    if (isLoading) {
      return (
        <svg className="translation-spinner" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M12 2V6" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M12 18V22" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M4.93 4.93L7.76 7.76" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M16.24 16.24L19.07 19.07" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M2 12H6" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M18 12H22" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M4.93 19.07L7.76 16.24" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M16.24 7.76L19.07 4.93" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
        </svg>
      );
    }

    return (
      <svg className="translation-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
        <path d="M12.8 19.6L7.4 14.2H12.2C12.6 14.2 13 13.8 13 13.4V10.6C13 10.2 12.6 9.8 12.2 9.8H7.4L12.8 4.4C13.1 4.1 13.1 3.6 12.8 3.3C12.5 3 12 3 11.7 3.3L4.1 10.9C3.9 11.1 3.9 11.5 4.1 11.7L11.7 19.3C12 19.6 12.5 19.6 12.8 19.3V19.6Z" fill="currentColor"/>
        <path d="M19.8 3.3H15.2C14.8 3.3 14.4 3.7 14.4 4.1V6.9C14.4 7.3 14.8 7.7 15.2 7.7H19.8C20.2 7.7 20.6 7.3 20.6 6.9V4.1C20.6 3.7 20.2 3.3 19.8 3.3Z" fill="currentColor"/>
        <path d="M20.6 13.4V16.2C20.6 16.6 20.2 17 19.8 17H15.2C14.8 17 14.4 16.6 14.4 16.2V13.4C14.4 13 14.8 12.6 15.2 12.6H19.8C20.2 12.6 20.6 13 20.6 13.4Z" fill="currentColor"/>
        <path d="M9.7 12.1H14.5C14.9 12.1 15.3 11.7 15.3 11.3V8.5C15.3 8.1 14.9 7.7 14.5 7.7H9.7C9.3 7.7 8.9 8.1 8.9 8.5V11.3C8.9 11.7 9.3 12.1 9.7 12.1Z" fill="currentColor"/>
      </svg>
    );
  };

  return (
    <div className="translation-container">
      <button
        className={`translation-button ${isTranslated ? 'translated' : ''} ${isLoading ? 'loading' : ''}`}
        onClick={handleTranslate}
        disabled={isLoading}
        aria-label={isTranslated ? "Show content in English" : "Translate content to Urdu"}
      >
        {getButtonIcon()}
        <span className="translation-button-text">{getButtonText()}</span>
      </button>

      {error && (
        <div className="translation-error">
          Error: {error}
        </div>
      )}
    </div>
  );
};

export default TranslationButton;