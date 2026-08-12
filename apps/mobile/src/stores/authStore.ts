import { create } from "zustand";
import AsyncStorage from "@react-native-async-storage/async-storage";
import * as SecureStore from "expo-secure-store";
import "react-native-get-random-values";
import { v4 as uuidv4 } from "uuid";

interface AuthState {
  localUserId: string | null;
  accessToken: string | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  initialize: () => Promise<void>;
  login: (token: string) => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  localUserId: null,
  accessToken: null,
  isLoggedIn: false,
  isLoading: true,
  initialize: async () => {
    try {
      // 1. Load or create localUserId
      let localId = await AsyncStorage.getItem("@nexo_local_user_id");
      if (!localId) {
        localId = uuidv4();
        await AsyncStorage.setItem("@nexo_local_user_id", localId);
      }
      
      // 2. Check for access token
      const token = await SecureStore.getItemAsync("access_token");
      
      set({ 
        localUserId: localId, 
        accessToken: token, 
        isLoggedIn: !!token,
        isLoading: false 
      });
    } catch (e) {
      set({ isLoading: false });
    }
  },
  login: async (token) => {
    await SecureStore.setItemAsync("access_token", token);
    set({ accessToken: token, isLoggedIn: true });
  },
  logout: async () => {
    await SecureStore.deleteItemAsync("access_token");
    set({ accessToken: null, isLoggedIn: false });
  }
}));

