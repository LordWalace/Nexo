import { useAuthStore } from "../stores/authStore";

export const scheduleNotification = (activityTitle: string, minutesBefore: number = 10) => {
  const name = useAuthStore.getState().name;
  const greeting = name ? `, ${name}` : "";
  
  console.log(`[Notification Scheduled]: Falta ${minutesBefore} minutos para iniciar sua atividade "${activityTitle}"${greeting}.`);
  // Lógica real do expo-notifications seria implementada aqui
};
