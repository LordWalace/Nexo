import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import AsyncStorage from "@react-native-async-storage/async-storage";
import "react-native-get-random-values";
import { v4 as uuidv4 } from "uuid";

interface AuthState {
  userId: string;
  name: string;
  email: string | null;
  isAnonymous: boolean;
  setProfile: (name: string, email?: string | null) => void;
  login: (email: string, name: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      userId: uuidv4(),
      name: "",
      email: null,
      isAnonymous: true,
      setProfile: (name, email = null) => set({ name, email }),
      login: (email, name) => set({ email, name, isAnonymous: false }),
      logout: () => set({ email: null, isAnonymous: true }),
    }),
    {
      name: "auth-storage",
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
