// API Configuration
export const API_CONFIG = {
  // Use environment variable if available, fallback to localhost for development
  BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  
  // API endpoints
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/users/login',
      REGISTER: '/users/register',
      ME: '/users/me',
    },
    USERS: {
      BASE: '/users',
      WATCHLIST: (userId: string) => `/users/${userId}/watchlist`,
      PREFERENCES: (userId: string) => `/users/${userId}/preferences`,
    },
    STOCKS: {
      BASE: '/stocks',
      BY_ID: (id: string) => `/stocks/${id}`,
      COMPANIES: '/stocks/companies',
    },
  },
  
  // Request timeout (in milliseconds)
  TIMEOUT: 10000,
  
  // Default headers
  DEFAULT_HEADERS: {
    'Content-Type': 'application/json',
  },
} as const;

// Helper function to get full API URL
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// Helper function to get auth headers
export const getAuthHeaders = (token?: string): Record<string, string> => {
  const headers = { ...API_CONFIG.DEFAULT_HEADERS };
  
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  
  return headers;
};
