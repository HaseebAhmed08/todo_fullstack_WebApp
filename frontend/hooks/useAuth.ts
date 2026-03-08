'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Session {
  user: User;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface AuthError {
  detail: string;
}

export const useAuth = () => {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Decode JWT token and get user info
  const decodeToken = useCallback((token: string): User | null => {
    try {
      const payload = jwtDecode(token);
      return {
        id: payload.sub || '',
        email: (payload as any).email || '',
        name: (payload as any).name || '',
      };
    } catch (err) {
      console.error('Error decoding token:', err);
      return null;
    }
  }, []);

  // Get token from localStorage
  const getToken = useCallback(() => {
    return localStorage.getItem('token');
  }, []);

  // Check for existing session on mount
  useEffect(() => {
    const token = getToken();

    if (token) {
      const user = decodeToken(token);
      if (user) {
        setSession({ user });
      } else {
        localStorage.removeItem('token');
      }
    }

    setLoading(false);
  }, [getToken, decodeToken]);

  const signIn = async (email: string, password: string) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData: AuthError = await response.json().catch(() => ({ detail: 'Login failed' }));
        throw new Error(errorData.detail || `Login failed: ${response.status}`);
      }

      const data: LoginResponse = await response.json();

      localStorage.setItem('token', data.access_token);
      const user = decodeToken(data.access_token);

      if (user) {
        setSession({ user });
      }

      return { user };
    } catch (err: any) {
      if (err.message.includes('fetch') || err.message.includes('NetworkError')) {
        throw new Error('Cannot connect to server. Please make sure the backend is running on http://localhost:8000');
      }
      throw err;
    }
  };

  const signUp = async (name: string, email: string, password: string) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      if (!response.ok) {
        const errorData: AuthError = await response.json().catch(() => ({ detail: 'Signup failed' }));
        throw new Error(errorData.detail || `Signup failed: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (err: any) {
      if (err.message.includes('fetch') || err.message.includes('NetworkError')) {
        throw new Error('Cannot connect to server. Please make sure the backend is running on http://localhost:8000');
      }
      throw err;
    }
  };

  const signOut = async () => {
    localStorage.removeItem('token');
    setSession(null);
    router.push('/signin');
  };

  return {
    session,
    loading,
    signIn,
    signUp,
    signOut,
  };
};

export default useAuth;