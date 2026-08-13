import React, { useState } from 'react';
import { View, StyleSheet, FlatList, TouchableOpacity, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useDataStore } from '../../src/stores/useDataStore';
import { useThemeStore } from '../../src/stores/themeStore';
import { lightColors, darkColors } from '../../src/theme/colors';
import { Text } from '../../src/components/Text';
import { ActionSheet } from '../../src/components/ActionSheet';
import { CustomAlert, AlertButton } from '../../src/components/CustomAlert';

// Helper to get an array of 7 days starting from today (or the start of the week)
const getWeekDays = () => {
  const days = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0); // Normalize to start of day

  // Get Monday of current week (or Sunday, let's just show 7 days starting from today for simplicity, or 3 days back and 3 days forward)
  // Let's do 7 days starting from Sunday of this week
  const startOfWeek = new Date(today);
  startOfWeek.setDate(today.getDate() - today.getDay());

  for (let i = 0; i < 7; i++) {
    const d = new Date(startOfWeek);
    d.setDate(startOfWeek.getDate() + i);
    days.push(d);
  }
  return days;
};

const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];

export default function ActivitiesTab() {
  const router = useRouter();
  const { activities, updateActivity, deleteRecurringGroup } = useDataStore();
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  const [selectedActivityId, setSelectedActivityId] = useState<string | null>(null);
  
  // Normalize today to start of day for default selection
  const todayNormalized = new Date();
  todayNormalized.setHours(0, 0, 0, 0);
  const [selectedDate, setSelectedDate] = useState<Date>(todayNormalized);

  const handleLongPress = (id: string) => {
    setSelectedActivityId(id);
  };

  const selectedActivity = activities.find(a => a.id === selectedActivityId);

  const [alertConfig, setAlertConfig] = useState<{ visible: boolean, title: string, message: string, buttons: AlertButton[] }>({
    visible: false,
    title: '',
    message: '',
    buttons: []
  });

  const handleDelete = () => {
    if (selectedActivityId && selectedActivity) {
      if (selectedActivity.recurringGroupId) {
        setAlertConfig({
          visible: true,
          title: 'Excluir Atividade Recorrente',
          message: 'Esta é uma atividade que se repete. Você deseja excluir apenas esta ocorrência ou todas?',
          buttons: [
            { text: 'Cancelar', style: 'cancel', onPress: () => setAlertConfig(p => ({...p, visible: false})) },
            { 
              text: 'Só Esta', 
              onPress: () => {
                updateActivity(selectedActivityId, { deleted: true });
                setSelectedActivityId(null);
                setAlertConfig(p => ({...p, visible: false}));
              }
            },
            { 
              text: 'Todas', 
              style: 'destructive',
              onPress: () => {
                deleteRecurringGroup(selectedActivity.recurringGroupId!);
                setSelectedActivityId(null);
                setAlertConfig(p => ({...p, visible: false}));
              }
            }
          ]
        });
      } else {
        updateActivity(selectedActivityId, { deleted: true });
        setSelectedActivityId(null);
      }
    }
  };

  const renderItem = ({ item }: { item: any }) => {
    let durationStr = 'Duração não definida';
    if (item.durationMs) {
      const mins = Math.round(item.durationMs / 60000);
      durationStr = `${mins} min`;
    }

    return (
      <TouchableOpacity 
        style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]} 
        onPress={() => router.push(`/activities/${item.id}`)}
        onLongPress={() => handleLongPress(item.id)}
      >
        <Text variant="body" style={{ fontWeight: 'bold' }}>{item.title}</Text>
        {item.startTime && (
          <Text variant="caption" style={{ color: colors.textSecondary, marginTop: 4 }}>
            Início: {new Date(item.startTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </Text>
        )}
        <Text variant="caption" style={{ color: colors.textSecondary, marginTop: 4 }}>{durationStr}</Text>
      </TouchableOpacity>
    );
  };

  // Filter activities for the selected date
  const activeActivities = activities.filter(a => {
    if (a.deleted) return false;
    if (!a.startTime) return false; // Activities without a date don't show on the calendar
    const activityDate = new Date(a.startTime);
    return activityDate.getDate() === selectedDate.getDate() &&
           activityDate.getMonth() === selectedDate.getMonth() &&
           activityDate.getFullYear() === selectedDate.getFullYear();
  });
  
  activeActivities.sort((a, b) => new Date(a.startTime!).getTime() - new Date(b.startTime!).getTime());

  const days = getWeekDays();

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={styles.calendarContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.calendarScroll}>
          {days.map((day, index) => {
            const isSelected = day.getTime() === selectedDate.getTime();
            const isToday = day.getTime() === todayNormalized.getTime();
            
            return (
              <TouchableOpacity
                key={index}
                style={[
                  styles.dayButton,
                  { backgroundColor: isSelected ? colors.primary : colors.surface, borderColor: colors.border },
                  isToday && !isSelected ? { borderColor: colors.primary, borderWidth: 2 } : {}
                ]}
                onPress={() => setSelectedDate(day)}
              >
                <Text style={[styles.dayName, { color: isSelected ? '#fff' : colors.textSecondary }]}>
                  {weekDays[day.getDay()]}
                </Text>
                <Text style={[styles.dayNumber, { color: isSelected ? '#fff' : colors.text }]}>
                  {day.getDate()}
                </Text>
              </TouchableOpacity>
            );
          })}
        </ScrollView>
      </View>

      <FlatList
        data={activeActivities}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        ListEmptyComponent={<Text style={[styles.empty, { color: colors.textSecondary }]}>Nenhuma atividade para este dia.</Text>}
        contentContainerStyle={{ paddingBottom: 100, paddingHorizontal: 16 }}
      />
      <ActionSheet
        visible={!!selectedActivityId}
        onClose={() => setSelectedActivityId(null)}
        title={selectedActivity ? `O que deseja fazer com "${selectedActivity.title}"?` : ''}
        options={[
          { label: 'Editar', onPress: () => {
            setSelectedActivityId(null);
            router.push(`/activities/${selectedActivityId}/edit`);
          }},
          { label: 'Excluir', destructive: true, onPress: () => {
            handleDelete();
            setSelectedActivityId(null);
          }}
        ]}
      />
      <CustomAlert 
        visible={alertConfig.visible}
        title={alertConfig.title}
        message={alertConfig.message}
        buttons={alertConfig.buttons}
        onDismiss={() => setAlertConfig(prev => ({ ...prev, visible: false }))}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  calendarContainer: { paddingVertical: 16 },
  calendarScroll: { paddingHorizontal: 16, gap: 12 },
  dayButton: { 
    width: 60, 
    height: 70, 
    borderRadius: 12, 
    borderWidth: 1, 
    alignItems: 'center', 
    justifyContent: 'center' 
  },
  dayName: { fontSize: 12, marginBottom: 4 },
  dayNumber: { fontSize: 18, fontWeight: 'bold' },
  card: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 12 },
  empty: { textAlign: 'center', marginTop: 32 }
});
