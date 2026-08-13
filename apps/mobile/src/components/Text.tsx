import React from 'react';
import { Text as RNText, TextProps as RNTextProps, StyleSheet } from 'react-native';
import { useThemeStore } from '../stores/themeStore';
import { lightColors, darkColors } from '../theme/colors';

export interface TextProps extends RNTextProps {
  variant?: 'h1' | 'h2' | 'body' | 'caption';
  color?: string;
}

export const Text: React.FC<TextProps> = ({ style, variant = 'body', color, children, ...props }) => {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  return (
    <RNText 
      style={[
        styles.default,
        { color: colors.text },
        styles[variant],
        color && { color },
        style
      ]} 
      {...props}
    >
      {children}
    </RNText>
  );
};

const styles = StyleSheet.create({
  default: {
    fontFamily: 'System', // Ensures correct UTF-8 and accents rendering natively
  },
  h1: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  h2: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  body: {
    fontSize: 16,
  },
  caption: {
    fontSize: 12,
  }
});
