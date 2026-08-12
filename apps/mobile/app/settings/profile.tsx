import { View, Text, StyleSheet, TextInput } from "react-native";
import { useThemeStore } from "../../src/stores/themeStore";
import { useAuthStore } from "../../src/stores/authStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Header } from "../../src/components/Header";
import { Button } from "../../src/components/Button";
import { useRouter } from "expo-router";
import { useState } from "react";

export default function Profile() {
  const { theme } = useThemeStore();
  const { name, email, setProfile } = useAuthStore();
  const colors = theme === "light" ? lightColors : darkColors;
  const router = useRouter();

  const [inputName, setInputName] = useState(name);

  const handleSave = () => {
    setProfile(inputName, email);
    router.back();
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Header title="Editar Perfil" />
      
      <View style={styles.content}>
        <Text style={[styles.label, { color: colors.text }]}>Nome</Text>
        <TextInput
          style={[styles.input, { color: colors.text, borderColor: colors.border, backgroundColor: colors.surface }]}
          value={inputName}
          onChangeText={setInputName}
          placeholder="Seu nome"
          placeholderTextColor={colors.textSecondary}
        />

        <Text style={[styles.label, { color: colors.text, marginTop: 16 }]}>Email</Text>
        <TextInput
          style={[styles.input, { color: colors.textSecondary, borderColor: colors.border, backgroundColor: colors.surface, opacity: 0.7 }]}
          value={email || "Não vinculado"}
          editable={false}
        />

        <View style={styles.actions}>
          <Button title="Salvar" onPress={handleSave} />
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: "500",
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  actions: {
    marginTop: 32,
  }
});
