import React, { useEffect, useRef } from 'react';
import { StyleSheet, View, Animated, Easing } from 'react-native';
import Svg, { Circle, Rect, Polygon } from 'react-native-svg';
import { useThemeStore } from '../stores/themeStore';
import { lightColors, darkColors } from '../theme/colors';

const AnimatedSvg = Animated.createAnimatedComponent(Svg);

interface ShapeConfig {
  id: number;
  type: 'circle' | 'rect' | 'triangle';
  size: number;
  initialX: number;
  initialY: number;
  travelDistance: number;
  duration: number;
  opacity: number;
}

const SHAPES: ShapeConfig[] = [
  { id: 1, type: 'circle', size: 60, initialX: 10, initialY: 10, travelDistance: 30, duration: 4000, opacity: 0.15 },
  { id: 2, type: 'circle', size: 100, initialX: 80, initialY: 80, travelDistance: -20, duration: 5500, opacity: 0.1 },
  { id: 3, type: 'rect', size: 80, initialX: 80, initialY: 10, travelDistance: 30, duration: 6000, opacity: 0.15 },
  { id: 4, type: 'rect', size: 50, initialX: 10, initialY: 80, travelDistance: -20, duration: 4500, opacity: 0.2 },
  { id: 5, type: 'triangle', size: 90, initialX: 45, initialY: 50, travelDistance: 20, duration: 7000, opacity: 0.1 },
  { id: 6, type: 'triangle', size: 45, initialX: 45, initialY: 85, travelDistance: -15, duration: 5000, opacity: 0.25 },
  { id: 7, type: 'circle', size: 75, initialX: 10, initialY: 50, travelDistance: -20, duration: 5000, opacity: 0.12 },
  { id: 8, type: 'rect', size: 65, initialX: 45, initialY: 10, travelDistance: 25, duration: 4800, opacity: 0.18 },
  { id: 9, type: 'triangle', size: 85, initialX: 80, initialY: 50, travelDistance: -20, duration: 6200, opacity: 0.14 },
];

const FloatingShape = ({ config, color }: { config: ShapeConfig; color: string }) => {
  const translateY = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const moveDown = Animated.timing(translateY, {
      toValue: config.travelDistance,
      duration: config.duration,
      easing: Easing.inOut(Easing.ease),
      useNativeDriver: true,
    });
    
    const moveUp = Animated.timing(translateY, {
      toValue: 0,
      duration: config.duration,
      easing: Easing.inOut(Easing.ease),
      useNativeDriver: true,
    });

    Animated.loop(Animated.sequence([moveDown, moveUp])).start();
  }, [config, translateY]);

  const renderShape = () => {
    const strokeWidth = 3;
    const { size } = config;
    if (config.type === 'circle') {
      return <Circle cx={size / 2} cy={size / 2} r={(size - strokeWidth) / 2} stroke={color} strokeWidth={strokeWidth} fill="transparent" />;
    }
    if (config.type === 'rect') {
      return <Rect x={strokeWidth / 2} y={strokeWidth / 2} width={size - strokeWidth} height={size - strokeWidth} stroke={color} strokeWidth={strokeWidth} fill="transparent" rx={4} ry={4} />;
    }
    if (config.type === 'triangle') {
      const p1 = `${size / 2},${strokeWidth}`;
      const p2 = `${size - strokeWidth},${size - strokeWidth}`;
      const p3 = `${strokeWidth},${size - strokeWidth}`;
      return <Polygon points={`${p1} ${p2} ${p3}`} stroke={color} strokeWidth={strokeWidth} fill="transparent" strokeLinejoin="round" />;
    }
    return null;
  };

  return (
    <Animated.View
      style={[
        styles.shape,
        {
          left: `${config.initialX}%`,
          top: `${config.initialY}%`,
          opacity: config.opacity,
          transform: [{ translateY }],
        },
      ]}
    >
      <Svg width={config.size} height={config.size}>
        {renderShape()}
      </Svg>
    </Animated.View>
  );
};

export const AnimatedBackground = () => {
  const { theme } = useThemeStore();
  const shapeColor = theme === 'dark' ? '#FFFFFF' : '#000000';

  return (
    <View style={styles.container} pointerEvents="none">
      {SHAPES.map((config) => (
        <FloatingShape key={config.id} config={config} color={shapeColor} />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
    overflow: 'hidden',
    zIndex: 0,
  },
  shape: {
    position: 'absolute',
  },
});
