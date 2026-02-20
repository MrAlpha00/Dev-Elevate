import React from 'react';
import { Code2 } from 'lucide-react';
import { motion } from 'framer-motion';

const LoadingScreen: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <div className="text-center">
        <motion.div
          animate={{ 
            rotate: 360,
            scale: [1, 1.2, 1]
          }}
          transition={{ 
            rotate: { duration: 2, repeat: Infinity, ease: "linear" },
            scale: { duration: 1, repeat: Infinity, ease: "easeInOut" }
          }}
          className="w-20 h-20 bg-gradient-to-r from-electric-400 to-neon-500 rounded-2xl flex items-center justify-center mx-auto mb-6"
        >
          <Code2 className="w-10 h-10 text-white" />
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="space-y-2"
        >
          <h2 className="text-2xl font-bold text-white">DevElevate</h2>
          <div className="flex items-center justify-center space-x-1">
            {[0, 1, 2].map((index) => (
              <motion.div
                key={index}
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [0.5, 1, 0.5]
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: index * 0.2
                }}
                className="w-2 h-2 bg-electric-400 rounded-full"
              />
            ))}
          </div>
          <p className="text-gray-400">Loading your coding environment...</p>
        </motion.div>
      </div>
    </div>
  );
};

export default LoadingScreen;