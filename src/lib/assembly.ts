import { AssemblyAI } from "assemblyai";

import { env } from "@/env";

const client = new AssemblyAI({
  apiKey: env.ASSEMBLY_AI_KEY,
});

const msToTime = (ms: number) => {
  const seconds = ms / 1000;
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  return `${minutes.toString().padStart(2, "0")}:${remainingSeconds.toString().padStart(2, "0")}`;
};

export async function processMeeting(meetingUrl: string) {
  const transcript = await client.transcripts.transcribe({
    audio: meetingUrl,
    auto_chapters: true,
  });

  if (!transcript.text) {
    throw new Error("No Transcript Found!");
  }

  const summaries =
    transcript.chapters?.map((chapter) => ({
      start: msToTime(chapter.start),
      end: msToTime(chapter.end),
      gist: chapter.gist,
      headline: chapter.headline,
      summary: chapter.summary,
    })) || [];

  return summaries;
}
