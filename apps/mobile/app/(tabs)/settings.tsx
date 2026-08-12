import { View, Text, StyleSheet, Switch, TouchableOpacity } from "react-native";
import { useRouter } from "expo-router";
import { useThemeStore } from "../../src/stores/themeStore";
import { useAuthStore } from "../../src/stores/authStore";
import { lightColors, darkColors } from "../../src/theme/colors";

export default function SettingsScreen() {
  const router = useRouter();
  const { theme, setTheme } = useThemeStore();
  const { isLoggedIn, logout } = useAuthStore();
  const colors = theme === "dark" ? darkColors : lightColors;

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      
      <View style={[styles.row, { backgroundColor: colors.surface }]}>
        <Text style={[styles.label, { color: colors.text }]}>Modo Escuro</Text>
        <Switch value={theme === "dark"} onValueChange={toggleTheme} />
      </View>

      {!isLoggedIn ? (
        <TouchableOpacity 
          style={[styles.button, { backgroundColor: colors.primary, marginTop: 24 }]}
          onPress={() => router.push("/(auth)/login")}
        >
          <Text style={styles.buttonText}>Sincronizar Conta (Login)</Text>
        </TouchableOpacity>
      ) : (
        <TouchableOpacity 
          style={[styles.button, { backgroundColor: "#ef4444", marginTop: 24 }]}
          onPress={() => logout()}
        >
          <Text style={styles.buttonText}>Sair</Text>
        </TouchableOpacity>
      )}

    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  row: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", padding: 16, borderRadius: 8 },
  label: { fontSize: 16 },
  button: { padding: 16, borderRadius: 8, alignItems: "center" },
  buttonText: { color: "#fff", fontSize: 16, fontWeight: "600" }
});

