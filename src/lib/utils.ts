import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

import { db } from "@/server/db";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
