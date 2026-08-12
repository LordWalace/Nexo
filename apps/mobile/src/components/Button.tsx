import { TouchableOpacity, Text, StyleSheet } from "react-native";
import { useThemeStore } from "../stores/themeStore";
import { lightColors, darkColors } from "../theme/colors";

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: "primary" | "secondary";
}

export function Button({ title, onPress, variant = "primary" }: ButtonProps) {
  const { theme } = useThemeStore();
  const colors = theme === "light" ? lightColors : darkColors;

  const isPrimary = variant === "primary";
  const bgColor = isPrimary ? colors.accent : colors.surface;
  const textColor = isPrimary ? "#FFFFFF" : colors.accent;
  const borderColor = isPrimary ? "transparent" : colors.border;

  return (
    <TouchableOpacity
      style={[styles.button, { backgroundColor: bgColor, borderColor, borderWidth: isPrimary ? 0 : 1 }]}
      onPress={onPress}
      activeOpacity={0.8}
    >
      <Text style={[styles.text, { color: textColor }]}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
  },
  text: {
    fontSize: 16,
    fontWeight: "bold",
  }
});
