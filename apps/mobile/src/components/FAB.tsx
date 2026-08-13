import React, { useState } from 'react';
import { View, TouchableOpacity, StyleSheet } from 'react-native';
import { useThemeStore } from '../stores/themeStore';
import { lightColors, darkColors } from '../theme/colors';
import { Text } from './Text';

interface FABProps {
  onActionPress: () => void;
  actionText?: string;
}

export const FAB: React.FC<FABProps> = ({ onActionPress, actionText = 'Criar nova tarefa' }) => {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;
  const [isOpen, setIsOpen] = useState(false);

  return (
    <View style={styles.container}>
      {isOpen && (
        <TouchableOpacity 
          style={[styles.actionButton, { backgroundColor: colors.surface, borderColor: colors.border }]} 
          onPress={() => {
            setIsOpen(false);
            onActionPress();
          }}
        >
          <Text variant="body">{actionText}</Text>
        </TouchableOpacity>
      )}
      <TouchableOpacity 
        style={[styles.fab, { backgroundColor: colors.accent }]} 
        onPress={() => setIsOpen(!isOpen)}
      >
        <Text variant="h1" style={{ color: '#FFF' }}>{isOpen ? 'X' : '+'}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    bottom: 120,
    right: 24,
    alignItems: 'flex-end',
  },
  fab: {
    width: 56,
    height: 56,
    borderRadius: 28,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOpacity: 0.3,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
    opacity: 0.85,
  },
  actionButton: {
    marginBottom: 16,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 8,
    borderWidth: 1,
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 1 },
    shadowRadius: 2,
  }
});
