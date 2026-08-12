import { useEffect } from "react";
import { Stack } from "expo-router";
import { useAuthStore } from "../src/stores/authStore";
import { useThemeStore } from "../src/stores/themeStore";

export default function RootLayout() {
  const { initialize, isLoading } = useAuthStore();
  const { loadTheme } = useThemeStore();

  useEffect(() => {
    loadTheme();
    initialize();
  }, []);

  if (isLoading) {
    return null; // or a splash screen
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="(tabs)" />
      <Stack.Screen name="(auth)" options={{ presentation: "modal" }} />
    </Stack>
  );
}

