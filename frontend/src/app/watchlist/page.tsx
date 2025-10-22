'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import LoadingComponent from '@/components/loading';
import { useAuth } from '@/hooks/useAuth';
import StockSearch from '@/components/StockSearch';
import StockCard from '@/components/StockCard';
import WatchlistStats from '@/components/WatchlistStats';

interface CompanyData {
  symbol: string;
  name: string;
}

interface StockData {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap: string;
  sector: string;
}

export default function WatchlistPage() {
  const [watchlist, setWatchlist] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const router = useRouter();
  const { user } = useAuth();
  const [companies, setCompanies] = useState<CompanyData[]>([]);
  const [isClient, setIsClient] = useState(false);

  // Set client-side flag
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Redirect if not authenticated
  useEffect(() => {
    if (isClient && !user?.id) {
      router.push('/auth');
    }
  }, [isClient, user?.id, router]);

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await apiClient.getCompanies();
        console.log('response', response);
        if (response.data) {
          const companies = response.data as CompanyData[];
          setCompanies(companies);
        }
        if (response.error) {
          setError(response.error);
          return;
        }
      } catch (_err) {
        setError('Failed to fetch companies');
      }
    }
    const fetchWatchlist = async () => {
      try {
        const response = await apiClient.getWatchlist(user?.id || '');
        if (response.error) {
          setError(response.error);
          setIsLoading(false);
          return;
        }
        if (response.data) {
          const symbols = response.data as string[];
          setWatchlist(symbols);
        }
        setIsLoading(false);
      } catch (_err) {
        setError('Failed to fetch watchlist');
        setIsLoading(false);
      }
    };
    fetchCompanies();
    fetchWatchlist();
  }, [user?.id]);

  // Don't render anything until client-side hydration is complete
  if (!isClient) {
    return <LoadingComponent />;
  }

  // Redirect if not authenticated (client-side only)
  if (!user?.id) {
    return <LoadingComponent />;
  }

  const handleAddStock = async (symbol: string) => {
    setIsAdding(true);
    setError(null);
    
    try {
      // Check if stock exists in our mock data
      if (!companies.find(c => c.symbol === symbol)) {
        setError(`Stock symbol "${symbol}" not found`);
        setIsAdding(false);
        return;
      }

      // Check if already in watchlist
      if (watchlist.includes(symbol)) {
        setError(`Stock "${symbol}" is already in your watchlist`);
        setIsAdding(false);
        return;
      }

      // Add to watchlist via API
      const response = await apiClient.addToWatchlist(user?.id || '', symbol);
      if (response.error) {
        setError(response.error);
      } else {
        setWatchlist(prev => [...prev, symbol]);
        setError(null);
      }
    } catch (_err) {
      setError('Failed to add stock to watchlist');
    } finally {
      setIsAdding(false);
    }
  };

  const handleRemoveStock = async (symbol: string) => {
    try {
      const response = await apiClient.removeFromWatchlist(user.id, symbol);
      if (response.error) {
        setError(response.error);
      } else {
        setWatchlist(prev => prev.filter(s => s !== symbol));
        setError(null);
      }
    } catch (_err) {
      setError('Failed to remove stock from watchlist');
    }
  };


  if (isLoading) {
    return <LoadingComponent />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">My Watchlist</h1>
              <p className="text-gray-600">Track your favorite stocks</p>
            </div>
            <button
              onClick={() => router.push('/dashboard')}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          
          {/* Add Stock Section */}
          <StockSearch 
            onAddStock={handleAddStock}
            isLoading={isAdding}
            error={error}
            companies={companies}
          />

          {/* Watchlist Stats */}
          <div className="mb-6 pt-6">
            <WatchlistStats 
              stocks={watchlist.map(symbol => {
                const company = companies.find(c => c.symbol === symbol);
                if (!company) return null;
                return {
                  symbol: company.symbol,
                  name: company.name,
                  price: 0,
                  change: 0,
                  changePercent: 0,
                  volume: 0,
                  marketCap: '',
                  sector: ''
                } as StockData;
              }).filter(Boolean) as StockData[]} 
              totalCount={watchlist.length} 
            />
          </div>

          {/* Stock List */}
          {watchlist.length === 0 ? (
            <div className="bg-white shadow rounded-lg p-12 text-center">
              <div className="mx-auto h-12 w-12 text-gray-400">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No stocks in watchlist</h3>
              <p className="mt-1 text-sm text-gray-500">Get started by adding some stocks to track.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {watchlist.map((symbol) => {
                const company = companies.find(c => c.symbol === symbol);
                if (!company) {
                  return null;
                }
                // Create a mock StockData object for display
                const stockData: StockData = {
                  symbol: company.symbol,
                  name: company.name,
                  price: 0, // Mock data - you might want to fetch real prices
                  change: 0,
                  changePercent: 0,
                  volume: 0,
                  marketCap: '',
                  sector: ''
                };
                return (
                <StockCard
                  key={company.symbol}
                  stock={stockData}
                  onRemove={handleRemoveStock}
                  showRemoveButton={true}
                />
                );
              })}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}