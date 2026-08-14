import * as Notifications from 'expo-notifications';
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Activity } from '../stores/useDataStore';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
    shouldShowBanner: true,
    shouldShowList: true,
  }),
});

export const requestNotificationPermissions = async () => {
  const { status } = await Notifications.getPermissionsAsync();
  if (status !== 'granted') {
    await Notifications.requestPermissionsAsync();
  }
};

export const scheduleActivityNotifications = async (activity: Activity) => {
  if (!activity.startTime) return;

  const notificationsEnabled = await AsyncStorage.getItem("@nexo:notificationsEnabled");
  if (notificationsEnabled === "false") return;

  // By default, if not explicitly set to false, we assume true
  const notifyBefore30Min = await AsyncStorage.getItem("@nexo:notifyBefore30Min") !== "false";
  const notifyBefore10Min = await AsyncStorage.getItem("@nexo:notifyBefore10Min") !== "false";

  const startTime = new Date(activity.startTime);
  const now = new Date();

  // 30 min antes
  if (notifyBefore30Min) {
    const trigger30 = new Date(startTime.getTime() - 30 * 60000);
    if (trigger30 > now) {
      await Notifications.scheduleNotificationAsync({
        content: {
          title: 'Atividade em 30 minutos!',
          body: `Sua atividade "${activity.title}" começará em breve.`,
          data: { activityId: activity.id, recurringGroupId: activity.recurringGroupId },
        },
        trigger: { type: Notifications.SchedulableTriggerInputTypes.DATE, date: trigger30 },
      });
    }
  }

  // 10 min antes
  if (notifyBefore10Min) {
    const trigger10 = new Date(startTime.getTime() - 10 * 60000);
    if (trigger10 > now) {
      await Notifications.scheduleNotificationAsync({
        content: {
          title: 'Atividade em 10 minutos!',
          body: `Prepare-se para "${activity.title}".`,
          data: { activityId: activity.id, recurringGroupId: activity.recurringGroupId },
        },
        trigger: { type: Notifications.SchedulableTriggerInputTypes.DATE, date: trigger10 },
      });
    }
  }

  // No início
  if (startTime > now) {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: 'Hora de começar!',
        body: `A atividade "${activity.title}" começou agora.`,
        data: { activityId: activity.id, recurringGroupId: activity.recurringGroupId },
      },
      trigger: { type: Notifications.SchedulableTriggerInputTypes.DATE, date: startTime },
    });
  }

  // No fim
  if (activity.endTime) {
    const endTime = new Date(activity.endTime);
    if (endTime > now) {
      await Notifications.scheduleNotificationAsync({
        content: {
          title: 'Atividade finalizada',
          body: `O tempo estimado para "${activity.title}" acabou.`,
          data: { activityId: activity.id, recurringGroupId: activity.recurringGroupId },
        },
        trigger: { type: Notifications.SchedulableTriggerInputTypes.DATE, date: endTime },
      });
    }
  }
};

export const cancelActivityNotifications = async (activityId: string) => {
  const scheduled = await Notifications.getAllScheduledNotificationsAsync();
  for (const notif of scheduled) {
    const data = notif.content.data as { activityId?: string };
    if (data && data.activityId === activityId) {
      await Notifications.cancelScheduledNotificationAsync(notif.identifier);
    }
  }
};

export const cancelRecurringGroupNotifications = async (groupId: string) => {
  const scheduled = await Notifications.getAllScheduledNotificationsAsync();
  for (const notif of scheduled) {
    const data = notif.content.data as { recurringGroupId?: string };
    if (data && data.recurringGroupId === groupId) {
      await Notifications.cancelScheduledNotificationAsync(notif.identifier);
    }
  }
};
