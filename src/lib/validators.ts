import { z } from "zod";

export const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  lastName: z.string().optional(),
  imageUrl: z.string().optional(),
  firstName: z.string().optional(),
});

export const projectSchema = z.object({
  name: z.string(),
  githubUrl: z.string(),
  githubToken: z.string().optional(),
});
