import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: undefined, // Using in-memory database for development
  socialProviders: {}, // No social providers configured
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  secret: process.env.BETTER_AUTH_SECRET || "mySuperSecretBetterAuthSecret32Chars", // Use same secret as backend
  baseURL: process.env.BETTER_AUTH_BASE_URL || "http://localhost:3000",
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET || "mySuperSecretBetterAuthSecret32Chars", // Ensure JWT uses the same secret
      expiresIn: "7d",
    })
  ],
});
