import React, { useState } from 'react';
import { View, StyleSheet, TextInput, ScrollView, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useDataStore } from '../../../src/stores/useDataStore';
import { useThemeStore } from '../../../src/stores/themeStore';
import { lightColors, darkColors } from '../../../src/theme/colors';
import { Text } from '../../../src/components/Text';
import { Button } from '../../../src/components/Button';
import DateTimePicker from '@react-native-community/datetimepicker';

export default function EditActivity() {
  const { id, recover } = useLocalSearchParams<{ id: string, recover?: string }>();
  const router = useRouter();
  const { activities, updateActivity, categories } = useDataStore();
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  const activity = activities.find(a => a.id === id);

  const [title, setTitle] = useState(activity?.title || '');
  const [description, setDescription] = useState(activity?.description || '');
  const [categoryId, setCategoryId] = useState(activity?.categoryId || '');

  const [date, setDate] = useState(activity?.startTime ? new Date(activity.startTime) : new Date());
  const [startTime, setStartTime] = useState(activity?.startTime ? new Date(activity.startTime) : new Date());
  const [endTime, setEndTime] = useState(activity?.endTime ? new Date(activity.endTime) : new Date(Date.now() + 3600000));

  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showStartTimePicker, setShowStartTimePicker] = useState(false);
  const [showEndTimePicker, setShowEndTimePicker] = useState(false);

  if (!activity) {
    return <View style={[styles.container, { backgroundColor: colors.background }]}><Text>Atividade não encontrada.</Text></View>;
  }

  const handleSave = () => {
    if (!title.trim()) return;

    const finalStart = new Date(date);
    finalStart.setHours(startTime.getHours(), startTime.getMinutes(), 0, 0);

    const finalEnd = new Date(date);
    finalEnd.setHours(endTime.getHours(), endTime.getMinutes(), 0, 0);
    if (finalEnd < finalStart) {
      finalEnd.setDate(finalEnd.getDate() + 1);
    }

    updateActivity(id, {
      title,
      description,
      categoryId: categoryId || undefined,
      startTime: finalStart.toISOString(),
      endTime: finalEnd.toISOString(),
      deleted: false
    });
    
    if (recover === 'true') {
      router.replace('/(tabs)');
    } else {
      router.back();
    }
  };

  const inputStyle = [styles.input, { backgroundColor: colors.surface, borderColor: colors.border, color: colors.text }];

  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: colors.background }]}>
      <Text variant="body" style={styles.label}>Título (obrigatório)</Text>
      <TextInput 
        style={inputStyle} 
        value={title} 
        onChangeText={setTitle} 
        placeholderTextColor={colors.textSecondary}
      />

      <Text variant="body" style={styles.label}>Descrição (opcional)</Text>
      <TextInput 
        style={[inputStyle, { height: 100, textAlignVertical: 'top' }]} 
        value={description} 
        onChangeText={setDescription} 
        multiline 
        placeholderTextColor={colors.textSecondary}
      />

      <Text variant="body" style={styles.label}>Categoria (opcional)</Text>
      <View style={styles.categoryList}>
        {categories.map((c: any) => (
          <TouchableOpacity 
            key={c.id} 
            style={[
              styles.categoryBtn, 
              { borderColor: colors.border, backgroundColor: colors.surface },
              categoryId === c.id && { backgroundColor: colors.accent, borderColor: colors.accent }
            ]}
            onPress={() => setCategoryId(c.id)}
          >
            <Text color={categoryId === c.id ? '#FFF' : colors.text}>{c.name}</Text>
          </TouchableOpacity>
        ))}
        <TouchableOpacity 
          style={[
            styles.categoryBtn, 
            { borderColor: colors.border, backgroundColor: colors.surface },
            categoryId === '' && { backgroundColor: colors.accent, borderColor: colors.accent }
          ]}
          onPress={() => setCategoryId('')}
        >
          <Text color={categoryId === '' ? '#FFF' : colors.text}>Nenhuma Categoria</Text>
        </TouchableOpacity>
      </View>

      <Text variant="body" style={styles.label}>Data Planejada</Text>
      <TouchableOpacity style={inputStyle} onPress={() => setShowDatePicker(true)}>
        <Text>{date.toLocaleDateString('pt-BR')}</Text>
      </TouchableOpacity>
      {showDatePicker && (
        <DateTimePicker
          value={date}
          mode="date"
          display="default"
          themeVariant={theme === 'dark' ? 'dark' : 'light'}
          onChange={(event, selectedDate) => {
            setShowDatePicker(false);
            if (selectedDate) setDate(selectedDate);
          }}
        />
      )}

      <Text variant="body" style={styles.label}>Horário de Início</Text>
      <TouchableOpacity style={inputStyle} onPress={() => setShowStartTimePicker(true)}>
        <Text>{startTime.toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})}</Text>
      </TouchableOpacity>
      {showStartTimePicker && (
        <DateTimePicker
          value={startTime}
          mode="time"
          is24Hour={true}
          display="default"
          themeVariant={theme === 'dark' ? 'dark' : 'light'}
          onChange={(event, selectedDate) => {
            setShowStartTimePicker(false);
            if (selectedDate) setStartTime(selectedDate);
          }}
        />
      )}

      <Text variant="body" style={styles.label}>Horário de Fim</Text>
      <TouchableOpacity style={inputStyle} onPress={() => setShowEndTimePicker(true)}>
        <Text>{endTime.toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})}</Text>
      </TouchableOpacity>
      {showEndTimePicker && (
        <DateTimePicker
          value={endTime}
          mode="time"
          is24Hour={true}
          display="default"
          themeVariant={theme === 'dark' ? 'dark' : 'light'}
          onChange={(event, selectedDate) => {
            setShowEndTimePicker(false);
            if (selectedDate) setEndTime(selectedDate);
          }}
        />
      )}

      <View style={styles.actions}>
        <Button title="Cancelar" color={colors.surface} textColor={colors.text} onPress={() => router.back()} style={{ flex: 1, marginRight: 8 }} />
        <Button title="Salvar" color={colors.accent} onPress={handleSave} style={{ flex: 1, marginLeft: 8 }} />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 16 },
  label: { marginBottom: 4, marginTop: 16 },
  input: { padding: 12, borderRadius: 8, borderWidth: 1, fontSize: 16, minHeight: 48, justifyContent: 'center' },
  actions: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 32 },
  categoryList: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 4 },
  categoryBtn: { paddingHorizontal: 16, paddingVertical: 10, borderRadius: 20, borderWidth: 1 }
});
