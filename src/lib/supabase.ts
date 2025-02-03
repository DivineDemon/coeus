import { createBrowserClient } from "@supabase/ssr";

import { env } from "@/env";

export function createClient() {
  return createBrowserClient(
    env.NEXT_PUBLIC_SUPABASE_URL!,
    env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}

export async function uploadFile({
  file,
  bucket,
  folder,
}: {
  file: File;
  bucket: string;
  folder?: string;
}) {
  const { storage } = createClient();
  const path = `${folder ? `${folder}/` : ""}${file.name}`;
  const { data, error } = await storage.from(bucket).upload(path, file);

  if (error) {
    throw new Error(error.message);
  }

  return `${env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/${bucket}/${data.path}`;
}
