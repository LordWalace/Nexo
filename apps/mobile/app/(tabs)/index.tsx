import { View, Text, StyleSheet, ScrollView } from "react-native";
import { useThemeStore } from "../../src/stores/themeStore";
import { useAuthStore } from "../../src/stores/authStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Button } from "../../src/components/Button";
import { Card } from "../../src/components/Card";
import { useRouter } from "expo-router";

export default function Home() {
  const { theme } = useThemeStore();
  const colors = theme === "light" ? lightColors : darkColors;
  const { name } = useAuthStore();
  const router = useRouter();

  const greeting = name ? "Bom dia, ${name}!" : "Bom dia!";

  return (
    <ScrollView style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={styles.header}>
        <Text style={[styles.greeting, { color: colors.text }]}>{greeting}</Text>
        <Text style={[styles.date, { color: colors.textSecondary }]}>Aqui está o seu resumo de hoje.</Text>
      </View>

      <Card>
        <Text style={[styles.sectionTitle, { color: colors.text }]}>Próxima atividade</Text>
        <Text style={[styles.activityTitle, { color: colors.text }]}>Matemática Avançada</Text>
        <Text style={[styles.activityTime, { color: colors.accent }]}>14:30 - 15:30</Text>
        <View style={styles.buttonRow}>
          <Button title="Ver detalhes" onPress={() => router.push("/activities/1")} />
        </View>
      </Card>

      <Card>
        <Text style={[styles.sectionTitle, { color: colors.text }]}>Resumo do dia</Text>
        <Text style={[styles.statsText, { color: colors.textSecondary }]}>Tempo estudado hoje: 2h 15m</Text>
      </Card>

      <View style={styles.actions}>
        <Button title="Nova atividade" onPress={() => router.push("/activities/new")} />
        <Button title="Ver todas as atividades" variant="secondary" onPress={() => router.push("/(tabs)/activities")} />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  header: {
    marginTop: 48,
    marginBottom: 24,
  },
  greeting: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 8,
  },
  date: {
    fontSize: 16,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: "bold",
    marginBottom: 12,
    textTransform: "uppercase",
  },
  activityTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 4,
  },
  activityTime: {
    fontSize: 16,
    fontWeight: "500",
    marginBottom: 16,
  },
  statsText: {
    fontSize: 16,
  },
  buttonRow: {
    alignItems: "flex-start",
  },
  actions: {
    marginTop: 24,
    gap: 12,
    paddingBottom: 48,
  }
});
