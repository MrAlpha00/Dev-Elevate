import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import { Toaster } from 'sonner';

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900">
      <Header />
      <main className="flex-1">
        <Outlet />
      </main>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#1F2937',
            color: '#F3F4F6',
            border: '1px solid #374151'
          }
        }}
      />
    </div>
  );
};

export default Layout;