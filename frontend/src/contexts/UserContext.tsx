'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient, User } from '@/lib/api';

interface UserContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (token: string) => void;
  logout: () => void;
  refreshUser: () => Promise<void>;
  isAuthenticated: boolean;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

interface UserProviderProps {
  children: ReactNode;
}

export function UserProvider({ children }: UserProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const isAuthenticated = !!user;

  const login = (token: string) => {
    localStorage.setItem('access_token', token);
    refreshUser();
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    setError(null);
    router.push('/auth');
  };

  const refreshUser = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await apiClient.getCurrentUser();
      if (result.error) {
        setError(result.error);
        // If token is invalid, logout user
        if (result.error.includes('401') || result.error.includes('Invalid')) {
          logout();
        }
      } else if (result.data) {
        setUser(result.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load user data');
      logout();
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      refreshUser();
    } else {
      setIsLoading(false);
    }
  }, []);

  const value: UserContextType = {
    user,
    isLoading,
    error,
    login,
    logout,
    refreshUser,
    isAuthenticated,
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}
