import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// Types
export interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in-progress' | 'done';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  dueDate?: Date;
  assignedTo?: string;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
  subtasks: Task[];
  tags: string[];
}

export interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  authorId: string;
  isPublic: boolean;
  collaborators: string[];
  aiSummary?: string;
}

export interface Expense {
  id: string;
  description: string;
  amount: number;
  date: Date;
  category: string;
}

export interface Budget {
  id: string;
  name: string;
  description: string;
  totalAmount: number;
  spent: number;
  category: string;
  createdAt: Date;
  updatedAt: Date;
  expenses: Expense[];
}

// State interface
interface AppState {
  tasks: Task[];
  notes: Note[];
  budgets: Budget[];
}

// Action types
type AppAction =
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: { id: string; updates: Partial<Task> } }
  | { type: 'DELETE_TASK'; payload: string }
  | { type: 'ADD_NOTE'; payload: Note }
  | { type: 'UPDATE_NOTE'; payload: { id: string; updates: Partial<Note> } }
  | { type: 'DELETE_NOTE'; payload: string }
  | { type: 'ADD_BUDGET'; payload: Budget }
  | { type: 'UPDATE_BUDGET'; payload: { id: string; updates: Partial<Budget> } }
  | { type: 'DELETE_BUDGET'; payload: string };

// Initial state
const initialState: AppState = {
  tasks: [
    {
      id: '1',
      title: 'Complete project proposal',
      description: 'Write and submit the project proposal for the new client',
      status: 'todo',
      priority: 'high',
      dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
      createdBy: '1',
      createdAt: new Date(),
      updatedAt: new Date(),
      subtasks: [],
      tags: ['work', 'proposal', 'client'],
    },
    {
      id: '2',
      title: 'Review code changes',
      description: 'Review pull requests and provide feedback',
      status: 'in-progress',
      priority: 'medium',
      createdBy: '1',
      createdAt: new Date(),
      updatedAt: new Date(),
      subtasks: [],
      tags: ['code', 'review', 'team'],
    },
  ],
  notes: [
    {
      id: '1',
      title: 'Meeting Notes - Project Kickoff',
      content: 'Discussed project timeline, deliverables, and team responsibilities. Key decisions made about technology stack and architecture.',
      tags: ['meeting', 'project', 'kickoff'],
      createdAt: new Date(),
      updatedAt: new Date(),
      authorId: '1',
      isPublic: false,
      collaborators: [],
    },
    {
      id: '2',
      title: 'Learning Resources',
      content: 'React hooks, TypeScript best practices, and modern CSS techniques. Need to practice more with real projects.',
      tags: ['learning', 'react', 'typescript', 'css'],
      createdAt: new Date(),
      updatedAt: new Date(),
      authorId: '1',
      isPublic: false,
      collaborators: [],
    },
  ],
  budgets: [
    {
      id: '1',
      name: 'Monthly Groceries',
      description: 'Budget for food and household items',
      totalAmount: 500,
      spent: 320,
      category: 'Food',
      createdAt: new Date(),
      updatedAt: new Date(),
      expenses: [
        {
          id: '1',
          description: 'Supermarket shopping',
          amount: 120,
          date: new Date(),
          category: 'Food',
        },
        {
          id: '2',
          description: 'Restaurant meals',
          amount: 200,
          date: new Date(),
          category: 'Food',
        },
      ],
    },
    {
      id: '2',
      name: 'Entertainment',
      description: 'Movies, games, and leisure activities',
      totalAmount: 200,
      spent: 150,
      category: 'Entertainment',
      createdAt: new Date(),
      updatedAt: new Date(),
      expenses: [
        {
          id: '3',
          description: 'Movie tickets',
          amount: 50,
          date: new Date(),
          category: 'Entertainment',
        },
        {
          id: '4',
          description: 'Gaming subscription',
          amount: 100,
          date: new Date(),
          category: 'Entertainment',
        },
      ],
    },
  ],
};

// Reducer
function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'ADD_TASK':
      return {
        ...state,
        tasks: [...state.tasks, action.payload],
      };
    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id
            ? { ...task, ...action.payload.updates }
            : task
        ),
      };
    case 'DELETE_TASK':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
      };
    case 'ADD_NOTE':
      return {
        ...state,
        notes: [...state.notes, action.payload],
      };
    case 'UPDATE_NOTE':
      return {
        ...state,
        notes: state.notes.map(note =>
          note.id === action.payload.id
            ? { ...note, ...action.payload.updates }
            : note
        ),
      };
    case 'DELETE_NOTE':
      return {
        ...state,
        notes: state.notes.filter(note => note.id !== action.payload),
      };
    case 'ADD_BUDGET':
      return {
        ...state,
        budgets: [...state.budgets, action.payload],
      };
    case 'UPDATE_BUDGET':
      return {
        ...state,
        budgets: state.budgets.map(budget =>
          budget.id === action.payload.id
            ? { ...budget, ...action.payload.updates }
            : budget
        ),
      };
    case 'DELETE_BUDGET':
      return {
        ...state,
        budgets: state.budgets.filter(budget => budget.id !== action.payload),
      };
    default:
      return state;
  }
}

// Context
interface AppContextType {
  state: AppState;
  addTask: (task: Task) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  deleteTask: (id: string) => void;
  addNote: (note: Note) => void;
  updateNote: (id: string, updates: Partial<Note>) => void;
  deleteNote: (id: string) => void;
  addBudget: (budget: Budget) => void;
  updateBudget: (id: string, updates: Partial<Budget>) => void;
  deleteBudget: (id: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

// Provider component
interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  const addTask = (task: Task) => {
    dispatch({ type: 'ADD_TASK', payload: task });
  };

  const updateTask = (id: string, updates: Partial<Task>) => {
    dispatch({ type: 'UPDATE_TASK', payload: { id, updates } });
  };

  const deleteTask = (id: string) => {
    dispatch({ type: 'DELETE_TASK', payload: id });
  };

  const addNote = (note: Note) => {
    dispatch({ type: 'ADD_NOTE', payload: note });
  };

  const updateNote = (id: string, updates: Partial<Note>) => {
    dispatch({ type: 'UPDATE_NOTE', payload: { id, updates } });
  };

  const deleteNote = (id: string) => {
    dispatch({ type: 'DELETE_NOTE', payload: id });
  };

  const addBudget = (budget: Budget) => {
    dispatch({ type: 'ADD_BUDGET', payload: budget });
  };

  const updateBudget = (id: string, updates: Partial<Budget>) => {
    dispatch({ type: 'UPDATE_BUDGET', payload: { id, updates } });
  };

  const deleteBudget = (id: string) => {
    dispatch({ type: 'DELETE_BUDGET', payload: id });
  };

  const value: AppContextType = {
    state,
    addTask,
    updateTask,
    deleteTask,
    addNote,
    updateNote,
    deleteNote,
    addBudget,
    updateBudget,
    deleteBudget,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

// Hook
export const useApp = (): AppContextType => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

// Destructured state getters for convenience
export const useTasks = () => {
  const { state, addTask, updateTask, deleteTask } = useApp();
  return { tasks: state.tasks, addTask, updateTask, deleteTask };
};

export const useNotes = () => {
  const { state, addNote, updateNote, deleteNote } = useApp();
  return { notes: state.notes, addNote, updateNote, deleteNote };
};

export const useBudgets = () => {
  const { state, addBudget, updateBudget, deleteBudget } = useApp();
  return { budgets: state.budgets, addBudget, updateBudget, deleteBudget };
};
