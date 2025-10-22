import { API_CONFIG, getApiUrl, getAuthHeaders } from '@/config/api';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  is_active: boolean;
  is_verified: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
  last_login: string | null;
  watchlist: string[];
  preferred_sectors: string[];
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || API_CONFIG.BASE_URL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = getApiUrl(endpoint);
    const token = localStorage.getItem('access_token');

    const config: RequestInit = {
      headers: {
        ...getAuthHeaders(token || undefined),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        return { error: data.detail || 'An error occurred' };
      }

      return { data };
    } catch (error) {
      return { 
        error: error instanceof Error ? error.message : 'Network error' 
      };
    }
  }

  // Authentication methods
  async login(email: string, password: string) {
    return this.request<{ access_token: string; token_type: string }>(API_CONFIG.ENDPOINTS.AUTH.LOGIN, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(email: string, name: string, password: string) {
    return this.request(API_CONFIG.ENDPOINTS.AUTH.REGISTER, {
      method: 'POST',
      body: JSON.stringify({ email, name, password }),
    });
  }

  // User methods
  async getCurrentUser() {
    return this.request<User>('/users/me');
  }

  async updateUser(userId: string, userData: any) {
    return this.request(`${API_CONFIG.ENDPOINTS.USERS.BASE}/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  // Stock methods
  async getStocks() {
    return this.request(API_CONFIG.ENDPOINTS.STOCKS.BASE);
  }

  async getStock(stockId: string) {
    return this.request(API_CONFIG.ENDPOINTS.STOCKS.BY_ID(stockId));
  }

  async addToWatchlist(userId: string, stockSymbol: string) {
    return this.request(`${API_CONFIG.ENDPOINTS.USERS.BASE}/${userId}/watchlist/${stockSymbol}`, {
      method: 'POST',
    });
  }

  async removeFromWatchlist(userId: string, stockSymbol: string) {
    return this.request(`${API_CONFIG.ENDPOINTS.USERS.BASE}/${userId}/watchlist/${stockSymbol}`, {
      method: 'DELETE',
    });
  }

  async getWatchlist(userId: string) {
    return this.request(API_CONFIG.ENDPOINTS.USERS.WATCHLIST(userId));
  }

  async getCompanies() {
    return this.request(API_CONFIG.ENDPOINTS.STOCKS.COMPANIES);
  }
}

export const apiClient = new ApiClient();
