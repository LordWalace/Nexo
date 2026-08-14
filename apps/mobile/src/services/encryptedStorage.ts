import AsyncStorage from '@react-native-async-storage/async-storage';
import { encode, decode } from 'base-64';
import { logger } from '../utils/logger';

// Função de ofuscação simples (Base64 + URI encode) para não depender de módulos nativos
function obfuscateData(text: string): string {
  return encode(encodeURIComponent(text));
}

function deobfuscateData(encoded: string): string {
  return decodeURIComponent(decode(encoded));
}

export async function saveEncryptedData<T>(key: string, data: T): Promise<void> {
  try {
    const jsonValue = JSON.stringify(data);
    const obfuscatedValue = obfuscateData(jsonValue);
    
    await AsyncStorage.setItem(key, obfuscatedValue);
  } catch (error) {
    logger.error(`Erro ao salvar dados ofuscados na chave: ${key}`, error);
  }
}

export async function loadEncryptedData<T>(key: string): Promise<T | null> {
  try {
    const obfuscatedValue = await AsyncStorage.getItem(key);
    if (!obfuscatedValue) return null;
    
    // Tratamento caso haja dados salvos no formato antigo (antes da ofuscação)
    if (obfuscatedValue.startsWith('{') || obfuscatedValue.startsWith('[')) {
      return JSON.parse(obfuscatedValue);
    }
    
    const decryptedJson = deobfuscateData(obfuscatedValue);
    if (!decryptedJson) return null;
    
    try {
      return JSON.parse(decryptedJson);
    } catch (parseError) {
      // Se não for possível fazer o parse (ex: formato antigo do crypto-js), ignora e retorna null
      return null;
    }
  } catch (error) {
    logger.error(`Erro ao carregar dados ofuscados da chave: ${key}`, error);
    return null;
  }
}

export async function removeEncryptedData(key: string): Promise<void> {
  try {
    await AsyncStorage.removeItem(key);
  } catch (error) {
    logger.error(`Erro ao remover dados criptografados da chave: ${key}`, error);
  }
}
