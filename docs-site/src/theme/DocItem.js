import React from 'react';
import OriginalDocItem from '@theme-original/DocItem';
import TranslationButton from '../components/TranslationButton';

export default function DocItem(props) {
  return (
    <>
      <div style={{ marginBottom: '1rem' }}>
        <TranslationButton 
          chapterId={props.content?.metadata?.unversionedId || 'default'} 
        />
      </div>
      <OriginalDocItem {...props} />
    </>
  );
}