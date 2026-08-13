import { View, Text, StyleSheet, Switch, ScrollView } from "react-native";
import { useThemeStore } from "../../src/stores/themeStore";
import { useAuthStore } from "../../src/stores/authStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Header } from "../../src/components/Header";
import { Card } from "../../src/components/Card";
import { Button } from "../../src/components/Button";
import { useRouter } from "expo-router";

export default function Settings() {
  const { theme, toggleTheme } = useThemeStore();
  const { isAnonymous, name, email, logout } = useAuthStore();
  const colors = theme === "light" ? lightColors : darkColors;
  const router = useRouter();

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Header title="Configurações" />
      
      <ScrollView contentContainerStyle={styles.content}>
        
        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>PERFIL</Text>
        <Card>
          <Text style={[styles.profileName, { color: colors.text }]}>{name || "Visitante"}</Text>
          {email && <Text style={[styles.profileEmail, { color: colors.textSecondary }]}>{email}</Text>}
          
          <View style={styles.buttonSpacing}>
            <Button title="Editar Perfil" variant="secondary" onPress={() => router.push("/settings/profile")} />
          </View>
          
          <View style={styles.buttonSpacing}>
            {isAnonymous ? (
              <Button title="Entrar com Google" onPress={() => router.push("/(auth)/login")} />
            ) : (
              <Button title="Sair" variant="secondary" onPress={logout} />
            )}
          </View>
        </Card>

        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>NOTIFICAÇÕES</Text>
        <Card>
          <View style={styles.row}>
            <Text style={[styles.rowText, { color: colors.text }]}>Ativar notificações</Text>
            <Switch value={true} onValueChange={() => {}} trackColor={{ true: colors.accent }} />
          </View>
          <View style={[styles.row, { marginTop: 16 }]}>
            <Text style={[styles.rowText, { color: colors.text }]}>Avisar 10 min antes</Text>
            <Switch value={true} onValueChange={() => {}} trackColor={{ true: colors.accent }} />
          </View>
        </Card>

        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>APARÊNCIA</Text>
        <Card>
          <View style={styles.row}>
            <Text style={[styles.rowText, { color: colors.text }]}>Tema Escuro</Text>
            <Switch value={theme === "dark"} onValueChange={toggleTheme} trackColor={{ true: colors.accent }} />
          </View>
        </Card>

        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>SINCRONIZAÇÃO</Text>
        <Card>
          <Text style={[styles.syncStatus, { color: isAnonymous ? colors.textSecondary : colors.success }]}>
            {isAnonymous ? "Aguardando conexão (Modo Local)" : "Sincronizado"}
          </Text>
          {!isAnonymous && (
            <View style={styles.buttonSpacing}>
              <Button title="Sincronizar agora" variant="secondary" onPress={() => {}} />
            </View>
          )}
        </Card>

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
    paddingBottom: 48,
  },
  sectionTitle: {
    fontSize: 12,
    fontWeight: "bold",
    marginTop: 24,
    marginBottom: 8,
    marginLeft: 4,
  },
  profileName: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 4,
  },
  profileEmail: {
    fontSize: 14,
    marginBottom: 16,
  },
  buttonSpacing: {
    marginTop: 12,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  rowText: {
    fontSize: 16,
  },
  syncStatus: {
    fontSize: 16,
    fontWeight: "500",
  }
});
