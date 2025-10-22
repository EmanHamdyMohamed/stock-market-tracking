'use client';

import { useAuth } from '@/hooks/useAuth';

interface UserProfileProps {
  showDetails?: boolean;
  className?: string;
}

export default function UserProfile({ showDetails = false, className = '' }: UserProfileProps) {
  const { user, getUserDisplayName, isVerified, watchlistCount } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      {/* Avatar */}
      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
        <span className="text-white font-semibold text-sm">
          {getUserDisplayName().charAt(0).toUpperCase()}
        </span>
      </div>
      
      {/* User Info */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">
          {getUserDisplayName()}
        </p>
        {showDetails && (
          <>
            <p className="text-xs text-gray-500 truncate">{user.email}</p>
            <div className="flex items-center space-x-2 mt-1">
              <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                isVerified 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {isVerified ? 'Verified' : 'Unverified'}
              </span>
              <span className="text-xs text-gray-500">
                {watchlistCount} stocks
              </span>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
