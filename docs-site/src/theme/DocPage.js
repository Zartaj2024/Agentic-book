import React from 'react';
import OriginalDocPage from '@theme-original/DocPage';
import TranslationButton from '../components/TranslationButton';

export default function DocPage(props) {
  return (
    <div>
      <div style={{ marginBottom: '1rem' }}>
        <TranslationButton
          chapterId={props.content?.metadata?.unversionedId || 'default'}
        />
      </div>
      <OriginalDocPage {...props} />
    </div>
  );
}