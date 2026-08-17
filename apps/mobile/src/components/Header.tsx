import { View, Text, StyleSheet } from "react-native";
import { useThemeStore } from "../stores/themeStore";
import { lightColors, darkColors } from "../theme/colors";

interface HeaderProps {
  title: string;
}

export function Header({ title }: HeaderProps) {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  return (
    <View style={[styles.container, { backgroundColor: colors.surface, borderBottomColor: colors.border }]}>
      <Text style={[styles.title, { color: colors.text }]}>{title}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    paddingTop: 48,
    borderBottomWidth: 1,
    alignItems: "center",
  },
  title: {
    fontSize: 18,
    fontWeight: "bold",
  },
});
