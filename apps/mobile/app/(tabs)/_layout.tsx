import { View } from "react-native";
import { Tabs, useRouter, useSegments } from "expo-router";
import { useThemeStore } from "../../src/stores/themeStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Home, ListTodo, History, Settings } from "lucide-react-native";
import { FAB } from "../../src/components/FAB";

export default function TabLayout() {
  const { theme } = useThemeStore();
  const colors = theme === "dark" ? darkColors : lightColors;
  const router = useRouter();
  const segments = useSegments();
  
  // Hide FAB if on settings screen
  const isSettings = segments[segments.length - 1] === "settings";

  return (
    <View style={{ flex: 1 }}>
      <Tabs
        screenOptions={{
          headerShown: true,
          headerTitleAlign: 'center',
          headerStyle: { backgroundColor: colors.surface },
          headerTintColor: colors.text,
          tabBarStyle: { backgroundColor: colors.surface, borderTopColor: colors.border },
          tabBarActiveTintColor: colors.primary,
          tabBarInactiveTintColor: colors.textSecondary,
        }}
        sceneContainerStyle={{ backgroundColor: 'transparent' }}
      >
        <Tabs.Screen
          name="index"
          options={{
            title: "Início",
            headerShown: false,
            tabBarIcon: ({ color }) => <Home color={color} size={24} />,
          }}
        />
        <Tabs.Screen
          name="activities"
          options={{
            title: "Atividades",
            tabBarIcon: ({ color }) => <ListTodo color={color} size={24} />,
          }}
        />
        <Tabs.Screen
          name="history"
          options={{
            title: "Histórico",
            tabBarIcon: ({ color }) => <History color={color} size={24} />,
          }}
        />
        <Tabs.Screen
          name="settings"
          options={{
            title: "Configurações",
            tabBarIcon: ({ color }) => <Settings color={color} size={24} />,
          }}
        />
      </Tabs>
      {!isSettings && <FAB onActionPress={() => router.push('/activities/new')} actionText="Criar nova tarefa" />}
    </View>
  );
}
