import React, { useState } from 'react';
import { View, StyleSheet, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import * as Crypto from 'expo-crypto';
import { useDataStore } from '../../src/stores/useDataStore';
import { useThemeStore } from '../../src/stores/themeStore';
import { lightColors, darkColors } from '../../src/theme/colors';
import { Text } from '../../src/components/Text';
import { Button } from '../../src/components/Button';
import DateTimePicker from '@react-native-community/datetimepicker';

export default function NewActivityWizard() {
  const router = useRouter();
  const { addActivity, addActivities, categories } = useDataStore();
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  const [step, setStep] = useState(1);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState('');
  
  const [date, setDate] = useState(new Date());
  const [startTime, setStartTime] = useState(new Date());
  const [endTime, setEndTime] = useState(new Date(Date.now() + 3600000)); // +1h

  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showStartTimePicker, setShowStartTimePicker] = useState(false);
  const [showEndTimePicker, setShowEndTimePicker] = useState(false);
  const [repeatDays, setRepeatDays] = useState<number[]>([]);

  const handleNext = () => setStep(step + 1);
  const handleBack = () => setStep(step - 1);
  const handleCancel = () => router.back();

  const handleSave = () => {
    const finalStart = new Date(date);
    finalStart.setHours(startTime.getHours(), startTime.getMinutes(), 0, 0);

    const finalEnd = new Date(date);
    finalEnd.setHours(endTime.getHours(), endTime.getMinutes(), 0, 0);
    if (finalEnd < finalStart) {
      finalEnd.setDate(finalEnd.getDate() + 1);
    }

    if (repeatDays.length > 0) {
      const activitiesToCreate = [];
      const groupId = Crypto.randomUUID();
      for (let week = 0; week < 52; week++) {
        for (const day of repeatDays) {
          const d = new Date(finalStart);
          const diff = day - d.getDay();
          d.setDate(d.getDate() + diff + (week * 7));
          
          if (week === 0 && d.getTime() < finalStart.getTime() && day !== finalStart.getDay()) {
             continue; // Skip past days in the first week
          }

          const actStart = new Date(d);
          const actEnd = new Date(d);
          actEnd.setHours(endTime.getHours(), endTime.getMinutes(), 0, 0);
          if (actEnd < actStart) actEnd.setDate(actEnd.getDate() + 1);

          activitiesToCreate.push({
            title,
            description,
            categoryId: categoryId || undefined,
            startTime: actStart.toISOString(),
            endTime: actEnd.toISOString(),
            recurringGroupId: groupId
          });
        }
      }
      if (activitiesToCreate.length > 0) {
        addActivities(activitiesToCreate);
      }
    } else {
      addActivity({
        title,
        description,
        categoryId: categoryId || undefined,
        startTime: finalStart.toISOString(),
        endTime: finalEnd.toISOString()
      });
    }
    router.back();
  };

  const inputStyle = [styles.input, { backgroundColor: colors.surface, borderColor: colors.border, color: colors.text }];

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: colors.background }}>
      <ScrollView contentContainerStyle={[styles.container, { backgroundColor: colors.background }]}>
      <Text variant="h2" style={styles.stepTitle}>Passo {step} de 6</Text>

      {step === 1 && (
        <View style={styles.stepContainer}>
          <Text variant="body" style={styles.label}>Nome da atividade</Text>
          <TextInput 
            style={inputStyle} 
            value={title} 
            onChangeText={setTitle} 
            autoFocus 
            placeholder="Ex: Reunião de equipe"
            placeholderTextColor={colors.textSecondary}
          />
          <View style={styles.actions}>
            <Button title="Cancelar" color={colors.danger} onPress={handleCancel} />
            <Button title="Continuar" color={colors.accent} onPress={handleNext} disabled={!title.trim()} />
          </View>
        </View>
      )}

      {step === 2 && (
        <View style={styles.stepContainer}>
          <Text variant="body" style={styles.label}>Descrição (opcional)</Text>
          <TextInput 
            style={[inputStyle, { height: 100 }]} 
            value={description} 
            onChangeText={setDescription} 
            multiline 
            placeholder="Detalhes da atividade..."
            placeholderTextColor={colors.textSecondary}
          />
          <View style={styles.actions}>
            <Button title="Voltar" color={colors.surface} textColor={colors.text} onPress={handleBack} />
            <Button title="Continuar" color={colors.accent} onPress={handleNext} />
          </View>
        </View>
      )}

      {step === 3 && (
        <View style={styles.stepContainer}>
          <Text variant="body" style={styles.label}>Categoria (opcional)</Text>
          <View style={styles.categoryList}>
            {categories.map(c => (
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
          <View style={styles.actions}>
            <Button title="Voltar" color={colors.surface} textColor={colors.text} onPress={handleBack} />
            <Button title="Continuar" color={colors.accent} onPress={handleNext} />
          </View>
        </View>
      )}

      {step === 4 && (
        <View style={styles.stepContainer}>
          <Text variant="body" style={styles.label}>Data</Text>
          <TouchableOpacity style={inputStyle} onPress={() => setShowDatePicker(true)}>
            <Text>{date.toLocaleDateString('pt-BR')}</Text>
          </TouchableOpacity>
          {showDatePicker && (
            <DateTimePicker
              value={date}
              mode="date"
              display="default"
              onChange={(event, selectedDate) => {
                setShowDatePicker(false);
                if (selectedDate) setDate(selectedDate);
              }}
            />
          )}
          <View style={styles.actions}>
            <Button title="Voltar" color={colors.surface} textColor={colors.text} onPress={handleBack} />
            <Button title="Continuar" color={colors.accent} onPress={handleNext} />
          </View>
        </View>
      )}

      {step === 5 && (
        <View style={styles.stepContainer}>
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

          <Text variant="body" style={[styles.label, {marginTop: 16}]}>Horário de Fim</Text>
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
            <Button title="Voltar" color={colors.surface} textColor={colors.text} onPress={handleBack} />
            <Button title="Continuar" color={colors.accent} onPress={handleNext} />
          </View>
        </View>
      )}

      {step === 6 && (
        <View style={styles.stepContainer}>
          <Text variant="body" style={styles.label}>Repetir esta atividade?</Text>
          <Text variant="caption" style={{ color: colors.textSecondary, marginBottom: 16 }}>Selecione os dias da semana para repetir por 1 ano.</Text>
          
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 32 }}>
            {[{l:'D', v:0}, {l:'S', v:1}, {l:'T', v:2}, {l:'Q', v:3}, {l:'Q', v:4}, {l:'S', v:5}, {l:'S', v:6}].map(day => (
              <TouchableOpacity
                key={day.v}
                style={[
                  styles.categoryBtn,
                  { paddingHorizontal: 12, paddingVertical: 12, borderRadius: 24, width: 42, alignItems: 'center' },
                  repeatDays.includes(day.v) ? { backgroundColor: colors.accent, borderColor: colors.accent } : { backgroundColor: colors.surface, borderColor: colors.border }
                ]}
                onPress={() => {
                  if (repeatDays.includes(day.v)) {
                    setRepeatDays(repeatDays.filter(d => d !== day.v));
                  } else {
                    setRepeatDays([...repeatDays, day.v].sort());
                  }
                }}
              >
                <Text color={repeatDays.includes(day.v) ? '#FFF' : colors.text}>{day.l}</Text>
              </TouchableOpacity>
            ))}
          </View>

          <View style={styles.actions}>
            <Button title="Voltar" color={colors.surface} textColor={colors.text} onPress={handleBack} />
            <Button title="Finalizar e Salvar" color={colors.accent} onPress={handleSave} />
          </View>
        </View>
      )}
    </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 16 },
  stepTitle: { marginBottom: 24, textAlign: 'center' },
  stepContainer: { flex: 1 },
  label: { marginBottom: 8 },
  input: { padding: 12, borderRadius: 8, borderWidth: 1, fontSize: 16, minHeight: 48, justifyContent: 'center' },
  actions: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 32 },
  categoryList: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  categoryBtn: { paddingHorizontal: 16, paddingVertical: 10, borderRadius: 20, borderWidth: 1 }
});
