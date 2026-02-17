// Mock authentication system for development
// This bypasses Better Auth and directly handles authentication for testing purposes

// Store mock user data
let mockUser: any = null;
let mockToken: string | null = null;

export const mockAuth = {
  // Simulate login
  login: (email: string, password: string) => {
    // In a real scenario, this would call the backend
    mockUser = {
      id: 'mock-user-id-123',
      email,
      name: email.split('@')[0] // Simple name from email
    };
    
    // Generate a mock token
    mockToken = `mock-token-${Date.now()}`;
    
    // Store in localStorage for persistence
    if (typeof window !== 'undefined') {
      localStorage.setItem('mock-auth-user', JSON.stringify(mockUser));
      localStorage.setItem('mock-auth-token', mockToken);
    }
    
    return { user: mockUser, token: mockToken };
  },

  // Simulate logout
  logout: () => {
    mockUser = null;
    mockToken = null;
    
    if (typeof window !== 'undefined') {
      localStorage.removeItem('mock-auth-user');
      localStorage.removeItem('mock-auth-token');
    }
  },

  // Get current user/session
  getSession: () => {
    if (mockUser && mockToken) {
      return { data: { user: mockUser, session: { token: mockToken } }, isLoading: false };
    }
    
    // Try to restore from localStorage
    if (typeof window !== 'undefined') {
      const storedUser = localStorage.getItem('mock-auth-user');
      const storedToken = localStorage.getItem('mock-auth-token');
      
      if (storedUser && storedToken) {
        mockUser = JSON.parse(storedUser);
        mockToken = storedToken;
        return { data: { user: mockUser, session: { token: mockToken } }, isLoading: false };
      }
    }
    
    return { data: null, isLoading: false };
  },

  // Get the current token
  getToken: () => {
    if (!mockToken && typeof window !== 'undefined') {
      mockToken = localStorage.getItem('mock-auth-token');
    }
    return mockToken;
  }
};