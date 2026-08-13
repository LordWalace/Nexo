import { useEffect } from "react";
import { Stack } from "expo-router";
import { useAuthStore } from "../src/stores/authStore";
import { useThemeStore } from "../src/stores/themeStore";

export default function RootLayout() {
  const { loadTheme } = useThemeStore();

  useEffect(() => {
    loadTheme();
  }, []);

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="(tabs)" />
      <Stack.Screen name="(auth)" options={{ presentation: "modal" }} />
    </Stack>
  );
}

