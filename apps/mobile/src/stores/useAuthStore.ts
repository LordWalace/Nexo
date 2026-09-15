import { create } from 'zustand';
import { onAuthStateChanged, User, signOut, updateProfile } from 'firebase/auth';
import { auth } from '../config/firebase';

interface AuthState {
  user: User | null;
  userName: string | null; // For fallback/offline mode
  isInitialized: boolean;
  initializeAuth: () => void;
  setOfflineUser: (name: string) => void;
  setUserName: (name: string) => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  userName: null,
  isInitialized: false,
  
  initializeAuth: () => {
    onAuthStateChanged(auth, (firebaseUser) => {
      set({ 
        user: firebaseUser, 
        userName: firebaseUser?.displayName || null,
        isInitialized: true 
      });
    });
  },

  setOfflineUser: (name) => {
    set({ userName: name, user: null, isInitialized: true });
  },

  setUserName: async (name) => {
    const { user } = get();
    if (user) {
      try {
        await updateProfile(user, { displayName: name });
        set({ userName: name });
      } catch (error) {
        console.error("Erro ao atualizar nome no Firebase:", error);
      }
    } else {
      set({ userName: name });
    }
  },

  logout: async () => {
    try {
      await signOut(auth);
      set({ user: null, userName: null });
    } catch (error) {
      console.error("Erro ao fazer logout:", error);
    }
  }
}));
