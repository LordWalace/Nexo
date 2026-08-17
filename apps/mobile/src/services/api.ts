import { getAuthTokens } from './secureStorage';
import { logger } from '../utils/logger';

// Example API Service using fetch
const BASE_URL = 'https://api.nexo.app.br/v1'; // Always use HTTPS

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  try {
    const tokens = await getAuthTokens();
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (tokens?.accessToken) {
      headers['Authorization'] = `Bearer ${tokens.accessToken}`;
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      logger.error(`API Error: ${response.status}`, { endpoint });
      throw new Error(`API returned ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    logger.error('API Request Failed', { endpoint });
    throw error;
  }
}
