import { initializeApp } from 'firebase/app';
import { initializeAuth, getReactNativePersistence } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Sua configuração do Firebase (obtida do Firebase Console)
const firebaseConfig = {
  apiKey: "AIzaSyDx8LDZhWaM7wg5XvEoHZULukL7OO2bdIc",
  authDomain: "nexo-9bca5.firebaseapp.com",
  projectId: "nexo-9bca5",
  storageBucket: "nexo-9bca5.firebasestorage.app",
  messagingSenderId: "270618831747",
  appId: "1:270618831747:web:6f205867d7bfe4765ce4b6",
  measurementId: "G-2DLPY5JDWB"
};

// Inicializa o Firebase
const app = initializeApp(firebaseConfig);

// Inicializa o Authentication com AsyncStorage para React Native
export const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(AsyncStorage)
});

// Inicializa o Cloud Firestore (Banco de Dados)
export const db = getFirestore(app);

export default app;
