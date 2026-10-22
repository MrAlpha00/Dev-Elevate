import axiosInstance from '../api/axiosinstance';
import type { ProjectRecommendation, UserPreferences } from '../components/ProjectRecommender/ProjectRecommender';

export const generateProjectRecommendations = async (
  preferences: UserPreferences,
  excludeTitles: string[] = []
): Promise<ProjectRecommendation[]> => {
  try {
    const response = await axiosInstance.post<{
      success: boolean;
      projects: ProjectRecommendation[];
      message?: string;
    }>('/api/v1/ai/generate-projects', {
      preferences,
      excludeTitles,
    });

    if (response.data && response.data.success && Array.isArray(response.data.projects)) {
      return response.data.projects;
    }

    throw new Error(response.data?.message || 'Invalid response from AI project service');
  } catch (error: any) {
    const backendMessage =
      error?.response?.data?.message ||
      error?.message ||
      'Failed to generate AI project recommendations';
    const status = error?.response?.status;
    const customError = new Error(backendMessage);
    (customError as any).status = status;
    throw customError;
  }
};


// Fallback function for when API fails
export const generateFallbackRecommendations = (preferences: UserPreferences): ProjectRecommendation[] => {
  const baseProjects: Omit<ProjectRecommendation, 'id'>[] = [
    {
      title: 'Smart Task Management System',
      description: 'Build a comprehensive task management application with team collaboration features, deadline tracking, and productivity analytics.',
      features: ['Team collaboration', 'Deadline notifications', 'Progress tracking', 'File attachments', 'Time tracking', 'Analytics dashboard'],
      difficulty: 'Intermediate',
      techStack: preferences.techStack.includes('React') ? ['React', 'Node.js', 'MongoDB'] : ['HTML', 'CSS', 'JavaScript'],
      tags: ['#productivity', '#collaboration', '#fullstack', '#dashboard'],
      estimatedTime: '3-4 weeks',
      starterTutorials: ['Building CRUD Applications', 'User Authentication Basics'],
      githubBoilerplates: ['https://github.com/example/task-manager-starter']
    },
    {
      title: 'Personal Finance Tracker',
      description: 'Create a personal finance application that helps users track expenses, set budgets, and achieve financial goals with beautiful visualizations.',
      features: ['Expense categorization', 'Budget planning', 'Goal setting', 'Data visualization', 'Bank integration', 'Monthly reports'],
      difficulty: preferences.skillLevel === 'Beginner' ? 'Beginner' : 'Intermediate',
      techStack: preferences.techStack.filter(tech => ['HTML', 'CSS', 'JavaScript', 'React'].includes(tech)),
      tags: ['#finance', '#budgeting', '#charts', '#personal'],
      estimatedTime: '2-3 weeks',
      starterTutorials: ['Chart.js for Data Visualization', 'Local Storage Management'],
      githubBoilerplates: ['https://github.com/example/finance-tracker']
    },
    {
      title: 'AI-Powered Code Review Assistant',
      description: 'Develop an intelligent code review tool that analyzes code quality, suggests improvements, and helps maintain coding standards.',
      features: ['Code quality analysis', 'Best practice suggestions', 'Security vulnerability detection', 'Performance recommendations', 'Integration with Git', 'Custom rules'],
      difficulty: 'Advanced',
      techStack: preferences.techStack.includes('Python') ? ['Python', 'Node.js', 'React'] : ['JavaScript', 'Node.js', 'React'],
      tags: ['#ai', '#code-analysis', '#developer-tools', '#automation'],
      estimatedTime: '4-6 weeks',
      starterTutorials: ['Working with AST Parsers', 'Building Developer Tools'],
      githubBoilerplates: ['https://github.com/example/code-review-ai']
    },
    {
      title: 'Healthcare Appointment System',
      description: 'Build a comprehensive healthcare management system for booking appointments, managing patient records, and telemedicine consultations.',
      features: ['Appointment scheduling', 'Patient portal', 'Doctor dashboard', 'Medical records', 'Video consultations', 'Prescription management'],
      difficulty: 'Advanced',
      techStack: preferences.techStack.includes('React') ? ['React', 'Node.js', 'MongoDB', 'Express.js'] : ['HTML', 'CSS', 'JavaScript', 'Node.js'],
      tags: ['#healthcare', '#appointments', '#telemedicine', '#fullstack'],
      estimatedTime: '5-7 weeks',
      starterTutorials: ['HIPAA Compliance Basics', 'Video Calling Integration'],
      githubBoilerplates: ['https://github.com/example/healthcare-system']
    },
    {
      title: 'Open Source Learning Platform',
      description: 'Create an open-source educational platform where users can create courses, track progress, and collaborate on learning projects.',
      features: ['Course creation', 'Progress tracking', 'Discussion forums', 'Peer reviews', 'Certificates', 'Mobile responsive'],
      difficulty: 'Intermediate',
      techStack: preferences.techStack.includes('React') ? ['React', 'Node.js', 'MongoDB'] : ['HTML', 'CSS', 'JavaScript'],
      tags: ['#education', '#open-source', '#learning', '#community'],
      estimatedTime: '4-5 weeks',
      starterTutorials: ['Building Learning Management Systems', 'User Progress Tracking'],
      githubBoilerplates: ['https://github.com/example/learning-platform']
    }
  ];

  // Filter projects based on user preferences
  let filteredProjects = baseProjects.filter(project => {
    // Filter by skill level
    if (preferences.skillLevel === 'Beginner' && project.difficulty === 'Advanced') return false;
    if (preferences.skillLevel === 'Advanced' && project.difficulty === 'Beginner') return false;
    
    // Filter by interest areas
    const interestKeywords = {
      'Productivity': ['task', 'productivity', 'management'],
      'Healthcare': ['healthcare', 'medical', 'health'],
      'Education': ['learning', 'education', 'course'],
      'Finance': ['finance', 'budget', 'money'],
      'AI Tools': ['ai', 'intelligent', 'automation'],
      'Open Source': ['open-source', 'community', 'collaboration'],
      'E-commerce': ['shop', 'commerce', 'store', 'marketplace'],
      'Social Media': ['social', 'chat', 'community', 'network'],
      'Entertainment': ['game', 'entertainment', 'media', 'fun'],
      'Travel': ['travel', 'location', 'maps', 'tourism'],
      'Food & Dining': ['food', 'recipe', 'restaurant', 'dining'],
      'Fitness': ['fitness', 'health', 'workout', 'exercise'],
      'Real Estate': ['property', 'real estate', 'housing', 'rental'],
      'Transportation': ['transport', 'logistics', 'delivery', 'mobility'],
      'Environmental': ['environment', 'green', 'sustainability', 'eco'],
      'Developer Tools': ['development', 'coding', 'programming', 'tools']
    };

    const interestAreas = Array.isArray(preferences.interestArea) ? preferences.interestArea : [preferences.interestArea];
    const allKeywords = interestAreas.flatMap(area => interestKeywords[area as keyof typeof interestKeywords] || []);

    if (allKeywords.length > 0) {
      const projectText = (project.title + ' ' + project.description).toLowerCase();
      return allKeywords.some(keyword => projectText.includes(keyword));
    }
    
    return true;
  });

  // If no projects match, return first 3 projects
  if (filteredProjects.length === 0) {
    filteredProjects = baseProjects.slice(0, 3);
  }

  // Add IDs and return up to 4 projects
  return filteredProjects.slice(0, 4).map((project, index) => ({
    ...project,
    id: `fallback-${Date.now()}-${index}`
  }));
};  