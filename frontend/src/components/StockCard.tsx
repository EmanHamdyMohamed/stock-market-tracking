'use client';

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

interface StockCardProps {
  stock: StockData;
  onRemove?: (symbol: string) => void;
  showRemoveButton?: boolean;
}

export default function StockCard({ stock, onRemove, showRemoveButton = true }: StockCardProps) {
  const formatPrice = (price: number) => `$${price.toFixed(2)}`;
  const formatChange = (change: number) => `${change >= 0 ? '+' : ''}${change.toFixed(2)}`;
  const formatChangePercent = (percent: number) => `${percent >= 0 ? '+' : ''}${percent.toFixed(2)}%`;
  const formatVolume = (volume: number) => (volume / 1000000).toFixed(1) + 'M';

  const getSectorColor = (sector: string) => {
    const colors: { [key: string]: string } = {
      'Technology': 'bg-blue-100 text-blue-800',
      'Automotive': 'bg-green-100 text-green-800',
      'Consumer Discretionary': 'bg-purple-100 text-purple-800',
      'Healthcare': 'bg-pink-100 text-pink-800',
      'Financial': 'bg-yellow-100 text-yellow-800',
      'Energy': 'bg-orange-100 text-orange-800',
    };
    return colors[sector] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {/* Stock Avatar */}
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-lg">
              {stock.symbol.charAt(0)}
            </span>
          </div>
          
          {/* Stock Info */}
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-lg font-semibold text-gray-900">{stock.symbol}</h3>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getSectorColor(stock.sector)}`}>
                {stock.sector}
              </span>
            </div>
            <p className="text-sm text-gray-600">{stock.name}</p>
          </div>
        </div>

        {/* Price and Change */}
        <div className="text-right">
          <p className="text-xl font-bold text-gray-900">{formatPrice(stock.price)}</p>
          <div className="flex items-center justify-end space-x-1">
            <span className={`text-sm font-medium ${
              stock.change >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {formatChange(stock.change)}
            </span>
            <span className={`text-sm ${
              stock.change >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              ({formatChangePercent(stock.changePercent)})
            </span>
          </div>
        </div>
      </div>

      {/* Additional Info */}
      <div className="mt-4 grid grid-cols-2 gap-4 pt-4 border-t border-gray-100">
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide">Volume</p>
          <p className="text-sm font-medium text-gray-900">{formatVolume(stock.volume)}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide">Market Cap</p>
          <p className="text-sm font-medium text-gray-900">{stock.marketCap}</p>
        </div>
      </div>

      {/* Remove Button */}
      {showRemoveButton && onRemove && (
        <div className="mt-4 flex justify-end">
          <button
            onClick={() => onRemove(stock.symbol)}
            className="text-red-600 hover:text-red-800 text-sm font-medium hover:bg-red-50 px-3 py-1 rounded-md transition-colors"
          >
            Remove from Watchlist
          </button>
        </div>
      )}
    </div>
  );
}

