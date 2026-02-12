import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { Kysely, PostgresDialect } from "kysely"; // Import Kysely
import { jwt } from "better-auth/plugins";

// Use safe fallback for DATABASE_URL
const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl) {
  console.warn("DATABASE_URL is not set. Using fallback configuration.");
}

// Check if DATABASE_URL is a real PostgreSQL connection string
const isValidPostgresUrl = databaseUrl && databaseUrl.startsWith('postgresql://');

export const auth = betterAuth({
  database: isValidPostgresUrl
    ? {
      db: new Kysely({
        dialect: new PostgresDialect({
          pool: new Pool({
            connectionString: databaseUrl,
          }),
        }),
      }),
      type: "postgres",
    }
    : undefined,
  emailAndPassword: {
    enabled: true,
  },
  baseURL: process.env.BETTER_AUTH_BASE_URL || "http://localhost:3000",
  plugins: [
    jwt({
      jwt: {
        expirationTime: "7d",
      }
    })
  ],
});
