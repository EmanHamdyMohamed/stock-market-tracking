import { useUser } from '@/contexts/UserContext';

/**
 * Custom hook for authentication-related functionality
 * Provides a simplified interface for common auth operations
 */
export function useAuth() {
  const { user, isLoading, error, login, logout, refreshUser, isAuthenticated } = useUser();

  return {
    // User data
    user,
    isAuthenticated,
    isLoading,
    error,
    
    // Auth actions
    login,
    logout,
    refreshUser,
    
    // Computed values
    isAdmin: user?.is_admin || false,
    isVerified: user?.is_verified || false,
    watchlistCount: user?.watchlist?.length || 0,
    preferredSectors: user?.preferred_sectors || [],
    
    // Helper functions
    hasWatchlist: (user?.watchlist?.length || 0) > 0,
    getUserDisplayName: () => user?.name || user?.email || 'User',
  };
}
