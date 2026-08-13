import { View, Text, StyleSheet } from "react-native";
import { useThemeStore } from "../../src/stores/themeStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Header } from "../../src/components/Header";

export default function NewActivity() {
  const { theme } = useThemeStore();
  const colors = theme === "light" ? lightColors : darkColors;

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Header title="Nova Atividade" />
      <View style={styles.content}>
        <Text style={{ color: colors.text }}>Formulário de criação em breve!</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { padding: 16, alignItems: "center", justifyContent: "center" }
});
