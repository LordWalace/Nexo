import React, { useEffect, useRef } from 'react';
import { Animated, ViewStyle, StyleProp } from 'react-native';
import Svg, { Circle, Rect, Polygon } from 'react-native-svg';

interface LogoGeometryProps {
  size?: number;
  color?: string;
  style?: StyleProp<ViewStyle>;
  animated?: boolean;
}

const AnimatedSvg = Animated.createAnimatedComponent(Svg);

export function LogoGeometry({
  size = 100,
  color = '#000',
  style,
  animated = false,
}: LogoGeometryProps) {
  const rotation = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (animated) {
      Animated.loop(
        Animated.timing(rotation, {
          toValue: 1,
          duration: 3000,
          useNativeDriver: true,
        })
      ).start();
    } else {
      rotation.setValue(0);
    }
  }, [animated, rotation]);

  const spin = rotation.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg']
  });

  return (
    <AnimatedSvg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      style={[style, animated && { transform: [{ rotate: spin }] }]}
    >
      {/* Triângulo */}
      <Polygon
        points="50,15 85,70 15,70"
        stroke={color}
        strokeWidth="6"
        fill="transparent"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      {/* Quadrado */}
      <Rect
        x="40"
        y="30"
        width="45"
        height="45"
        stroke={color}
        strokeWidth="6"
        fill="transparent"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      {/* Círculo */}
      <Circle
        cx="40"
        cy="55"
        r="22"
        stroke={color}
        strokeWidth="6"
        fill="transparent"
      />
    </AnimatedSvg>
  );
}
