'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';

interface User {
  id: string;
  email: string;
  name: string;
}

interface Session {
  user: User;
  expires?: string;
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

  // Check for existing session on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    
    if (token) {
      const user = decodeToken(token);
      if (user) {
        setSession({ user });
      } else {
        localStorage.removeItem('token');
      }
    }
    
    setLoading(false);
  }, [decodeToken]);

  const signIn = async (email: string, password: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Login failed: ${response.status}`);
      }

      const data = await response.json();

      localStorage.setItem('token', data.access_token);
      const user = decodeToken(data.access_token);

      if (user) {
        setSession({ user });
      }

      return data;
    } catch (err: any) {
      if (err.message.includes('fetch') || err.message.includes('NetworkError')) {
        throw new Error('Cannot connect to server. Please make sure the backend is running on http://localhost:8000');
      }
      throw err;
    }
  };

  const signUp = async (name: string, email: string, password: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
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