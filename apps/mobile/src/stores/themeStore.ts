import { create } from "zustand";
import AsyncStorage from "@react-native-async-storage/async-storage";

interface ThemeState {
  theme: "light" | "dark" | "system";
  setTheme: (theme: "light" | "dark" | "system") => void;
  loadTheme: () => Promise<void>;
}

export const useThemeStore = create<ThemeState>((set) => ({
  theme: "system",
  setTheme: async (theme) => {
    set({ theme });
    await AsyncStorage.setItem("@nexo_theme", theme);
  },
  loadTheme: async () => {
    const saved = await AsyncStorage.getItem("@nexo_theme");
    if (saved === "light" || saved === "dark" || saved === "system") {
      set({ theme: saved });
    }
  },
}));

