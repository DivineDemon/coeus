import { z } from "zod";

import { pollCommits } from "@/lib/github";
import { createTRPCRouter, privateProcedure } from "@/server/api/trpc";

export const commitRouter = createTRPCRouter({
  getCommits: privateProcedure
    .input(z.object({ projectId: z.string() }))
    .query(async ({ ctx, input }) => {
      pollCommits(input.projectId)
        .then()
        .catch((error) => {
          throw new Error(error);
        });

      return await ctx.db.commit.findMany({
        where: {
          projectId: input.projectId,
        },
      });
    }),
});
