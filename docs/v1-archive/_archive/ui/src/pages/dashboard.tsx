import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4 text-text-1">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-surface-2 p-4 rounded-lg">
          <h2 className="text-lg font-bold text-text-1 mb-2">Recent Models</h2>
          <ul>
            <li className="text-text-2">spy_opt_0dte_hourly</li>
            <li className="text-text-2">spy_eq_swing_daily</li>
          </ul>
        </div>
        <div className="bg-surface-2 p-4 rounded-lg">
          <h2 className="text-lg font-bold text-text-1 mb-2">Last Runs</h2>
          <ul>
            <li className="text-text-2">2025-08-16 11:50 - spy_opt_0dte_hourly - Backtest</li>
            <li className="text-text-2">2025-08-15 16:10 - spy_eq_swing_daily - Train</li>
          </ul>
        </div>
        <div className="bg-surface-2 p-4 rounded-lg">
          <h2 className="text-lg font-bold text-text-1 mb-2">Quick Actions</h2>
          <div className="flex flex-col">
            <button className="bg-accent text-white px-4 py-2 rounded-lg mb-2">Create Model</button>
            <button className="bg-accent text-white px-4 py-2 rounded-lg">Run Backtest</button>
          </div>
        </div>
        <div className="bg-surface-2 p-4 rounded-lg">
          <h2 className="text-lg font-bold text-text-1 mb-2">Health</h2>
          <p className="text-text-2">API: ok</p>
          <p className="text-text-2">DB: warn</p>
          <p className="text-text-2">Data: ok</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;