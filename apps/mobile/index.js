import '@expo/metro-runtime';
import { ExpoRoot } from 'expo-router';
import { renderRootComponent } from 'expo-router/build/renderRootComponent';

const ctx = require.context('./app', true, /.*/);

export function App() {
  return <ExpoRoot context={ctx} />;
}

renderRootComponent(App);
