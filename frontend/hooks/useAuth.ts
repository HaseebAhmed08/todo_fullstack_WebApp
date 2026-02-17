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
      callbackURL: "/login",
    });
    if (result.error) throw new Error(result.error.message || "Failed to sign up");

    return result.data;
  };

  const signInUser = async (email: string, password: string) => {
    const result = await signIn.email({
      email,
      password,
      callbackURL: "/dashboard",
    });
    if (result.error) throw new Error(result.error.message || "Failed to sign in");

    return result.data;
  };

  const logoutUser = async () => {
    await signOut({
      fetchOptions: {
        onSuccess: () => {
          router.push("/login");
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