import { z } from "zod";

import { checkCredits } from "@/lib/github";
import { creditSchema, userSchema } from "@/lib/validators";
import {
  createTRPCRouter,
  privateProcedure,
  publicProcedure,
} from "@/server/api/trpc";

export const userRouter = createTRPCRouter({
  syncUser: publicProcedure
    .input(userSchema)
    .mutation(async ({ ctx, input }) => {
      return ctx.db.user.upsert({
        where: {
          email: input.email,
        },
        update: {
          imageUrl: input.imageUrl,
          firstName: input.firstName,
          lastName: input.lastName,
        },
        create: {
          id: input.id,
          email: input.email,
          imageUrl: input.imageUrl,
          firstName: input.firstName,
          lastName: input.lastName,
        },
      });
    }),
  findUser: privateProcedure.query(async ({ ctx }) => {
    return await ctx.db.user.findUnique({
      where: {
        id: ctx.user.id,
      },
    });
  }),
  linkToProject: publicProcedure
    .input(z.object({ userId: z.string(), projectId: z.string() }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.userToProject.create({
        data: {
          userId: input.userId,
          projectId: input.projectId,
        },
      });
    }),
  getUser: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      return await ctx.db.user.findUnique({
        where: {
          id: input.id,
        },
      });
    }),
  getMyCredits: privateProcedure.query(async ({ ctx }) => {
    return await ctx.db.user.findUnique({
      where: {
        id: ctx.user.id,
      },
      select: {
        credits: true,
      },
    });
  }),
  seeCredits: privateProcedure
    .input(creditSchema)
    .mutation(async ({ ctx, input }) => {
      const fileCount = await checkCredits(input.githubUrl, input.githubToken);
      const userCredits = await ctx.db.user.findUnique({
        where: {
          id: ctx.user.id,
        },
        select: {
          credits: true,
        },
      });

      return {
        fileCount,
        userCredits: userCredits?.credits || 0,
      };
    }),
});
