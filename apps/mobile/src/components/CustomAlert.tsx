import React from 'react';
import { Modal, View, StyleSheet, TouchableOpacity } from 'react-native';
import { useThemeStore } from '../stores/themeStore';
import { lightColors, darkColors } from '../theme/colors';
import { Text } from './Text';

export interface AlertButton {
  text: string;
  style?: 'default' | 'cancel' | 'destructive';
  onPress?: () => void;
}

interface CustomAlertProps {
  visible: boolean;
  title: string;
  message?: string;
  buttons: AlertButton[];
  onDismiss?: () => void;
}

export const CustomAlert: React.FC<CustomAlertProps> = ({ visible, title, message, buttons, onDismiss }) => {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  if (!visible) return null;

  return (
    <Modal transparent animationType="fade" visible={visible} onRequestClose={onDismiss}>
      <View style={styles.overlay}>
        <View style={[styles.dialog, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Text variant="h2" style={{ marginBottom: 8, textAlign: 'center' }}>{title}</Text>
          {message && <Text variant="body" style={{ textAlign: 'center', marginBottom: 24, color: colors.textSecondary }}>{message}</Text>}
          
          <View style={[styles.buttonContainer, { borderTopColor: colors.border }]}>
            {buttons.map((btn, index) => {
              let color = colors.primary;
              if (btn.style === 'cancel') color = colors.textSecondary;
              if (btn.style === 'destructive') color = colors.danger;
              
              return (
                <TouchableOpacity 
                  key={index} 
                  style={[styles.button, index > 0 && { borderLeftWidth: 1, borderLeftColor: colors.border }]} 
                  onPress={() => {
                    if (btn.onPress) btn.onPress();
                    if (onDismiss) onDismiss();
                  }}
                >
                  <Text style={{ color, fontWeight: btn.style === 'cancel' ? 'normal' : 'bold', textAlign: 'center' }}>
                    {btn.text}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  dialog: {
    width: '100%',
    maxWidth: 340,
    borderRadius: 16,
    borderWidth: 1,
    paddingTop: 24,
    overflow: 'hidden',
  },
  buttonContainer: {
    flexDirection: 'row',
    borderTopWidth: 1,
  },
  button: {
    flex: 1,
    paddingVertical: 16,
    justifyContent: 'center',
    alignItems: 'center',
  }
});
