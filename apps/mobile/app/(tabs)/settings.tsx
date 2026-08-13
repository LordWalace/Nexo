import { View, StyleSheet, Switch, ScrollView } from "react-native";
import React, { useState, useEffect } from "react";
import { useThemeStore } from "../../src/stores/themeStore";
import { useAuthStore } from "../../src/stores/useAuthStore";
import { lightColors, darkColors } from "../../src/theme/colors";
import { Card } from "../../src/components/Card";
import { Button } from "../../src/components/Button";
import { Text } from "../../src/components/Text";
import { useRouter } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function Settings() {
  const { theme, toggleTheme } = useThemeStore();
  const { userName, setUserName } = useAuthStore();
  const colors = theme === "light" ? lightColors : darkColors;
  const router = useRouter();

  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [notifyBefore30Min, setNotifyBefore30Min] = useState(true);
  const [notifyBefore10Min, setNotifyBefore10Min] = useState(true);

  useEffect(() => {
    AsyncStorage.getItem("@nexo:notificationsEnabled").then(val => {
      if (val !== null) setNotificationsEnabled(val === "true");
    });
    AsyncStorage.getItem("@nexo:notifyBefore30Min").then(val => {
      if (val !== null) setNotifyBefore30Min(val === "true");
    });
    AsyncStorage.getItem("@nexo:notifyBefore10Min").then(val => {
      if (val !== null) setNotifyBefore10Min(val === "true");
    });
  }, []);

  const toggleNotifications = (val: boolean) => {
    setNotificationsEnabled(val);
    AsyncStorage.setItem("@nexo:notificationsEnabled", val.toString());
  };

  const toggleNotify30Min = (val: boolean) => {
    setNotifyBefore30Min(val);
    AsyncStorage.setItem("@nexo:notifyBefore30Min", val.toString());
  };

  const toggleNotify10Min = (val: boolean) => {
    setNotifyBefore10Min(val);
    AsyncStorage.setItem("@nexo:notifyBefore10Min", val.toString());
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      
      <ScrollView contentContainerStyle={styles.content}>
        
        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>PERFIL</Text>
        <Card>
          <Text style={[styles.profileName, { color: colors.text }]}>{userName || "Visitante"}</Text>
          
          <View style={styles.buttonSpacing}>
            <Button title="Editar Perfil" color="#4A6B69" onPress={() => router.push("/settings/profile")} />
          </View>
          
          <View style={styles.buttonSpacing}>
            <Button title="Entrar com Google" color="#4A6B69" onPress={() => {}} />
          </View>
        </Card>

        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>NOTIFICAÇÕES</Text>
        <Card>
          <View style={styles.row}>
            <Text style={[styles.rowText, { color: colors.text }]}>Ativar notificações</Text>
            <Switch value={notificationsEnabled} onValueChange={toggleNotifications} trackColor={{ true: colors.primary }} />
          </View>
          {notificationsEnabled && (
            <>
              <View style={[styles.row, { marginTop: 16 }]}>
                <Text style={[styles.rowText, { color: colors.text }]}>Avisar 30 min antes</Text>
                <Switch value={notifyBefore30Min} onValueChange={toggleNotify30Min} trackColor={{ true: colors.primary }} />
              </View>
              <View style={[styles.row, { marginTop: 16 }]}>
                <Text style={[styles.rowText, { color: colors.text }]}>Avisar 10 min antes</Text>
                <Switch value={notifyBefore10Min} onValueChange={toggleNotify10Min} trackColor={{ true: colors.primary }} />
              </View>
            </>
          )}
        </Card>

        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>APARÊNCIA</Text>
        <Card>
          <View style={styles.row}>
            <Text style={[styles.rowText, { color: colors.text }]}>Tema Escuro</Text>
            <Switch value={theme === "dark"} onValueChange={toggleTheme} trackColor={{ true: colors.primary }} />
          </View>
        </Card>

      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 16,
    paddingBottom: 48,
  },
  sectionTitle: {
    fontSize: 12,
    fontWeight: "bold",
    marginTop: 24,
    marginBottom: 8,
    marginLeft: 4,
  },
  profileName: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 4,
  },
  buttonSpacing: {
    marginTop: 12,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  rowText: {
    fontSize: 16,
  }
});
