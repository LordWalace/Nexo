import AsyncStorage from '@react-native-async-storage/async-storage';
import { logger } from '../utils/logger';

export const saveData = async (key: string, data: any) => {
  try {
    const jsonValue = JSON.stringify(data);
    await AsyncStorage.setItem(key, jsonValue);
  } catch (e) {
    logger.error(`Erro ao salvar dados (AsyncStorage) para a chave: ${key}`, e);
  }
};

export const loadData = async (key: string) => {
  try {
    const jsonValue = await AsyncStorage.getItem(key);
    return jsonValue != null ? JSON.parse(jsonValue) : null;
  } catch (e) {
    logger.error(`Erro ao carregar dados (AsyncStorage) da chave: ${key}`, e);
    return null;
  }
};

export const removeData = async (key: string) => {
  try {
    await AsyncStorage.removeItem(key);
  } catch (e) {
    logger.error(`Erro ao remover dados (AsyncStorage) da chave: ${key}`, e);
  }
};
