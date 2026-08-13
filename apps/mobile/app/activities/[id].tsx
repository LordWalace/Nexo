import { View, Text, StyleSheet, ScrollView } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useThemeStore } from "../../src/stores/themeStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Header } from "../../src/components/Header";
import { Button } from "../../src/components/Button";

export default function ActivityDetails() {
  const { id } = useLocalSearchParams();
  const { theme } = useThemeStore();
  const colors = theme === "light" ? lightColors : darkColors;
  const router = useRouter();

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Header title="Detalhes da Atividade" />
      
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={[styles.title, { color: colors.text }]}>Matemática Avançada</Text>
        <Text style={[styles.category, { color: colors.accent }]}>Categoria: Exatas</Text>
        
        <Text style={[styles.label, { color: colors.textSecondary, marginTop: 16 }]}>Descrição</Text>
        <Text style={[styles.description, { color: colors.text }]}>Revisão de cálculo e álgebra linear para a prova final.</Text>

        <Text style={[styles.label, { color: colors.textSecondary, marginTop: 16 }]}>Duração Estimada</Text>
        <Text style={[styles.description, { color: colors.text }]}>1 hora</Text>

        <View style={styles.actions}>
          <Button title="Iniciar sessão" onPress={() => {}} />
          <Button title="Editar" variant="secondary" onPress={() => {}} />
          <Button title="Excluir" variant="secondary" onPress={() => router.back()} />
        </View>
      </ScrollView>
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
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 8,
  },
  category: {
    fontSize: 16,
    fontWeight: "500",
  },
  label: {
    fontSize: 14,
    fontWeight: "bold",
    marginBottom: 4,
    textTransform: "uppercase",
  },
  description: {
    fontSize: 16,
    lineHeight: 24,
  },
  actions: {
    marginTop: 32,
    gap: 12,
  }
});
