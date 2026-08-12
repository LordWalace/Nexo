import { View, Text, StyleSheet } from "react-native";
import { useThemeStore } from "../../src/stores/themeStore";
import { useAuthStore } from "../../src/stores/authStore";
import { lightColors, darkColors } from "../../src/theme/colors";

export default function HomeScreen() {
  const { theme } = useThemeStore();
  const { localUserId, isLoggedIn } = useAuthStore();
  const colors = theme === "dark" ? darkColors : lightColors;

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Text style={[styles.title, { color: colors.text }]}>Dashboard</Text>
      <View style={[styles.card, { backgroundColor: colors.surface }]}>
        <Text style={[styles.text, { color: colors.textSecondary }]}>
          Modo: {isLoggedIn ? "Logado / Sincronizado" : "Anônimo / Local"}
        </Text>
        <Text style={[styles.text, { color: colors.textSecondary, marginTop: 8 }]}>
          Local ID: {localUserId}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 16 },
  card: { padding: 16, borderRadius: 8 },
  text: { fontSize: 14 }
});

