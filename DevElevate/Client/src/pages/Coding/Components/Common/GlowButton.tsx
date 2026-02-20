import React from 'react';
import { motion } from 'framer-motion';
import { DivideIcon as LucideIcon } from 'lucide-react';

interface GlowButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  icon?: LucideIcon;
  disabled?: boolean;
  className?: string;
}

const GlowButton: React.FC<GlowButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  disabled = false,
  className = ''
}) => {
  const variants = {
    primary: 'bg-gradient-to-r from-electric-400 to-neon-500 hover:from-electric-500 hover:to-neon-600 shadow-electric-400/50',
    secondary: 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 shadow-purple-500/50',
    success: 'bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 shadow-green-500/50',
    danger: 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 shadow-red-500/50'
  };

  const sizes = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };

  return (
    <motion.button
      whileHover={{ scale: disabled ? 1 : 1.05, boxShadow: disabled ? 'none' : '0 10px 25px -5px rgba(0, 212, 255, 0.4)' }}
      whileTap={{ scale: disabled ? 1 : 0.95 }}
      onClick={onClick}
      disabled={disabled}
      className={`
        ${variants[variant]} 
        ${sizes[size]} 
        ${className}
        relative overflow-hidden rounded-lg font-semibold text-white 
        transition-all duration-300 transform hover:shadow-lg 
        disabled:opacity-50 disabled:cursor-not-allowed 
        disabled:hover:scale-100 disabled:hover:shadow-none
        flex items-center justify-center space-x-2
      `}
    >
      <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300" />
      <div className="relative z-10 flex items-center space-x-2">
        {Icon && <Icon className="w-4 h-4" />}
        <span>{children}</span>
      </div>
    </motion.button>
  );
};

export default GlowButton;