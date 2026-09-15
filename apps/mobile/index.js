import '@expo/metro-runtime';
import { ExpoRoot } from 'expo-router';
import { renderRootComponent } from 'expo-router/build/renderRootComponent';
import React from 'react';

// Only load React component files (.js, .jsx, .ts, .tsx) to avoid crashing Expo Router with non-component files.
const ctx = require.context('./app', true, /\.(js|jsx|ts|tsx)$/);

export default function App() {
  return <ExpoRoot context={ctx} />;
}

renderRootComponent(App);
