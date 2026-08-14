import * as SecureStore from 'expo-secure-store';
import { logger } from '../utils/logger';

export async function saveAuthTokens(accessToken: string, refreshToken?: string): Promise<void> {
  try {
    await SecureStore.setItemAsync('nexo_access_token', accessToken);
    if (refreshToken) {
      await SecureStore.setItemAsync('nexo_refresh_token', refreshToken);
    }
    logger.info('Tokens salvos com sucesso');
  } catch (error) {
    logger.error('Erro ao salvar tokens seguros', error);
  }
}

export async function getAuthTokens(): Promise<{ accessToken: string; refreshToken?: string } | null> {
  try {
    const accessToken = await SecureStore.getItemAsync('nexo_access_token');
    const refreshToken = await SecureStore.getItemAsync('nexo_refresh_token');
    if (accessToken) {
      return { accessToken, refreshToken: refreshToken || undefined };
    }
    return null;
  } catch (error) {
    logger.error('Erro ao recuperar tokens seguros', error);
    return null;
  }
}

export async function clearAuthTokens(): Promise<void> {
  try {
    await SecureStore.deleteItemAsync('nexo_access_token');
    await SecureStore.deleteItemAsync('nexo_refresh_token');
    logger.info('Tokens removidos com sucesso');
  } catch (error) {
    logger.error('Erro ao limpar tokens seguros', error);
  }
}

export async function saveUserProfile(profile: { id: string; name: string; email?: string }): Promise<void> {
  try {
    await SecureStore.setItemAsync('nexo_user_profile', JSON.stringify(profile));
    logger.info('Perfil salvo com sucesso');
  } catch (error) {
    logger.error('Erro ao salvar perfil seguro', error);
  }
}

export async function getUserProfile(): Promise<{ id: string; name: string; email?: string } | null> {
  try {
    const profileData = await SecureStore.getItemAsync('nexo_user_profile');
    return profileData ? JSON.parse(profileData) : null;
  } catch (error) {
    logger.error('Erro ao recuperar perfil seguro', error);
    return null;
  }
}

export async function clearUserProfile(): Promise<void> {
  try {
    await SecureStore.deleteItemAsync('nexo_user_profile');
    logger.info('Perfil removido com sucesso');
  } catch (error) {
    logger.error('Erro ao limpar perfil seguro', error);
  }
}
