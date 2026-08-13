import React from 'react';
import { View, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { useDataStore } from '../../src/stores/useDataStore';
import { useThemeStore } from '../../src/stores/themeStore';
import { lightColors, darkColors } from '../../src/theme/colors';
import { Text } from '../../src/components/Text';
import { Button } from '../../src/components/Button';

export default function MaterialsList() {
  const router = useRouter();
  const { materials } = useDataStore();
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <FlatList
        data={materials}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity 
            style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]} 
            onPress={() => router.push(`/materials/${item.id}`)}
          >
            <Text variant="h2">{item.name}</Text>
            <Text variant="caption">{item.type}</Text>
          </TouchableOpacity>
        )}
        ListEmptyComponent={<Text style={[styles.empty, { color: colors.textSecondary }]}>Nenhum material encontrado.</Text>}
      />
      <Button title="Novo Material" color={colors.accent} onPress={() => router.push('/materials/new')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  card: { padding: 16, borderRadius: 8, borderWidth: 1, marginBottom: 8 },
  empty: { textAlign: 'center', marginTop: 32, marginBottom: 32 }
});
