import { View, StyleSheet, TouchableOpacity } from "react-native";
import { useThemeStore } from "../stores/themeStore";
import { lightColors, darkColors } from "../theme/colors";

interface CardProps {
  children: React.ReactNode;
  onPress?: () => void;
}

export function Card({ children, onPress }: CardProps) {
  const { theme } = useThemeStore();
  const colors = theme === 'dark' ? darkColors : lightColors;

  const cardStyle = [styles.card, { backgroundColor: colors.surface, borderColor: colors.border }];

  if (onPress) {
    return (
      <TouchableOpacity style={cardStyle} onPress={onPress} activeOpacity={0.7}>
        {children}
      </TouchableOpacity>
    );
  }

  return (
    <View style={cardStyle}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    marginBottom: 16,
    elevation: 2,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  }
});
