import React, { useState, useEffect } from 'react';
import { Lightbulb, Sparkles, RefreshCw, BookOpen, Github, Tag, Clock, Save, Play, Users, AlertCircle, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import PreferenceForm from './PreferenceForm';
import ProjectCard from './ProjectCard';
import CommunityShowcase from './CommunityShowcase';
import { generateProjectRecommendations, generateFallbackRecommendations } from '../../utils/groqAPI';
import { useGlobalState } from '../../contexts/GlobalContext';
import {
  getSavedProjects,
  saveProject,
  updateProjectStatus,
  isProjectSaved,
  type SavedProject
} from '../../utils/projectStorage';

export interface ProjectRecommendation {
  id: string;
  title: string;
  description: string;
  features: string[];
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  techStack: string[];
  tags: string[];
  estimatedTime: string;
  starterTutorials?: string[];
  githubBoilerplates?: string[];
  status?: 'saved' | 'in_progress' | 'completed';
}

export interface UserPreferences {
  techStack: string[];
  careerFocus: string;
  skillLevel: string;
  interestArea: string[];
}

const ProjectRecommender: React.FC = () => {
  const { state } = useGlobalState();
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const [recommendations, setRecommendations] = useState<ProjectRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [errorStatus, setErrorStatus] = useState<number | null>(null);
  const [isFallbackMode, setIsFallbackMode] = useState<boolean>(false);
  const [savedProjects, setSavedProjects] = useState<SavedProject[]>([]);
  const [activeTab, setActiveTab] = useState<'form' | 'recommendations' | 'saved' | 'community'>('form');

  // Load saved projects on component mount
  useEffect(() => {
    setSavedProjects(getSavedProjects());
  }, []);

  const handlePreferencesSubmit = async (prefs: UserPreferences) => {
    setPreferences(prefs);
    setIsLoading(true);
    setErrorMessage(null);
    setErrorStatus(null);
    setIsFallbackMode(false);
    setActiveTab('recommendations');

    const savedTitles = savedProjects.map((p) => p.title);

    try {
      const projects = await generateProjectRecommendations(prefs, savedTitles);
      setRecommendations(projects);
      setIsFallbackMode(false);
    } catch (error: any) {
      console.error('Error generating recommendations:', error);
      const msg = error?.message || 'Failed to generate AI recommendations.';
      setErrorMessage(msg);
      setErrorStatus(error?.status || null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerateRecommendations = async () => {
    if (!preferences) return;
    setIsLoading(true);
    setErrorMessage(null);
    setErrorStatus(null);

    // Collect titles of currently displayed recommendations and saved projects to avoid duplicates
    const currentTitles = recommendations.map((p) => p.title);
    const savedTitles = savedProjects.map((p) => p.title);
    const excludeTitles = Array.from(new Set([...currentTitles, ...savedTitles]));

    try {
      const projects = await generateProjectRecommendations(preferences, excludeTitles);
      setRecommendations(projects);
      setIsFallbackMode(false);
    } catch (error: any) {
      console.error('Error regenerating recommendations:', error);
      const msg = error?.message || 'Failed to regenerate AI recommendations.';
      setErrorMessage(msg);
      setErrorStatus(error?.status || null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadCuratedFallback = () => {
    if (!preferences) return;
    const fallbackProjects = generateFallbackRecommendations(preferences);
    setRecommendations(fallbackProjects);
    setIsFallbackMode(true);
    setErrorMessage(null);
    setErrorStatus(null);
  };


  const handleSaveProject = (project: ProjectRecommendation) => {
    try {
      const savedProject = saveProject(project);
      setSavedProjects(prev => [...prev, savedProject]);
    } catch (error) {
      console.error('Failed to save project:', error);
      // Could add toast notification here
    }
  };

  const handleProjectStatusChange = (projectId: string, status: ProjectRecommendation['status']) => {
    try {
      const updatedProject = updateProjectStatus(projectId, status);
      if (updatedProject) {
        setSavedProjects(prev =>
          prev.map(project =>
            project.id === projectId ? updatedProject : project
          )
        );
      }
    } catch (error) {
      console.error('Failed to update project status:', error);
      // Could add toast notification here
    }
  };

  const getExampleRecommendations = (prefs: UserPreferences): ProjectRecommendation[] => {
    // Fallback recommendations based on preferences
    const examples: ProjectRecommendation[] = [
      {
        id: '1',
        title: 'Smart Appointment Booking System',
        description: 'A comprehensive booking platform with role-based dashboards, calendar integration, and automated email notifications.',
        features: ['Role-based dashboard', 'Calendar view', 'Email alerts', 'Payment integration', 'SMS notifications'],
        difficulty: 'Intermediate',
        techStack: ['React', 'Node.js', 'MongoDB', 'Express.js'],
        tags: ['#fullstack', '#productivity', '#mern', '#calendar'],
        estimatedTime: '3-4 weeks',
        starterTutorials: ['Building a MERN Stack Application', 'Calendar Integration Guide'],
        githubBoilerplates: ['https://github.com/example/booking-system']
      },
      {
        id: '2',
        title: 'Personal Finance Tracker',
        description: 'Track expenses, income, and financial goals with beautiful charts and insights.',
        features: ['Expense tracking', 'Budget planning', 'Financial goals', 'Data visualization', 'Export reports'],
        difficulty: prefs.skillLevel === 'Beginner' ? 'Beginner' : 'Intermediate',
        techStack: prefs.techStack.includes('React') ? ['React', 'JavaScript'] : ['HTML', 'CSS', 'JavaScript'],
        tags: ['#finance', '#productivity', '#charts', '#budgeting'],
        estimatedTime: '2-3 weeks',
        starterTutorials: ['Chart.js Basics', 'Local Storage in JavaScript'],
        githubBoilerplates: ['https://github.com/example/finance-tracker']
      },
      {
        id: '3',
        title: 'AI-Powered Study Assistant',
        description: 'An intelligent study companion that creates quizzes, tracks progress, and provides personalized learning paths.',
        features: ['AI quiz generation', 'Progress tracking', 'Study reminders', 'Performance analytics', 'Study groups'],
        difficulty: 'Advanced',
        techStack: ['React', 'Node.js', 'Python', 'MongoDB'],
        tags: ['#ai', '#education', '#machine-learning', '#study'],
        estimatedTime: '4-6 weeks',
        starterTutorials: ['Introduction to AI APIs', 'Building Educational Apps'],
        githubBoilerplates: ['https://github.com/example/ai-study-assistant']
      }
    ];

    return examples.filter(project => {
      // Filter by skill level
      if (prefs.skillLevel === 'Beginner' && project.difficulty === 'Advanced') return false;
      if (prefs.skillLevel === 'Advanced' && project.difficulty === 'Beginner') return false;

      // Filter by interest areas (check if any interest area matches project themes)
      const hasMatchingInterest = prefs.interestArea.some(interest => {
        const projectText = (project.title + ' ' + project.description + ' ' + project.tags.join(' ')).toLowerCase();
        return projectText.includes(interest.toLowerCase());
      });

      return hasMatchingInterest || prefs.interestArea.length === 0;
    });
  };

  return (
    <div className={`min-h-screen transition-colors duration-200 ${
      state.darkMode ? 'bg-gray-900' : 'bg-gradient-to-br from-blue-50 via-white to-purple-50'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 rounded-2xl flex items-center justify-center shadow-xl">
                <Lightbulb className="w-8 h-8 text-white" />
              </div>
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-yellow-400 rounded-full animate-pulse"></div>
              <div className="absolute -bottom-2 -left-2 w-4 h-4 bg-green-400 rounded-full animate-bounce"></div>
            </div>
          </div>
          <h1 className={`text-5xl font-bold mb-6 ${
            state.darkMode
              ? 'text-white'
              : 'bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent'
          }`}>
            AI Project Recommender
          </h1>
          <p className={`text-xl max-w-4xl mx-auto leading-relaxed ${
            state.darkMode ? 'text-gray-300' : 'text-gray-700'
          }`}>
            Get personalized project recommendations powered by AI to accelerate your skill growth and build an impressive portfolio
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-10">
          <div className={`flex rounded-2xl p-1.5 border shadow-lg ${
            state.darkMode
              ? 'bg-gray-800 border-gray-700'
              : 'bg-white/80 backdrop-blur-sm border-gray-200/50'
          }`}>
            {[
              { id: 'form', label: 'Preferences', icon: Sparkles },
              { id: 'recommendations', label: 'Recommendations', icon: Lightbulb },
              { id: 'saved', label: 'Saved Projects', icon: BookOpen },
              { id: 'community', label: 'Community', icon: Users }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-6 py-3 rounded-xl text-sm font-semibold transition-all duration-300 ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg transform scale-105'
                      : state.darkMode
                      ? 'text-gray-300 hover:text-white hover:bg-gray-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-blue-50 hover:shadow-md'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'form' && (
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <PreferenceForm initialPreferences={preferences} onSubmit={handlePreferencesSubmit} />
            </motion.div>
          )}

          {activeTab === 'recommendations' && (
            <motion.div
              key="recommendations"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="space-y-6">
                {/* Fallback Mode Honest Banner */}
                {isFallbackMode && (
                  <div className="p-4 rounded-2xl border border-amber-300 bg-amber-50 dark:bg-amber-900/20 dark:border-amber-700 flex items-start space-x-3 text-amber-900 dark:text-amber-200">
                    <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5 text-amber-600 dark:text-amber-400" />
                    <div className="text-sm">
                      <p className="font-semibold">Curated Starter Templates (Offline Mode)</p>
                      <p className="mt-0.5 opacity-90">
                        The projects displayed below are curated offline starter templates matching your preferences, not freshly generated by AI.
                      </p>
                    </div>
                  </div>
                )}

                {/* Error Banner */}
                {errorMessage && (
                  <div className={`p-5 rounded-2xl border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 ${
                    errorStatus === 429
                      ? 'border-yellow-400 bg-yellow-50 dark:bg-yellow-900/20 dark:border-yellow-700 text-yellow-900 dark:text-yellow-200'
                      : 'border-red-300 bg-red-50 dark:bg-red-900/20 dark:border-red-700 text-red-900 dark:text-red-200'
                  }`}>
                    <div className="flex items-start space-x-3">
                      <AlertCircle className={`w-6 h-6 flex-shrink-0 mt-0.5 ${
                        errorStatus === 429 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'
                      }`} />
                      <div>
                        <p className="font-bold text-base">
                          {errorStatus === 429
                            ? 'Gemini AI Rate Limit / Quota Reached'
                            : 'AI Recommendation Service Unavailable'}
                        </p>
                        <p className="text-sm mt-1 opacity-90">
                          {errorMessage}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 self-end sm:self-auto">
                      <button
                        onClick={preferences ? handleRegenerateRecommendations : undefined}
                        disabled={isLoading || !preferences}
                        className="px-4 py-2 rounded-xl text-xs font-semibold bg-white dark:bg-gray-800 border shadow-sm hover:shadow transition-all disabled:opacity-50"
                      >
                        Retry AI
                      </button>
                      <button
                        onClick={handleLoadCuratedFallback}
                        disabled={!preferences}
                        className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 text-white hover:bg-blue-700 transition-all disabled:opacity-50"
                      >
                        Load Curated Templates
                      </button>
                    </div>
                  </div>
                )}

                {/* Regenerate Button */}
                {recommendations.length > 0 && !isLoading && (
                  <div className="flex justify-center">
                    <button
                      onClick={handleRegenerateRecommendations}
                      disabled={isLoading}
                      className="flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 text-white rounded-2xl hover:from-purple-600 hover:via-pink-600 hover:to-orange-600 transition-all duration-300 disabled:opacity-50 shadow-lg hover:shadow-xl font-semibold"
                    >
                      <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                      <span>Generate New Recommendations</span>
                    </button>
                  </div>
                )}

                {/* Loading State */}
                {isLoading && (
                  <div className="flex flex-col items-center justify-center py-12">
                    <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-500 rounded-full animate-spin mb-4"></div>
                    <p className={`text-lg font-medium ${state.darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                      AI is generating personalized recommendations based on your preferences...
                    </p>
                    <p className={`text-sm mt-1 ${state.darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                      Connecting to Gemini API via backend
                    </p>
                  </div>
                )}

                {/* Recommendations Grid */}
                {!isLoading && recommendations.length > 0 && (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {recommendations.map((project, index) => (
                      <motion.div
                        key={project.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                      >
                        <ProjectCard
                          project={project}
                          onSave={() => handleSaveProject(project)}
                          isSaved={isProjectSaved(project.id)}
                        />
                      </motion.div>
                    ))}
                  </div>
                )}

                {/* Empty State */}
                {!isLoading && recommendations.length === 0 && !errorMessage && (
                  <div className={`text-center py-16 rounded-2xl border-2 border-dashed ${
                    state.darkMode ? 'border-gray-600 bg-gray-800/50' : 'border-gray-300 bg-white/50'
                  }`}>
                    <div className="relative">
                      <Lightbulb className={`w-20 h-20 mx-auto mb-6 ${
                        state.darkMode ? 'text-gray-600' : 'text-blue-400'
                      }`} />
                      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-8 h-8 bg-yellow-300 rounded-full animate-ping opacity-30"></div>
                    </div>
                    <h3 className={`text-2xl font-bold mb-3 ${
                      state.darkMode
                        ? 'text-gray-300'
                        : 'bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent'
                    }`}>
                      Ready to discover amazing projects?
                    </h3>
                    <p className={`text-lg ${
                      state.darkMode ? 'text-gray-400' : 'text-gray-600'
                    }`}>
                      Fill out your preferences to get personalized AI recommendations
                    </p>
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {activeTab === 'saved' && (
            <motion.div
              key="saved"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {savedProjects.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {savedProjects.map((project, index) => (
                    <motion.div
                      key={project.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.1 }}
                    >
                      <ProjectCard
                        project={project}
                        onSave={() => {}}
                        isSaved={true}
                        onStatusChange={(status) => handleProjectStatusChange(project.id, status)}
                        showStatusControls={true}
                      />
                    </motion.div>
                  ))}
                </div>
              ) : (
                <div className={`text-center py-16 rounded-2xl border-2 border-dashed ${
                  state.darkMode ? 'border-gray-600 bg-gray-800/50' : 'border-gray-300 bg-white/50'
                }`}>
                  <div className="relative">
                    <BookOpen className={`w-20 h-20 mx-auto mb-6 ${
                      state.darkMode ? 'text-gray-600' : 'text-indigo-400'
                    }`} />
                    <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-8 h-8 bg-indigo-300 rounded-full animate-pulse opacity-40"></div>
                  </div>
                  <h3 className={`text-2xl font-bold mb-3 ${
                    state.darkMode
                      ? 'text-gray-300'
                      : 'bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent'
                  }`}>
                    No saved projects yet
                  </h3>
                  <p className={`text-lg ${
                    state.darkMode ? 'text-gray-400' : 'text-gray-600'
                  }`}>
                    Save projects from your recommendations to track your progress
                  </p>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'community' && (
            <motion.div
              key="community"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <CommunityShowcase />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default ProjectRecommender;
