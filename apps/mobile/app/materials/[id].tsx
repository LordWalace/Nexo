import React from 'react';
import { View, StyleSheet, Button } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useDataStore } from '../../src/stores/useDataStore';
import { Text } from '../../src/components/Text';
import { colors } from '../../src/theme/colors';

export default function MaterialDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { materials, deleteMaterial } = useDataStore();

  const material = materials.find(m => m.id === id);

  if (!material) {
    return <View style={styles.container}><Text>Material não encontrado.</Text></View>;
  }

  const handleDelete = () => {
    deleteMaterial(material.id);
    router.back();
  };

  return (
    <View style={styles.container}>
      <Text variant="h1" style={styles.title}>{material.name}</Text>
      <Text variant="body">Tipo: {material.type}</Text>
      {material.link && <Text variant="body">Link: {material.link}</Text>}

      <View style={styles.actions}>
        <Button title="Excluir Material" color={colors.light.danger} onPress={handleDelete} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: colors.light.background },
  title: { marginBottom: 8 },
  actions: { marginTop: 24 }
});
