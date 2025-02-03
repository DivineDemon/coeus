import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    NODE_ENV: z
      .enum(["development", "test", "production"])
      .default("development"),
    OPENAI_KEY: z.string().regex(/^sk-[a-zA-Z0-9]{48}$/, {
      message: "Invalid OpenAI API key format.",
    }),
    ASSEMBLY_AI_KEY: z.string().regex(/^[a-f0-9]{32}$/, {
      message: "Invalid Assembly AI key format.",
    }),
    STRIPE_SECRET_KEY: z
      .string()
      .regex(
        /^sk_(test|live)_[0-9a-zA-Z]{24,}$/,
        "Invalid Stripe secret key format"
      ),
    STRIPE_PUBLISHABLE_KEY: z
      .string()
      .regex(
        /^pk_(test|live)_[0-9a-zA-Z]{24,}$/,
        "Invalid Stripe secret key format"
      ),
    STRIPE_WEBHOOK_SECRET: z
      .string()
      .regex(
        /^whsec_[a-zA-Z0-9]{32}$/,
        "Invalid Stripe Webhook Secret Format!"
      ),
    KINDE_SITE_URL: z.string().url(),
    KINDE_ISSUER_URL: z.string().url(),
    KINDE_CLIENT_ID: z.string().min(1),
    KINDE_CLIENT_SECRET: z.string().min(1),
    KINDE_POST_LOGIN_REDIRECT_URL: z.string().url(),
    KINDE_POST_LOGOUT_REDIRECT_URL: z.string().url(),
  },
  client: {
    NEXT_PUBLIC_APP_URL: z.string(),
    NEXT_PUBLIC_SUPABASE_URL: z
      .string()
      .url()
      .regex(
        /^https:\/\/[a-zA-Z0-9\-]+\.supabase\.co$/,
        "Invalid Supabase project URL"
      ),
    NEXT_PUBLIC_SUPABASE_ANON_KEY: z
      .string()
      .regex(
        /^eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/,
        "Invalid Supabase anon key"
      ),
    NEXT_PUBLIC_KINDE_EMAIL_CONNECTION_ID: z.string().min(1),
    NEXT_PUBLIC_KINDE_GITHUB_CONNECTION_ID: z.string().min(1),
    NEXT_PUBLIC_KINDE_GOOGLE_CONNECTION_ID: z.string().min(1),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    NODE_ENV: process.env.NODE_ENV,
    OPENAI_KEY: process.env.OPENAI_KEY,
    ASSEMBLY_AI_KEY: process.env.ASSEMBLY_AI_KEY,
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    STRIPE_PUBLISHABLE_KEY: process.env.STRIPE_PUBLISHABLE_KEY,
    STRIPE_WEBHOOK_SECRET: process.env.STRIPE_WEBHOOK_SECRET,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    KINDE_SITE_URL: process.env.KINDE_SITE_URL,
    KINDE_CLIENT_ID: process.env.KINDE_CLIENT_ID,
    KINDE_ISSUER_URL: process.env.KINDE_ISSUER_URL,
    KINDE_CLIENT_SECRET: process.env.KINDE_CLIENT_SECRET,
    KINDE_POST_LOGIN_REDIRECT_URL: process.env.KINDE_POST_LOGIN_REDIRECT_URL,
    KINDE_POST_LOGOUT_REDIRECT_URL: process.env.KINDE_POST_LOGOUT_REDIRECT_URL,
    NEXT_PUBLIC_KINDE_EMAIL_CONNECTION_ID:
      process.env.NEXT_PUBLIC_KINDE_EMAIL_CONNECTION_ID,
    NEXT_PUBLIC_KINDE_GITHUB_CONNECTION_ID:
      process.env.NEXT_PUBLIC_KINDE_GITHUB_CONNECTION_ID,
    NEXT_PUBLIC_KINDE_GOOGLE_CONNECTION_ID:
      process.env.NEXT_PUBLIC_KINDE_GOOGLE_CONNECTION_ID,
  },
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});
