'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { useSession } from '@better-auth/react';

// Define types
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
}

interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

interface AppState {
  user: User | null;
  tasks: Task[] | null;
  loading: boolean;
  error: string | null;
}

type AppAction =
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'SET_TASKS'; payload: Task[] }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: Task }
  | { type: 'DELETE_TASK'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null };

// Initial state
const initialState: AppState = {
  user: null,
  tasks: null,
  loading: false,
  error: null,
};

// Reducer function
const appReducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_TASKS':
      return { ...state, tasks: action.payload };
    case 'ADD_TASK':
      if (!state.tasks) return { ...state, tasks: [action.payload] };
      return { ...state, tasks: [...state.tasks, action.payload] };
    case 'UPDATE_TASK':
      if (!state.tasks) return state;
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
      };
    case 'DELETE_TASK':
      if (!state.tasks) return state;
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

// Create context
interface AppContextType extends AppState {
  dispatch: React.Dispatch<AppAction>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

// Provider component
export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);
  const { session } = useSession();

  // Update user in state based on session
  useEffect(() => {
    if (session) {
      // In a real app, you'd fetch user details from the API
      const user: User = {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name || '',
        createdAt: new Date(session.user.createdAt),
        updatedAt: new Date(),
      };
      dispatch({ type: 'SET_USER', payload: user });
    } else {
      dispatch({ type: 'SET_USER', payload: null });
    }
  }, [session]);

  return (
    <AppContext.Provider value={{ ...state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook to use the context
export const useAppContext = (): AppContextType => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};