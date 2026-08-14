import React from 'react';
import { Modal, View, TouchableOpacity, StyleSheet, TouchableWithoutFeedback } from 'react-native';
import { useThemeStore } from '../stores/themeStore';
import { lightColors, darkColors } from '../theme/colors';
import { Text } from './Text';

interface ActionSheetProps {
  visible: boolean;
  onClose: () => void;
  title?: string;
  options: { label: string; onPress: () => void; destructive?: boolean }[];
}

export const ActionSheet: React.FC<ActionSheetProps> = ({ visible, onClose, title, options }) => {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  return (
    <Modal visible={visible} transparent animationType="slide" onRequestClose={onClose}>
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={styles.overlay}>
          <TouchableWithoutFeedback>
            <View style={[styles.sheet, { backgroundColor: colors.surface }]}>
              {title && (
                <Text variant="body" style={[styles.title, { color: colors.textSecondary }]}>{title}</Text>
              )}
              {options.map((opt, i) => (
                <TouchableOpacity 
                  key={i} 
                  style={[styles.option, { borderBottomColor: colors.border, borderBottomWidth: i === options.length - 1 ? 0 : 1 }]} 
                  onPress={() => {
                    onClose();
                    opt.onPress();
                  }}
                >
                  <Text variant="h2" style={{ color: opt.destructive ? colors.danger : colors.text, textAlign: 'center' }}>
                    {opt.label}
                  </Text>
                </TouchableOpacity>
              ))}
              <View style={[styles.cancelContainer, { backgroundColor: colors.background }]}>
                 <TouchableOpacity style={styles.option} onPress={onClose}>
                   <Text variant="h2" style={{ color: colors.textSecondary, textAlign: 'center' }}>Cancelar</Text>
                 </TouchableOpacity>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  sheet: { borderTopLeftRadius: 24, borderTopRightRadius: 24, padding: 16, paddingBottom: 32 },
  title: { textAlign: 'center', marginBottom: 16 },
  option: { paddingVertical: 16 },
  cancelContainer: { marginTop: 16, borderRadius: 16 }
});
