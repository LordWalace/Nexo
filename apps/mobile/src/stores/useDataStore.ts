import { create } from 'zustand';
import { saveData, loadData } from '../services/storage';
import * as Crypto from 'expo-crypto';
import { scheduleActivityNotifications, cancelActivityNotifications, cancelRecurringGroupNotifications } from '../services/notifications';

export interface Activity {
  id: string;
  title: string;
  description?: string;
  categoryId?: string;
  startTime?: string;
  endTime?: string;
  durationMs?: number; // Calculated duration
  deleted?: boolean; // Soft delete
  recurringGroupId?: string;
}

export interface Category {
  id: string;
  name: string;
  description?: string;
}

export interface Material {
  id: string;
  name: string;
  type: string;
  link?: string;
  activityId?: string;
  categoryId?: string;
}

export interface HistorySession {
  id: string;
  activityId: string;
  startTime: string;
  endTime?: string;
  durationMs?: number;
}

interface DataState {
  activities: Activity[];
  categories: Category[];
  materials: Material[];
  history: HistorySession[];
  
  loadAllData: () => Promise<void>;
  
  addActivity: (activity: Omit<Activity, 'id'>) => void;
  addActivities: (newActivities: Omit<Activity, 'id'>[]) => void;
  updateActivity: (id: string, activity: Partial<Activity>) => void;
  deleteActivity: (id: string) => void;
  deleteRecurringGroup: (groupId: string) => void;
  recoverActivity: (id: string) => void; // Recover soft-deleted activity
  
  addCategory: (category: Omit<Category, 'id'>) => void;
  updateCategory: (id: string, category: Partial<Category>) => void;
  deleteCategory: (id: string) => void;
  
  addMaterial: (material: Omit<Material, 'id'>) => void;
  updateMaterial: (id: string, material: Partial<Material>) => void;
  deleteMaterial: (id: string) => void;
  
  startSession: (activityId: string) => void;
  finishSession: (sessionId: string) => void;
  deleteHistorySession: (id: string) => void;
}

export const useDataStore = create<DataState>((set, get) => ({
  activities: [],
  categories: [],
  materials: [],
  history: [],

  loadAllData: async () => {
    const activities = (await loadData('@nexo:activities')) || [];
    const categories = (await loadData('@nexo:categories')) || [];
    const materials = (await loadData('@nexo:materials')) || [];
    const history = (await loadData('@nexo:history')) || [];
    set({ activities, categories, materials, history });
  },

  addActivity: (activity) => {
    // Calculate duration automatically if start and end are provided
    let durationMs = activity.durationMs;
    if (activity.startTime && activity.endTime) {
      durationMs = new Date(activity.endTime).getTime() - new Date(activity.startTime).getTime();
    }
    const newActivity = { ...activity, durationMs, id: Crypto.randomUUID(), deleted: false };
    const activities = [...get().activities, newActivity];
    set({ activities });
    saveData('@nexo:activities', activities);
    scheduleActivityNotifications(newActivity);
  },
  addActivities: (newActivities) => {
    const prepared = newActivities.map(activity => {
      let durationMs = activity.durationMs;
      if (activity.startTime && activity.endTime) {
        durationMs = new Date(activity.endTime).getTime() - new Date(activity.startTime).getTime();
      }
      return { ...activity, durationMs, id: Crypto.randomUUID(), deleted: false };
    });
    const activities = [...get().activities, ...prepared];
    set({ activities });
    saveData('@nexo:activities', activities);
    prepared.forEach(act => scheduleActivityNotifications(act));
  },
  updateActivity: (id, data) => {
    let durationMs = data.durationMs;
    const existing = get().activities.find(a => a.id === id);
    const start = data.startTime || existing?.startTime;
    const end = data.endTime || existing?.endTime;
    if (start && end) {
      durationMs = new Date(end).getTime() - new Date(start).getTime();
    }
    const activities = get().activities.map(a => a.id === id ? { ...a, ...data, durationMs } : a);
    set({ activities });
    saveData('@nexo:activities', activities);
    
    // Reschedule if times changed
    if (data.startTime || data.endTime || data.deleted === true) {
      cancelActivityNotifications(id).then(() => {
        if (!data.deleted) {
          const updated = get().activities.find(a => a.id === id);
          if (updated) scheduleActivityNotifications(updated);
        }
      });
    }
  },
  deleteActivity: (id) => {
    const activities = get().activities.map(a => a.id === id ? { ...a, deleted: true } : a);
    set({ activities });
    saveData('@nexo:activities', activities);
    cancelActivityNotifications(id);
  },
  deleteRecurringGroup: (groupId) => {
    const activities = get().activities.map(a => a.recurringGroupId === groupId ? { ...a, deleted: true } : a);
    set({ activities });
    saveData('@nexo:activities', activities);
    cancelRecurringGroupNotifications(groupId);
  },
  recoverActivity: (id) => {
    const activities = get().activities.map(a => a.id === id ? { ...a, deleted: false } : a);
    set({ activities });
    saveData('@nexo:activities', activities);
    const recovered = get().activities.find(a => a.id === id);
    if (recovered) scheduleActivityNotifications(recovered);
  },

  addCategory: (category) => {
    const newCategory = { ...category, id: Crypto.randomUUID() };
    const categories = [...get().categories, newCategory];
    set({ categories });
    saveData('@nexo:categories', categories);
  },
  updateCategory: (id, data) => {
    const categories = get().categories.map(c => c.id === id ? { ...c, ...data } : c);
    set({ categories });
    saveData('@nexo:categories', categories);
  },
  deleteCategory: (id) => {
    const categories = get().categories.filter(c => c.id !== id);
    set({ categories });
    saveData('@nexo:categories', categories);
  },

  addMaterial: (material) => {
    const newMaterial = { ...material, id: Crypto.randomUUID() };
    const materials = [...get().materials, newMaterial];
    set({ materials });
    saveData('@nexo:materials', materials);
  },
  updateMaterial: (id, data) => {
    const materials = get().materials.map(m => m.id === id ? { ...m, ...data } : m);
    set({ materials });
    saveData('@nexo:materials', materials);
  },
  deleteMaterial: (id) => {
    const materials = get().materials.filter(m => m.id !== id);
    set({ materials });
    saveData('@nexo:materials', materials);
  },

  startSession: (activityId) => {
    const newSession: HistorySession = {
      id: Crypto.randomUUID(),
      activityId,
      startTime: new Date().toISOString(),
    };
    const history = [...get().history, newSession];
    set({ history });
    saveData('@nexo:history', history);
  },
  finishSession: (sessionId) => {
    const history = get().history.map(h => {
      if (h.id === sessionId && !h.endTime) {
        const endTime = new Date();
        const startTime = new Date(h.startTime);
        const durationMs = endTime.getTime() - startTime.getTime();
        return { ...h, endTime: endTime.toISOString(), durationMs };
      }
      return h;
    });
    set({ history });
    saveData('@nexo:history', history);
  },
  deleteHistorySession: (id) => {
    const history = get().history.filter(h => h.id !== id);
    set({ history });
    saveData('@nexo:history', history);
  }
}));
