import { string, z } from "zod";

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

export const questionSchema = z.object({
  projectId: z.string(),
  question: z.string(),
  answer: z.string(),
  filesReference: z.any(),
});

export const meetingSchema = z.object({
  projectId: z.string(),
  meetingUrl: z.string().url(),
  name: z.string(),
});

export const creditSchema = z.object({
  githubUrl: z.string(),
  githubToken: z.string().optional(),
});
