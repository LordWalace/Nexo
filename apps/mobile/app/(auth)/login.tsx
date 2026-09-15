import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator } from "react-native";
import { useRouter } from "expo-router";
import * as WebBrowser from "expo-web-browser";
import * as Google from "expo-auth-session/providers/google";
import { useEffect, useState } from "react";
import { useAuthStore } from "../../src/stores/useAuthStore";
import { useThemeStore } from "../../src/stores/themeStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { auth } from "../../src/config/firebase";
import { GoogleAuthProvider, signInWithCredential } from "firebase/auth";

WebBrowser.maybeCompleteAuthSession();

export default function LoginScreen() {
  const router = useRouter();
  const { setOfflineUser } = useAuthStore();
  const { theme } = useThemeStore();
  const colors = theme === "dark" ? darkColors : lightColors;
  const [loading, setLoading] = useState(false);

  // Aqui estamos forçando a URL do proxy do Expo para funcionar no Expo Go
  const [request, response, promptAsync] = Google.useAuthRequest({
    clientId: "270618831747-1ijsaof3ts0igrgbkj3eig97h0g03ceb.apps.googleusercontent.com",
    scopes: ["profile", "email"],
    redirectUri: "https://auth.expo.io/@lordwalace/nexo"
  });

  useEffect(() => {
    if (response?.type === "success") {
      const { id_token } = response.params;
      if (id_token) {
        handleFirebaseSignIn(id_token);
      }
    } else if (response?.type === "error") {
      setLoading(false);
      console.error(response.error);
    } else if (response?.type === "dismiss") {
      setLoading(false);
    }
  }, [response]);

  const handleFirebaseSignIn = async (idToken: string) => {
    try {
      const credential = GoogleAuthProvider.credential(idToken);
      await signInWithCredential(auth, credential);
    } catch (error) {
      console.error("Firebase Sign In Error:", error);
      setLoading(false);
    }
  };

  const handleOffline = () => {
    setOfflineUser("Visitante");
  };

  const handleLoginPress = () => {
    setLoading(true);
    promptAsync();
  };

  return (
    <View style={[styles.container, { backgroundColor: 'transparent' }]}>
      <Text style={[styles.title, { color: colors.text }]}>Sincronizar Conta</Text>
      <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
        Faça login com o Google para salvar seus dados e sincronizá-los entre dispositivos.
      </Text>
      
      <TouchableOpacity 
        style={[styles.button, { backgroundColor: colors.primary, opacity: (!request || loading) ? 0.7 : 1 }]}
        disabled={!request || loading}
        onPress={handleLoginPress}
      >
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Entrar com Google</Text>}
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
