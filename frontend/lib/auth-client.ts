import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
    baseURL: process.env.BETTER_AUTH_BASE_URL || "http://localhost:3000/api/auth",
});

export const { signIn, signUp, useSession, signOut } = authClient;
