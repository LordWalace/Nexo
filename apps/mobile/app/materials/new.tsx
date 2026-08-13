import React, { useState } from 'react';
import { View, StyleSheet, TextInput, Button } from 'react-native';
import { useRouter } from 'expo-router';
import { useDataStore } from '../../src/stores/useDataStore';
import { Text } from '../../src/components/Text';
import { colors } from '../../src/theme/colors';

export default function NewMaterial() {
  const router = useRouter();
  const { addMaterial } = useDataStore();
  
  const [name, setName] = useState('');
  const [type, setType] = useState('');
  const [link, setLink] = useState('');

  const handleSave = () => {
    if (!name.trim() || !type.trim()) return;
    addMaterial({ name, type, link });
    router.back();
  };

  return (
    <View style={styles.container}>
      <Text variant="body" style={styles.label}>Nome (obrigatório)</Text>
      <TextInput style={styles.input} value={name} onChangeText={setName} />

      <Text variant="body" style={styles.label}>Tipo (obrigatório, ex: PDF, Link)</Text>
      <TextInput style={styles.input} value={type} onChangeText={setType} />

      <Text variant="body" style={styles.label}>Link (opcional)</Text>
      <TextInput style={styles.input} value={link} onChangeText={setLink} />

      <View style={{ marginTop: 16 }}>
        <Button title="Salvar" color={colors.light.accent} onPress={handleSave} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: colors.light.background },
  label: { marginBottom: 4, marginTop: 12 },
  input: { backgroundColor: colors.light.surface, padding: 12, borderRadius: 8, borderWidth: 1, borderColor: colors.light.border }
});
