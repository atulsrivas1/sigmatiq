import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-surface-1 text-text-1 p-4 flex justify-between items-center">
      <div className="flex items-center">
        <img src="/assets/LEKOCH_Logo_Pack/lekoch_logo_small.png" alt="Logo" className="h-8 w-8 mr-2" />
        <span className="text-xl font-bold">Sigmatiq</span>
      </div>
      <nav>
        <a href="/" className="px-4">Dashboard</a>
        <a href="/models" className="px-4">Models</a>
        <a href="/runs" className="px-4">Runs</a>
        <a href="/sweeps" className="px-4">Sweeps</a>
        <a href="/leaderboard" className="px-4">Leaderboard</a>
      </nav>
    </header>
  );
};

export default Header;