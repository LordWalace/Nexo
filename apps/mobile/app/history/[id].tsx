import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useDataStore } from '../../src/stores/useDataStore';
import { useThemeStore } from '../../src/stores/themeStore';
import { lightColors, darkColors } from '../../src/theme/colors';
import { Text } from '../../src/components/Text';
import { Button } from '../../src/components/Button';
import { CustomAlert, AlertButton } from '../../src/components/CustomAlert';

export default function HistoryDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { activities, recoverActivity } = useDataStore();
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  const [alertConfig, setAlertConfig] = useState<{ visible: boolean, title: string, message: string, buttons: AlertButton[] }>({
    visible: false,
    title: '',
    message: '',
    buttons: []
  });

  const activity = activities.find(a => a.id === id);

  if (!activity || !activity.deleted) {
    return <View style={[styles.container, { backgroundColor: colors.background }]}><Text>Atividade excluída não encontrada.</Text></View>;
  }

  const handleRecover = () => {
    const isOverdue = activity.endTime && new Date(activity.endTime).getTime() < Date.now();

    if (isOverdue) {
      setAlertConfig({
        visible: true,
        title: 'Tarefa Expirada',
        message: 'Esta tarefa já passou do horário. Você será redirecionado para alterar a data/horário antes de recuperá-la.',
        buttons: [
          { text: 'Cancelar', style: 'cancel' },
          { 
            text: 'Editar e Recuperar', 
            onPress: () => router.push(`/activities/${activity.id}/edit?recover=true`)
          }
        ]
      });
    } else {
      setAlertConfig({
        visible: true,
        title: 'Recuperar Atividade',
        message: 'Deseja restaurar esta atividade para a lista principal?',
        buttons: [
          { text: 'Cancelar', style: 'cancel' },
          { 
            text: 'Restaurar', 
            onPress: () => {
              recoverActivity(activity.id);
              router.back();
            }
          }
        ]
      });
    }
  };

  const durationMins = activity.durationMs ? Math.round(activity.durationMs / 60000) : 0;

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
        <Text variant="h1" style={styles.row}>{activity.title}</Text>
        {activity.description && <Text variant="body" style={styles.row}>{activity.description}</Text>}
        {activity.startTime && <Text variant="body" style={styles.row}>Início Planejado: {new Date(activity.startTime).toLocaleString('pt-BR')}</Text>}
        {activity.endTime && <Text variant="body" style={styles.row}>Fim Planejado: {new Date(activity.endTime).toLocaleString('pt-BR')}</Text>}
        <Text variant="body" style={styles.row}>Duração Total: {durationMins} minutos</Text>
      </View>

      <View style={styles.actions}>
        <Button title="Recuperar Tarefa" color={colors.accent} onPress={handleRecover} />
      </View>
      
      <CustomAlert 
        visible={alertConfig.visible}
        title={alertConfig.title}
        message={alertConfig.message}
        buttons={alertConfig.buttons}
        onDismiss={() => setAlertConfig(prev => ({ ...prev, visible: false }))}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  card: { padding: 16, borderRadius: 8, borderWidth: 1, marginBottom: 24 },
  row: { marginBottom: 8 },
  actions: { marginTop: 'auto', marginBottom: 24 }
});
