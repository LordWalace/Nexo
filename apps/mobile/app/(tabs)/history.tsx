import React from 'react';
import { View, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { useDataStore } from '../../src/stores/useDataStore';
import { useThemeStore } from '../../src/stores/themeStore';
import { lightColors, darkColors } from '../../src/theme/colors';
import { Text } from '../../src/components/Text';

export default function HistoryList() {
  const router = useRouter();
  const { activities } = useDataStore();
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  const deletedActivities = activities.filter(a => a.deleted).reverse();

  return (
    <View style={[styles.container, { backgroundColor: 'transparent' }]}>
      <Text variant="body" style={{ marginBottom: 16, color: colors.textSecondary }}>
        Aqui estão as atividades excluídas. Você pode selecioná-las para visualizar detalhes ou recuperar.
      </Text>
      <FlatList
        data={deletedActivities}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => {
          const durationMins = item.durationMs ? Math.round(item.durationMs / 60000) : 0;
          
          return (
            <TouchableOpacity 
              style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]} 
              onPress={() => router.push(`/history/${item.id}`)}
            >
              <Text variant="h2" style={{ textDecorationLine: 'line-through', opacity: 0.7 }}>
                {item.title}
              </Text>
              {item.startTime && (
                <Text variant="caption" style={{ marginTop: 4, color: colors.textSecondary }}>
                  Planejado: {new Date(item.startTime).toLocaleDateString()}
                </Text>
              )}
              <Text variant="caption" style={{ color: colors.textSecondary }}>
                Dura��o: {durationMins} min
              </Text>
            </TouchableOpacity>
          );
        }}
        ListEmptyComponent={<Text style={[styles.empty, { color: colors.textSecondary }]}>Nenhuma atividade excluída encontrada.</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  card: { padding: 16, borderRadius: 8, borderWidth: 1, marginBottom: 8 },
  empty: { textAlign: 'center', marginTop: 32 }
});
