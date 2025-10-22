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

interface WatchlistStatsProps {
  stocks: StockData[];
  totalCount: number;
}

export default function WatchlistStats({ stocks, totalCount }: WatchlistStatsProps) {
  const gainingCount = stocks.filter(stock => stock.change > 0).length;
  const losingCount = stocks.filter(stock => stock.change < 0).length;
  const totalValue = stocks.reduce((sum, stock) => sum + stock.price, 0);
  const totalChange = stocks.reduce((sum, stock) => sum + stock.change, 0);
  const totalChangePercent = totalCount > 0 ? (totalChange / totalCount) : 0;

  const stats = [
    {
      name: 'Total Stocks',
      value: totalCount,
      icon: 'W',
      color: 'bg-blue-500',
      description: 'Stocks in watchlist'
    },
    {
      name: 'Gaining Today',
      value: gainingCount,
      icon: '↑',
      color: 'bg-green-500',
      description: 'Stocks up today'
    },
    {
      name: 'Losing Today',
      value: losingCount,
      color: 'bg-red-500',
      icon: '↓',
      description: 'Stocks down today'
    },
    {
      name: 'Avg Change',
      value: `${totalChangePercent >= 0 ? '+' : ''}${totalChangePercent.toFixed(2)}%`,
      icon: 'Δ',
      color: totalChangePercent >= 0 ? 'bg-green-500' : 'bg-red-500',
      description: 'Average change'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div key={stat.name} className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className={`w-10 h-10 ${stat.color} rounded-lg flex items-center justify-center`}>
                  <span className="text-white font-bold text-lg">{stat.icon}</span>
                </div>
              </div>
              <div className="ml-4 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {stat.name}
                  </dt>
                  <dd className="text-2xl font-bold text-gray-900">
                    {stat.value}
                  </dd>
                  <dd className="text-xs text-gray-500">
                    {stat.description}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

