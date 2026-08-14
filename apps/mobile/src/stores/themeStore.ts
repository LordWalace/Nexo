import { create } from "zustand";
import AsyncStorage from "@react-native-async-storage/async-storage";

interface ThemeState {
  theme: "light" | "dark" | "system";
  setTheme: (theme: "light" | "dark" | "system") => void;
  toggleTheme: () => void;
  loadTheme: () => Promise<void>;
}

export const useThemeStore = create<ThemeState>((set, get) => ({
  theme: "system",
  setTheme: async (theme) => {
    set({ theme });
    await AsyncStorage.setItem("@nexo_theme", theme);
  },
  toggleTheme: async () => {
    const newTheme = get().theme === "dark" ? "light" : "dark";
    set({ theme: newTheme });
    await AsyncStorage.setItem("@nexo_theme", newTheme);
  },
  loadTheme: async () => {
    const saved = await AsyncStorage.getItem("@nexo_theme");
    if (saved === "light" || saved === "dark" || saved === "system") {
      set({ theme: saved });
    }
  },
}));

