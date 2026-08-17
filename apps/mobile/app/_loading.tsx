import React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { LogoGeometry } from '../src/components/LogoGeometry';
import { useThemeStore } from '../src/stores/themeStore';
import { lightColors, darkColors } from '../src/theme/colors';

export default function LoadingScreen() {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <LogoGeometry size={120} color={colors.accent} animated={true} />
      <Text style={[styles.text, { color: colors.textSecondary }]}>
        Carregando...
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    marginTop: 24,
    fontSize: 16,
    fontFamily: 'sans-serif-medium',
  },
});
