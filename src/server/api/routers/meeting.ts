import { z } from "zod";

import { meetingSchema } from "@/lib/validators";
import { createTRPCRouter, privateProcedure } from "@/server/api/trpc";

export const meetingRouter = createTRPCRouter({
  uploadMeeting: privateProcedure
    .input(meetingSchema)
    .mutation(async ({ ctx, input }) => {
      return ctx.db.meeting.create({
        data: {
          ...input,
          status: "PROCESSING",
        },
      });
    }),
  getMeetings: privateProcedure
    .input(z.object({ projectId: z.string() }))
    .query(async ({ ctx, input }) => {
      return await ctx.db.meeting.findMany({
        where: {
          projectId: input.projectId,
        },
        include: {
          Issue: true,
        },
      });
    }),
});
