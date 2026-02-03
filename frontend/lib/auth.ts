import { betterAuth } from "better-auth";
import { neon } from "@neondatabase/serverless";
import { jwt } from "better-auth/plugins";

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is not set");
}

export const auth = betterAuth({
  database: {
    db: neon(process.env.DATABASE_URL),
    type: "postgres",
  },
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt({
        jwt: {
            expirationTime: "7d",
        }
    })
  ],
});
