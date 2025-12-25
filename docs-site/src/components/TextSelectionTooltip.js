import React, { useState, useEffect } from 'react';

const TextSelectionTooltip = ({ onSelectText }) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text.length > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setTooltipPosition({
          x: rect.left + window.scrollX,
          y: rect.top + window.scrollY - 40 // Position above the selection
        });

        setSelectedText(text);
        setShowTooltip(true);
      } else {
        setShowTooltip(false);
      }
    };

    const handleClick = () => {
      const selection = window.getSelection();
      if (selection.toString().trim() === '') {
        setShowTooltip(false);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('click', handleClick);
    };
  }, []);

  const handleAskAI = () => {
    if (selectedText) {
      onSelectText(selectedText);
      setShowTooltip(false);
    }
  };

  if (!showTooltip || !selectedText) {
    return null;
  }

  return (
    <div
      className="text-selection-tooltip"
      style={{
        position: 'absolute',
        left: `${tooltipPosition.x}px`,
        top: `${tooltipPosition.y}px`,
        zIndex: 10000,
      }}
    >
      <button
        onClick={handleAskAI}
        style={{
          background: '#2e8555',
          color: 'white',
          border: 'none',
          padding: '6px 12px',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '14px',
          fontWeight: 'bold',
        }}
      >
        Ask AI
      </button>
      <div
        style={{
          position: 'absolute',
          bottom: '-10px',
          left: '50%',
          transform: 'translateX(-50%)',
          width: 0,
          height: 0,
          borderLeft: '5px solid transparent',
          borderRight: '5px solid transparent',
          borderTop: '10px solid #2e8555',
        }}
      />
    </div>
  );
};

export default TextSelectionTooltip;