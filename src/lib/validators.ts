import { z } from "zod";

export const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  imageUrl: z.string(),
  firstName: z.string(),
  lastName: z.string(),
});
