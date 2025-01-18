import { NextRequest, NextResponse } from "next/server";

import { auth } from "@clerk/nextjs/server";
import { z } from "zod";

import { processMeeting } from "@/lib/assembly";
import { db } from "@/server/db";

const bodyParser = z.object({
  meetingUrl: z.string(),
  meetingId: z.string(),
});

export const maxDuration = 300; // Function Timeout Limit Defined due to Vercel Limitations. (5 Minutes)

export async function POST(req: NextRequest) {
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await req.json();
    const { meetingUrl, meetingId } = bodyParser.parse(body);
    const summaries = await processMeeting(meetingUrl);

    await db.issue.createMany({
      data: summaries.map((summary) => ({
        start: summary.start,
        end: summary.end,
        gist: summary.gist,
        headline: summary.headline,
        summary: summary.summary,
        meetingId,
      })),
    });

    await db.meeting.update({
      where: {
        id: meetingId,
      },
      data: {
        status: "COMPLETED",
        name: summaries[0]!.headline,
      },
    });

    return NextResponse.json({ success: true }, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      { error: (error as Error).message },
      { status: 500 }
    );
  }
}
