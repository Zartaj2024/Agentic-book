import React, { useState, useEffect } from 'react';
import AIChatbot from './AIChatbot';
import TextSelectionTooltip from './TextSelectionTooltip';

const AIProvider = ({ children }) => {
  const [selectedText, setSelectedText] = useState(null);

  const handleTextSelection = (text) => {
    setSelectedText(text);
  };

  // When selectedText is set, we might want to interact with the chatbot
  useEffect(() => {
    if (selectedText) {
      // In a full implementation, this might trigger the chatbot to focus
      // or prepare to receive the selected text as input
    }
  }, [selectedText]);

  return (
    <>
      {children}
      <TextSelectionTooltip onSelectText={handleTextSelection} />
      <AIChatbot selectedText={selectedText} onTextSelected={setSelectedText} />
    </>
  );
};

export default AIProvider;