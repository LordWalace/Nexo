import React from 'react';
import { TouchableOpacity, StyleSheet, TouchableOpacityProps, ViewStyle } from 'react-native';
import { Text } from './Text';
import { useThemeStore } from '../stores/themeStore';
import { lightColors, darkColors } from '../theme/colors';

interface ButtonProps extends TouchableOpacityProps {
  title: string;
  color?: string;
  textColor?: string;
  style?: ViewStyle;
}

export const Button: React.FC<ButtonProps> = ({ title, color, textColor = '#FFFFFF', style, ...props }) => {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;
  const bgColor = color || colors.accent;

  return (
    <TouchableOpacity 
      style={[
        styles.button,
        { backgroundColor: bgColor },
        props.disabled && { opacity: 0.5 },
        style
      ]} 
      {...props}
    >
      <Text variant="body" style={{ color: textColor, fontWeight: 'bold' }}>{title}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 9999, // Botões completamente arredondados
    alignItems: 'center',
    justifyContent: 'center',
  }
});
