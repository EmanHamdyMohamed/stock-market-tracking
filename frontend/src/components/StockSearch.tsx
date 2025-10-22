'use client';

import { useState } from 'react';

interface StockData {
  symbol: string;
  name: string;
}

interface StockSearchProps {
  onAddStock: (symbol: string) => void;
  isLoading?: boolean;
  error?: string | null;
  companies?: StockData[];
}

export default function StockSearch({ onAddStock, isLoading = false, error, companies }: StockSearchProps) {
  const [searchSymbol, setSearchSymbol] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchSymbol.trim()) {
      onAddStock(searchSymbol.trim().toUpperCase());
      setSearchSymbol('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Add Stock to Watchlist</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex gap-4">
          <input
            type="text"
            value={searchSymbol}
            onChange={(e) => setSearchSymbol(e.target.value)}
            placeholder="Enter stock symbol (e.g., AAPL, GOOGL, MSFT)"
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg text-gray-600"
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !searchSymbol.trim()}
            className="bg-green-600 text-white px-8 py-3 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {isLoading ? 'Adding...' : 'Add Stock'}
          </button>
        </div>
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}
      </form>

      {/* Popular Stocks */}
      <div className="mt-6">
        <p className="text-sm text-gray-600 mb-3">Popular stocks:</p>
        <div className="flex flex-wrap gap-2">
          {companies?.map((c: StockData) => (
            <button
              key={c.symbol}
              onClick={() => setSearchSymbol(c.symbol)}
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              {c.symbol}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

