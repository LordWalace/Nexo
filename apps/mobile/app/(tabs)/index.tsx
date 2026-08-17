import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView, Linking } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useDataStore } from '../../src/stores/useDataStore';
import { useAuthStore } from '../../src/stores/useAuthStore';
import { useThemeStore } from '../../src/stores/themeStore';
import { lightColors, darkColors } from '../../src/theme/colors';
import { Text } from '../../src/components/Text';

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

export default function Home() {
  const { activities, loadAllData, updateActivity } = useDataStore();
  const { userName, loadUserName } = useAuthStore();
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    loadAllData();
    loadUserName();
    const interval = setInterval(() => {
      const nowTime = new Date();
      setCurrentTime(nowTime);
      
      // Auto-archive expired activities without triggering re-render dependency loop
      const state = useDataStore.getState();
      state.activities.forEach(a => {
        if (!a.deleted && a.endTime) {
          if (new Date(a.endTime).getTime() < nowTime.getTime()) {
            state.updateActivity(a.id, { deleted: true });
          }
        }
      });
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const getGreeting = () => {
    const hour = currentTime.getHours();
    if (hour >= 5 && hour < 12) return 'Bom dia';
    if (hour >= 12 && hour < 18) return 'Boa tarde';
    return 'Boa noite';
  };

  const now = currentTime.getTime();
  
  const currentActivities = activities.filter(a => 
    !a.deleted && a.startTime && a.endTime &&
    new Date(a.startTime).getTime() <= now &&
    new Date(a.endTime).getTime() > now
  );
  
  const currentActivity = currentActivities.length > 0 ? currentActivities[0] : null;

  const getNextActivities = () => {
    const futureActivities = activities.filter(a => !a.deleted && a.startTime && new Date(a.startTime).getTime() > now);
    futureActivities.sort((a, b) => new Date(a.startTime!).getTime() - new Date(b.startTime!).getTime());
    return futureActivities.slice(0, 5);
  };

  const nextActivities = getNextActivities();
  const nextActivitiesWithoutCurrent = nextActivities.filter(a => a.id !== currentActivity?.id);

  const dateStr = currentTime.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  const timeStr = currentTime.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

  let countdownStr = '';
  if (currentActivity && currentActivity.endTime) {
    const endMs = new Date(currentActivity.endTime).getTime();
    const diffMs = endMs - now;
    if (diffMs > 0) {
      const hours = Math.floor(diffMs / 3600000);
      const mins = Math.floor((diffMs % 3600000) / 60000);
      const secs = Math.floor((diffMs % 60000) / 1000);
      countdownStr = `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
  }

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: 'transparent' }}>
      <ScrollView style={[styles.container, { backgroundColor: 'transparent' }]}>
      <View style={styles.header}>
        <Text variant="caption" style={{ color: colors.textSecondary, textTransform: 'capitalize' }}>{dateStr}</Text>
        <Text variant="body" style={{ color: colors.textSecondary, marginTop: 4 }}>{timeStr}</Text>
        <Text variant="h1" style={styles.greeting}>
          {getGreeting()}, {userName || 'Usuário'}
        </Text>
      </View>

      {currentActivity && (
        <View style={{ marginBottom: 24 }}>
          <Text variant="h2" style={styles.sectionTitle}>Acontecendo Agora</Text>
          <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
            <Text variant="h2">{currentActivity.title}</Text>
            {currentActivity.description && (
              <LinkedText text={currentActivity.description} style={{ marginTop: 8 }} />
            )}
            <Text variant="h1" style={{ color: colors.accent, marginTop: 12 }}>
              {countdownStr} restantes
            </Text>
          </View>
        </View>
      )}

      <Text variant="h2" style={styles.sectionTitle}>Próximas Atividades</Text>
      {nextActivitiesWithoutCurrent.length > 0 ? (
        nextActivitiesWithoutCurrent.map((activity, index) => {
          let startCountdownStr = '';
          let isToday = false;
          let dateStr = '';
          
          if (activity.startTime) {
            const startDate = new Date(activity.startTime);
            const today = new Date();
            isToday = startDate.getDate() === today.getDate() && 
                      startDate.getMonth() === today.getMonth() && 
                      startDate.getFullYear() === today.getFullYear();
            
            if (isToday) {
              const diffToStart = startDate.getTime() - now;
              if (diffToStart > 0) {
                const hours = Math.floor(diffToStart / 3600000);
                const mins = Math.floor((diffToStart % 3600000) / 60000);
                const secs = Math.floor((diffToStart % 60000) / 1000);
                startCountdownStr = `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
              }
            } else {
              dateStr = startDate.toLocaleDateString('pt-BR');
            }
          }

          return (
            <View key={activity.id} style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border, marginTop: index > 0 ? 0 : undefined }]}>
              <Text variant="h2">{activity.title}</Text>
              {activity.description && (
                <LinkedText text={activity.description} style={{ marginTop: 8 }} />
              )}
              
              {isToday && startCountdownStr ? (
                <Text variant="h1" style={{ color: colors.primary, marginTop: 12 }}>
                  Inicia em {startCountdownStr}
                </Text>
              ) : null}
              
              <View style={styles.timeInfo}>
                {activity.startTime && (
                  <Text variant="caption">
                    Início: {!isToday && dateStr ? `${dateStr} às ` : ''}{new Date(activity.startTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </Text>
                )}
                {activity.endTime && (
                  <Text variant="caption">Fim: {new Date(activity.endTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</Text>
                )}
              </View>
            </View>
          );
        })
      ) : (
        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border, alignItems: 'center' }]}>
          <Text variant="body" style={{ color: colors.textSecondary }}>Nenhuma atividade hoje.</Text>
        </View>
      )}
    </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  header: { marginBottom: 32, marginTop: 16 },
  greeting: { marginTop: 8 },
  sectionTitle: { marginBottom: 12 },
  card: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 16 },
  timeInfo: { marginTop: 12, gap: 4 }
});
