import React from 'react';
import { CheckCircle, XCircle, Clock, AlertCircle, Play } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface TestCase {
  id: string;
  input: string;
  expectedOutput: string;
  actualOutput?: string;
  passed: boolean;
  runtime?: number;
  memory?: number;
  error?: string;
}

interface TestResultsProps {
  results: TestCase[];
  isVisible: boolean;
  onClose: () => void;
  onRunAgain: () => void;
  totalPassed: number;
  totalTests: number;
}

const TestResults: React.FC<TestResultsProps> = ({
  results,
  isVisible,
  onClose,
  onRunAgain,
  totalPassed,
  totalTests
}) => {
  const getStatusIcon = (passed: boolean, error?: string) => {
    if (error) return <AlertCircle className="w-5 h-5 text-orange-400" />;
    return passed ? 
      <CheckCircle className="w-5 h-5 text-green-400" /> : 
      <XCircle className="w-5 h-5 text-red-400" />;
  };

  const getStatusColor = (passed: boolean, error?: string) => {
    if (error) return 'border-orange-500 bg-orange-900/20';
    return passed ? 'border-green-500 bg-green-900/20' : 'border-red-500 bg-red-900/20';
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="border-t border-gray-700"
        >
          <div className="bg-gray-800 p-4">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-4">
                <h3 className="text-lg font-semibold text-white">Test Results</h3>
                <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                  totalPassed === totalTests ? 
                    'bg-green-400/20 text-green-400' : 
                    'bg-red-400/20 text-red-400'
                }`}>
                  {totalPassed}/{totalTests} Passed
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={onRunAgain}
                  className="flex items-center space-x-1 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                >
                  <Play className="w-4 h-4" />
                  <span>Run Again</span>
                </motion.button>
                <button
                  onClick={onClose}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="space-y-3 max-h-96 overflow-y-auto">
              {results.map((result, index) => (
                <motion.div
                  key={result.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`p-4 rounded-lg border-2 ${getStatusColor(result.passed, result.error)}`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(result.passed, result.error)}
                      <span className="font-medium text-white">
                        Test Case {index + 1}
                      </span>
                    </div>
                    
                    {(result.runtime || result.memory) && (
                      <div className="flex items-center space-x-4 text-sm text-gray-400">
                        {result.runtime && (
                          <div className="flex items-center space-x-1">
                            <Clock className="w-3 h-3" />
                            <span>{result.runtime}ms</span>
                          </div>
                        )}
                        {result.memory && (
                          <span>{result.memory}MB</span>
                        )}
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-gray-400">Input:</span>
                      <pre className="mt-1 p-2 bg-gray-900 rounded text-yellow-400 overflow-x-auto">
                        {result.input}
                      </pre>
                    </div>
                    
                    <div>
                      <span className="text-gray-400">Expected:</span>
                      <pre className="mt-1 p-2 bg-gray-900 rounded text-blue-400 overflow-x-auto">
                        {result.expectedOutput}
                      </pre>
                    </div>
                    
                    {result.actualOutput && (
                      <div>
                        <span className="text-gray-400">Your Output:</span>
                        <pre className={`mt-1 p-2 bg-gray-900 rounded overflow-x-auto ${
                          result.passed ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {result.actualOutput}
                        </pre>
                      </div>
                    )}
                    
                    {result.error && (
                      <div>
                        <span className="text-gray-400">Error:</span>
                        <pre className="mt-1 p-2 bg-gray-900 rounded text-orange-400 overflow-x-auto">
                          {result.error}
                        </pre>
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default TestResults;