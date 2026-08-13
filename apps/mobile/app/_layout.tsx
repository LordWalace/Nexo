import React, { useEffect, useState } from "react";
import { View, ActivityIndicator, StyleSheet } from "react-native";
import { Stack, useRouter, useSegments } from "expo-router";
import { useAuthStore } from "../src/stores/useAuthStore";
import { useThemeStore } from "../src/stores/themeStore";
import { useDataStore } from "../src/stores/useDataStore";
import { lightColors, darkColors } from "../src/theme/colors";
import { Text } from "../src/components/Text";

export default function RootLayout() {
  const { loadTheme, theme } = useThemeStore();
  const { loadUserName, userName } = useAuthStore();
  const { loadAllData } = useDataStore();
  const colors = theme === "dark" ? darkColors : lightColors;

  const [isReady, setIsReady] = useState(false);
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    async function initApp() {
      await loadTheme();
      await loadAllData();
      await loadUserName();
      setIsReady(true);
    }
    initApp();
  }, []);

  useEffect(() => {
    if (!isReady) return;
    
    const inAuthGroup = segments[0] === "(auth)";
    const isAuthenticated = !!userName;

    if (!isAuthenticated && !inAuthGroup) {
      router.replace("/(auth)/login");
    } else if (isAuthenticated && inAuthGroup) {
      router.replace("/(tabs)");
    }
  }, [isReady, segments, userName]);

  if (!isReady) {
    return (
      <View style={[styles.loadingContainer, { backgroundColor: colors.background }]}>
        <ActivityIndicator size="large" color={colors.accent} />
        <Text variant="h1" style={{ marginTop: 16, color: colors.text }}>Nexo</Text>
      </View>
    );
  }

  return (
    <Stack 
      screenOptions={{ 
        headerShown: false,
        animation: 'slide_from_right', 
        contentStyle: { backgroundColor: colors.background }
      }}
    >
      <Stack.Screen name="(tabs)" options={{ animation: 'fade' }} />
      <Stack.Screen name="(auth)/login" options={{ animation: 'fade' }} />
      <Stack.Screen name="activities/new" options={{ presentation: 'modal', animation: 'slide_from_bottom' }} />
      <Stack.Screen name="activities/[id]/edit" options={{ animation: 'slide_from_right' }} />
      <Stack.Screen name="history/[id]" options={{ animation: 'slide_from_right' }} />
    </Stack>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  }
});
