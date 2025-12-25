import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import AIProvider from '../components/AIProvider';

export default function Layout(props) {
  return (
    <AIProvider>
      <OriginalLayout {...props} />
    </AIProvider>
  );
}