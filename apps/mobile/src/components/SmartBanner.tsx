import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Platform, Linking, Image } from 'react-native';

export function SmartBanner() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Só renderiza na web. Se for Android/iOS, não faz nada.
    if (Platform.OS !== 'web') return;

    // Detectar mobile simplificado no navegador
    const userAgent = typeof window !== 'undefined' ? window.navigator.userAgent : '';
    const isMobileWeb = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
    
    // Evitar irritar o usuário que já fechou
    const isDismissed = typeof sessionStorage !== 'undefined' && sessionStorage.getItem('smart_banner_dismissed') === 'true';

    if (isMobileWeb && !isDismissed) {
      setIsVisible(true);
    }
  }, []);

  const handleDismiss = () => {
    setIsVisible(false);
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.setItem('smart_banner_dismissed', 'true');
    }
  };

  const handleDownload = () => {
    Linking.openURL('https://github.com/LordWalace/Nexo/releases/latest');
  };

  if (!isVisible) return null;

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <View style={styles.iconContainer}>
          {/* Pode trocar por um ícone local futuramente */}
          <View style={styles.placeholderIcon} />
        </View>
        <View style={styles.textContainer}>
          <Text style={styles.title}>Nexo App</Text>
          <Text style={styles.subtitle}>A experiência é melhor no app!</Text>
        </View>
      </View>
      
      <View style={styles.actions}>
        <TouchableOpacity style={styles.downloadBtn} onPress={handleDownload}>
          <Text style={styles.downloadText}>Baixar APK</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.closeBtn} onPress={handleDismiss}>
          <Text style={styles.closeText}>×</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'rgba(20, 20, 25, 0.95)',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 9999,
  },
  content: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  iconContainer: {
    width: 40,
    height: 40,
    backgroundColor: '#fff',
    borderRadius: 8,
    marginRight: 12,
  },
  placeholderIcon: {
    flex: 1,
    backgroundColor: '#6366f1',
    borderRadius: 8,
  },
  textContainer: {
    flex: 1,
  },
  title: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 2,
  },
  subtitle: {
    color: 'rgba(255, 255, 255, 0.7)',
    fontSize: 12,
  },
  actions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  downloadBtn: {
    backgroundColor: '#a855f7',
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 20,
    marginRight: 12,
  },
  downloadText: {
    color: '#fff',
    fontSize: 13,
    fontWeight: '600',
  },
  closeBtn: {
    padding: 4,
  },
  closeText: {
    color: 'rgba(255, 255, 255, 0.5)',
    fontSize: 24,
    lineHeight: 24,
  },
});
