import React, { useEffect, useRef } from 'react';
import { Animated, ViewStyle, StyleProp, View } from 'react-native';
import Svg, { Circle, Rect, Polygon } from 'react-native-svg';

interface LogoGeometryProps {
  size?: number;
  color?: string;
  style?: StyleProp<ViewStyle>;
  animated?: boolean;
}

export function LogoGeometry({
  size = 100,
  color = '#000',
  style,
  animated = false,
}: LogoGeometryProps) {
  const triAnim = useRef(new Animated.Value(1)).current;
  const circAnim = useRef(new Animated.Value(1)).current;
  const sqAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (animated) {
      triAnim.setValue(0);
      circAnim.setValue(0);
      sqAnim.setValue(0);

      const createSequence = (target: Animated.Value) => 
        Animated.sequence([
          Animated.parallel([
            Animated.timing(target, { toValue: 1, duration: 400, useNativeDriver: true }),
          ]),
          Animated.delay(600),
          Animated.timing(target, { toValue: 0, duration: 400, useNativeDriver: true }),
        ]);

      Animated.loop(
        Animated.sequence([
          createSequence(triAnim),
          createSequence(circAnim),
          createSequence(sqAnim),
        ])
      ).start();
    } else {
      triAnim.setValue(1);
      circAnim.setValue(1);
      sqAnim.setValue(1);
    }
  }, [animated, triAnim, circAnim, sqAnim]);

  const getStyle = (animValue: Animated.Value) => ({
    position: 'absolute' as const,
    width: size,
    height: size,
    opacity: animValue,
    transform: [
      {
        scale: animValue.interpolate({
          inputRange: [0, 1],
          outputRange: [0.5, 1],
        }),
      },
    ],
  });

  return (
    <View style={[style, { width: size, height: size }]}>
      {/* Triângulo (Topo) */}
      <Animated.View style={getStyle(triAnim)}>
        <Svg width={size} height={size} viewBox="0 0 100 100">
          <Polygon
            points="50,15 65,41 35,41"
            stroke={color}
            strokeWidth="6"
            fill="transparent"
            strokeLinejoin="round"
            strokeLinecap="round"
          />
        </Svg>
      </Animated.View>

      {/* Círculo (Inferior Esquerdo) */}
      <Animated.View style={getStyle(circAnim)}>
        <Svg width={size} height={size} viewBox="0 0 100 100">
          <Circle
            cx="25"
            cy="75"
            r="15"
            stroke={color}
            strokeWidth="6"
            fill="transparent"
          />
        </Svg>
      </Animated.View>

      {/* Quadrado (Inferior Direito) */}
      <Animated.View style={getStyle(sqAnim)}>
        <Svg width={size} height={size} viewBox="0 0 100 100">
          <Rect
            x="60"
            y="60"
            width="30"
            height="30"
            stroke={color}
            strokeWidth="6"
            fill="transparent"
            strokeLinejoin="round"
            strokeLinecap="round"
          />
        </Svg>
      </Animated.View>
    </View>
  );
}
