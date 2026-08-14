import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useDataStore } from '../../src/stores/useDataStore';
import { useThemeStore } from '../../src/stores/themeStore';
import { lightColors, darkColors } from '../../src/theme/colors';
import { Text } from '../../src/components/Text';
import { Button } from '../../src/components/Button';
import { Linking } from 'react-native';
import { CustomAlert, AlertButton } from '../../src/components/CustomAlert';

const LinkedText = ({ text, style }: { text: string, style?: any }) => {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;
  
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const parts = text.split(urlRegex);
  
  return (
    <Text variant="body" style={style}>
      {parts.map((part, i) => {
        if (part.match(urlRegex)) {
          return (
            <Text 
              key={i} 
              style={{ color: colors.primary, textDecorationLine: 'underline' }}
              onPress={() => Linking.openURL(part)}
            >
              {part}
            </Text>
          );
        }
        return <Text key={i}>{part}</Text>;
      })}
    </Text>
  );
};

export default function ActivityDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { activities, deleteActivity } = useDataStore();
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  const [alertConfig, setAlertConfig] = useState<{ visible: boolean, title: string, message: string, buttons: AlertButton[] }>({
    visible: false,
    title: '',
    message: '',
    buttons: []
  });

  const activity = activities.find(a => a.id === id);

  if (!activity || activity.deleted) {
    return <View style={[styles.container, { backgroundColor: 'transparent' }]}><Text>Atividade não encontrada.</Text></View>;
  }

  const handleDelete = () => {
    setAlertConfig({
      visible: true,
      title: 'Confirmação',
      message: 'Tem certeza que deseja excluir esta atividade?',
      buttons: [
        { text: 'Cancelar', style: 'cancel' },
        { 
          text: 'Excluir', 
          style: 'destructive', 
          onPress: () => {
            deleteActivity(activity.id);
            router.back();
          }
        }
      ]
    });
  };

  const durationMins = activity.durationMs ? Math.round(activity.durationMs / 60000) : 0;

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: 'transparent' }]}>
      <Text variant="h1" style={styles.title}>{activity.title}</Text>
      
      {activity.description && (
        <View style={[styles.descCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Text variant="caption" style={{ color: colors.textSecondary, marginBottom: 8, textTransform: 'uppercase', fontWeight: 'bold' }}>
            Descrição
          </Text>
          <LinkedText text={activity.description} style={{ fontSize: 18, lineHeight: 26, color: colors.text }} />
        </View>
      )}
      
      <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
        <Text variant="h2" style={{ marginBottom: 12 }}>Planejamento</Text>
        {activity.startTime && <Text variant="body" style={styles.row}>Início: {new Date(activity.startTime).toLocaleString('pt-BR')}</Text>}
        {activity.endTime && <Text variant="body" style={styles.row}>Fim: {new Date(activity.endTime).toLocaleString('pt-BR')}</Text>}
        <Text variant="body" style={styles.row}>Duração Estimada: {durationMins} minutos</Text>
      </View>

      <View style={styles.actions}>
        <Button title="Editar" color={colors.surface} textColor={colors.text} onPress={() => router.push(`/activities/${activity.id}/edit`)} />
        <View style={{ height: 16 }} />
        <Button title="Excluir" color={colors.danger} onPress={handleDelete} />
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
  title: { marginBottom: 16, fontSize: 32 },
  descCard: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 24 },
  card: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 24 },
  row: { marginBottom: 8 },
  actions: { marginTop: 'auto', marginBottom: 24 }
});
