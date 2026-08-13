import { create } from 'zustand';
import { saveData, loadData } from '../services/storage';

interface AuthState {
  userName: string | null;
  loadUserName: () => Promise<void>;
  setUserName: (name: string) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  userName: null,
  loadUserName: async () => {
    const name = await loadData('@nexo:userName');
    if (name) set({ userName: name });
  },
  setUserName: (name) => {
    set({ userName: name });
    saveData('@nexo:userName', name);
  },
}));
