'use client';

import { signIn, signUp, signOut, useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export const useAuth = () => {
  const { data: session, isPending, error } = useSession();
  const router = useRouter();

  const signUpUser = async (name: string, email: string, password: string) => {
    const result = await signUp.email({
      email,
      password,
      name,
      callbackURL: "/signin",
    });
    if (result.error) throw new Error(result.error.message || "Failed to sign up");

    // After successful signup with Better Auth, ensure user exists in backend
    if (result.data) {
      await ensureBackendUserExists(result.data.user);
    }

    return result.data;
  };

  const signInUser = async (email: string, password: string) => {
    const result = await signIn.email({
      email,
      password,
      callbackURL: "/dashboard",
    });
    if (result.error) throw new Error(result.error.message || "Failed to sign in");

    // After successful sign in with Better Auth, ensure user exists in backend
    if (result.data && result.data.user) {
      await ensureBackendUserExists(result.data.user);
    }

    return result.data;
  };

  const ensureBackendUserExists = async (user: any) => {
    try {
      // Get the session token to pass to the backend
      const sessionResult = await authClient.getSession();
      const token = sessionResult.data?.session?.token;

      if (!token) {
        console.warn('No session token available for backend user creation');
        return;
      }

      // Call backend endpoint to ensure user exists in backend database
      const response = await fetch('http://localhost:8000/api/auth/auto-create-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          sub: user.id,  // Better Auth user ID
          email: user.email,
          name: user.name || user.email.split('@')[0]
        })
      });

      if (!response.ok) {
        console.warn('Backend user creation failed:', await response.text());
      }
    } catch (err) {
      console.warn('Error ensuring backend user exists:', err);
    }
  };

  const logoutUser = async () => {
    await signOut({
      fetchOptions: {
        onSuccess: () => {
          router.push("/signin");
        },
      },
    });
  };

  return {
    session,
    loading: isPending,
    error,
    signUp: signUpUser,
    signIn: signInUser,
    signOut: logoutUser,
  };
};

export default useAuth;