import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    NODE_ENV: z
      .enum(["development", "test", "production"])
      .default("development"),
    CLERK_SECRET_KEY: z.string().regex(/^sk_test_[A-Za-z0-9-\.]+$/, {
      message: "Invalid CLERK_SECRET_KEY format",
    }),
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
  },
  client: {
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: z
      .string()
      .regex(/^pk_test_[A-Za-z0-9]+$/, {
        message: "Invalid NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY format",
      }),
    NEXT_PUBLIC_CLERK_SIGN_IN_URL: z.string().startsWith("/"),
    NEXT_PUBLIC_CLERK_SIGN_UP_URL: z.string().startsWith("/"),
    NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL: z.string().startsWith("/"),
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
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    NODE_ENV: process.env.NODE_ENV,
    CLERK_SECRET_KEY: process.env.CLERK_SECRET_KEY,
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY:
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY,
    NEXT_PUBLIC_CLERK_SIGN_IN_URL: process.env.NEXT_PUBLIC_CLERK_SIGN_IN_URL,
    NEXT_PUBLIC_CLERK_SIGN_UP_URL: process.env.NEXT_PUBLIC_CLERK_SIGN_UP_URL,
    NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL:
      process.env.NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL,
    OPENAI_KEY: process.env.OPENAI_KEY,
    ASSEMBLY_AI_KEY: process.env.ASSEMBLY_AI_KEY,
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    STRIPE_PUBLISHABLE_KEY: process.env.STRIPE_PUBLISHABLE_KEY,
    STRIPE_WEBHOOK_SECRET: process.env.STRIPE_WEBHOOK_SECRET,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  },
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});
