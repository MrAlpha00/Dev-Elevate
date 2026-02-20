import React from 'react';
import { motion } from 'framer-motion';

interface NeonCardProps {
  children: React.ReactNode;
  className?: string;
  glowColor?: 'electric' | 'neon' | 'cyber';
  hover?: boolean;
}

const NeonCard: React.FC<NeonCardProps> = ({
  children,
  className = '',
  glowColor = 'electric',
  hover = true
}) => {
  const glowColors = {
    electric: 'hover:shadow-electric-400/30 border-electric-400/30',
    neon: 'hover:shadow-neon-500/30 border-neon-500/30',
    cyber: 'hover:shadow-cyber-400/30 border-cyber-400/30'
  };

  return (
    <motion.div
      whileHover={hover ? { 
        y: -5,
        boxShadow: glowColor === 'electric' ? '0 20px 40px -10px rgba(0, 212, 255, 0.3)' :
                   glowColor === 'neon' ? '0 20px 40px -10px rgba(188, 111, 241, 0.3)' :
                   '0 20px 40px -10px rgba(16, 185, 129, 0.3)'
      } : {}}
      className={`
        bg-gray-800/50 backdrop-blur-sm border border-gray-700
        rounded-xl p-6 transition-all duration-300
        ${hover ? `hover:border-opacity-60 ${glowColors[glowColor]}` : ''}
        ${className}
      `}
    >
      {children}
    </motion.div>
  );
};

export default NeonCard;