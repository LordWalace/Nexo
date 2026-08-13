import React from 'react';
import { View, StyleSheet, Button, FlatList } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useDataStore } from '../../src/stores/useDataStore';
import { Text } from '../../src/components/Text';
import { colors } from '../../src/theme/colors';

export default function CategoryDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { categories, activities, deleteCategory } = useDataStore();

  const category = categories.find(c => c.id === id);
  const relatedActivities = activities.filter(a => a.categoryId === id);

  if (!category) {
    return <View style={styles.container}><Text>Categoria não encontrada.</Text></View>;
  }

  const handleDelete = () => {
    deleteCategory(category.id);
    router.back();
  };

  return (
    <View style={styles.container}>
      <Text variant="h1" style={styles.title}>{category.name}</Text>
      {category.description && <Text variant="body" style={styles.desc}>{category.description}</Text>}
      
      <Text variant="h2" style={styles.sectionTitle}>Atividades vinculadas:</Text>
      <FlatList
        data={relatedActivities}
        keyExtractor={item => item.id}
        renderItem={({ item }) => <Text style={styles.item}>• {item.title}</Text>}
        ListEmptyComponent={<Text style={styles.empty}>Nenhuma atividade.</Text>}
      />

      <View style={styles.actions}>
        <Button title="Excluir Categoria" color={colors.light.danger} onPress={handleDelete} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: colors.light.background },
  title: { marginBottom: 8 },
  desc: { marginBottom: 16, color: colors.light.textSecondary },
  sectionTitle: { marginTop: 16, marginBottom: 8 },
  item: { marginBottom: 4 },
  empty: { fontStyle: 'italic', color: colors.light.textSecondary },
  actions: { marginTop: 24 }
});
