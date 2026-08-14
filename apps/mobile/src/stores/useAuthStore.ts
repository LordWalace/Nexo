import { create } from 'zustand';
import { saveUserProfile, getUserProfile, clearUserProfile } from '../services/secureStorage';

interface AuthState {
  userName: string | null;
  loadUserName: () => Promise<void>;
  setUserName: (name: string) => void;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  userName: null,
  loadUserName: async () => {
    const profile = await getUserProfile();
    if (profile?.name) set({ userName: profile.name });
  },
  setUserName: async (name) => {
    set({ userName: name });
    // Generating dummy ID and email for demonstration, as we only had userName before
    await saveUserProfile({ id: 'local-user', name, email: '' });
  },
  logout: async () => {
    set({ userName: null });
    await clearUserProfile();
  }
}));
