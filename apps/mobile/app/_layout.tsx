import React, { useEffect, useState } from "react";
import { View, ActivityIndicator, StyleSheet } from "react-native";
import { Stack, useRouter, useSegments } from "expo-router";
import { useAuthStore } from "../src/stores/useAuthStore";
import { useThemeStore } from "../src/stores/themeStore";
import { useDataStore } from "../src/stores/useDataStore";
import { lightColors, darkColors } from "../src/theme/colors";
import { Text } from "../src/components/Text";
import LoadingScreen from './_loading';
import { ThemeProvider, DefaultTheme, DarkTheme } from "@react-navigation/native";
import { AnimatedBackground } from "../src/components/AnimatedBackground";
import { SmartBanner } from "../src/components/SmartBanner";
import { requestNotificationPermissions } from "../src/services/notifications";

export default function RootLayout() {
  const { loadTheme, theme } = useThemeStore();
  const { initializeAuth, isInitialized, userName } = useAuthStore();
  const { loadAllData } = useDataStore();
  const colors = theme === "dark" ? darkColors : lightColors;

  const [dataLoaded, setDataLoaded] = useState(false);
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    async function initApp() {
      await loadTheme();
      await loadAllData();
      await requestNotificationPermissions();
      initializeAuth();
      setDataLoaded(true);
    }
    initApp();
  }, []);

  const isReady = dataLoaded && isInitialized;

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
    return <LoadingScreen />;
  }

  const customTheme = theme === "dark" ? DarkTheme : DefaultTheme;
  const navigationTheme = {
    ...customTheme,
    colors: {
      ...customTheme.colors,
      background: "transparent",
    },
  };

  return (
    <ThemeProvider value={navigationTheme}>
      <View style={{ flex: 1, backgroundColor: colors.background }}>
        <AnimatedBackground />
        <SmartBanner />
        <Stack 
          screenOptions={{ 
            headerShown: false,
            animation: 'slide_from_right', 
            contentStyle: { backgroundColor: 'transparent' }
          }}
        >
          <Stack.Screen name="(tabs)" options={{ animation: 'fade' }} />
          <Stack.Screen name="(auth)/login" options={{ animation: 'fade' }} />
          <Stack.Screen name="activities/new" options={{ presentation: 'modal', animation: 'slide_from_bottom' }} />
          <Stack.Screen name="activities/[id]/edit" options={{ animation: 'slide_from_right' }} />
          <Stack.Screen name="history/[id]" options={{ animation: 'slide_from_right' }} />
        </Stack>
      </View>
    </ThemeProvider>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  }
});
