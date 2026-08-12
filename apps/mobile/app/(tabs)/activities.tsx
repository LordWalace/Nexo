import { View, Text, StyleSheet, ScrollView } from "react-native";
import { useThemeStore } from "../../src/stores/themeStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Header } from "../../src/components/Header";
import { Card } from "../../src/components/Card";
import { Button } from "../../src/components/Button";
import { useRouter } from "expo-router";

export default function ActivitiesList() {
  const { theme } = useThemeStore();
  const colors = theme === "light" ? lightColors : darkColors;
  const router = useRouter();

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Header title="Atividades" />
      
      <ScrollView contentContainerStyle={styles.content}>
        <Card onPress={() => router.push("/activities/1")}>
          <Text style={[styles.title, { color: colors.text }]}>Matemática Avançada</Text>
          <Text style={[styles.category, { color: colors.accent }]}>Exatas</Text>
          <Text style={[styles.duration, { color: colors.textSecondary }]}>Duração: 1h</Text>
        </Card>

        <Card onPress={() => router.push("/activities/2")}>
          <Text style={[styles.title, { color: colors.text }]}>História do Brasil</Text>
          <Text style={[styles.category, { color: colors.accent }]}>Humanas</Text>
          <Text style={[styles.duration, { color: colors.textSecondary }]}>Duração: 45m</Text>
        </Card>
      </ScrollView>

      <View style={styles.fabContainer}>
        <Button title="Nova atividade" onPress={() => router.push("/activities/new")} />
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
    gap: 12,
    paddingBottom: 80,
  },
  title: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 4,
  },
  category: {
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 8,
  },
  duration: {
    fontSize: 14,
  },
  fabContainer: {
    position: "absolute",
    bottom: 24,
    left: 16,
    right: 16,
  }
});
