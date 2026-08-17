import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import * as WebBrowser from "expo-web-browser";
import * as Google from "expo-auth-session/providers/google";
import { useEffect } from "react";
import { useAuthStore } from "../../src/stores/useAuthStore";
import { useThemeStore } from "../../src/stores/themeStore";
import { lightColors, darkColors } from "../../src/theme/colors";

WebBrowser.maybeCompleteAuthSession();

export default function LoginScreen() {
  const router = useRouter();
  const { setUserName } = useAuthStore();
  const { theme } = useThemeStore();
  const colors = theme === "dark" ? darkColors : lightColors;

  const [request, response, promptAsync] = Google.useAuthRequest({
    clientId: "YOUR_GOOGLE_CLIENT_ID",
  });

  useEffect(() => {
    if (response?.type === "success") {
      const { id_token } = response.params;
      if (id_token) {
        handleGoogleLogin(id_token);
      }
    }
  }, [response]);

  const handleGoogleLogin = async (idToken: string) => {
    try {
      setUserName("Usuário Google");
    } catch (error) {
      console.error(error);
    }
  };

  const handleOffline = () => {
    setUserName("Visitante");
  };

  return (
    <View style={[styles.container, { backgroundColor: 'transparent' }]}>
      <Text style={[styles.title, { color: colors.text }]}>Sincronizar Conta</Text>
      <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
        Faça login com o Google para salvar seus dados e sincronizá-los entre dispositivos.
      </Text>
      
      <TouchableOpacity 
        style={[styles.button, { backgroundColor: colors.primary }]}
        disabled={!request}
        onPress={() => promptAsync()}
      >
        <Text style={styles.buttonText}>Entrar com Google</Text>
      </TouchableOpacity>
      
      <TouchableOpacity onPress={handleOffline} style={styles.skipButton}>
        <Text style={[styles.skipText, { color: colors.textSecondary }]}>Voltar ao modo offline</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: "center", alignItems: "center" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 12 },
  subtitle: { fontSize: 16, textAlign: "center", marginBottom: 32 },
  button: { paddingVertical: 12, paddingHorizontal: 24, borderRadius: 8, width: "100%", alignItems: "center" },
  buttonText: { color: "#ffffff", fontSize: 16, fontWeight: "600" },
  skipButton: { marginTop: 16, padding: 8 },
  skipText: { fontSize: 14 }
});
