import React, { useState } from "react";
import { View, StyleSheet, TextInput, ScrollView, Alert } from "react-native";
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from "expo-router";
import { useAuthStore } from "../../src/stores/useAuthStore";
import { useThemeStore } from "../../src/stores/themeStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Text } from "../../src/components/Text";
import { Button } from "../../src/components/Button";

export default function Profile() {
  const { userName, setUserName } = useAuthStore();
  const { theme } = useThemeStore();
  const colors = theme === "dark" ? darkColors : lightColors;
  const router = useRouter();

  const [name, setName] = useState(userName || "");

  const handleSave = () => {
    if (!name.trim()) {
      Alert.alert("Erro", "O nome não pode estar vazio.");
      return;
    }
    setUserName(name.trim());
    router.back();
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: 'transparent' }}>
      <ScrollView contentContainerStyle={[styles.container, { backgroundColor: 'transparent' }]}>
      <Text variant="body" style={styles.label}>Como prefere ser chamado?</Text>
      <TextInput
        style={[styles.input, { backgroundColor: colors.surface, borderColor: colors.border, color: colors.text }]}
        value={name}
        onChangeText={setName}
        placeholder="Seu nome"
        placeholderTextColor={colors.textSecondary}
      />
      <View style={styles.actions}>
        <Button title="Cancelar" color={colors.surface} textColor={colors.text} onPress={() => router.back()} style={{ flex: 1, marginRight: 8 }} />
        <Button title="Salvar" color={colors.accent} onPress={handleSave} style={{ flex: 1, marginLeft: 8 }} />
      </View>
    </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 16,
  },
  label: {
    marginBottom: 8,
    marginTop: 24,
  },
  input: {
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    fontSize: 16,
    minHeight: 48,
  },
  actions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 32,
  },
});
