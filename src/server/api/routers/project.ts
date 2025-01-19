import { z } from "zod";

import { pollCommits } from "@/lib/github";
import { indexGithubRepo } from "@/lib/github-loader";
import { projectSchema } from "@/lib/validators";
import { createTRPCRouter, privateProcedure } from "@/server/api/trpc";

export const projectRouter = createTRPCRouter({
  createProject: privateProcedure
    .input(projectSchema)
    .mutation(async ({ ctx, input }) => {
      const project = await ctx.db.project.create({
        data: {
          name: input.name,
          githubUrl: input.githubUrl,
          UserToProject: {
            create: {
              userId: ctx.user.userId!,
            },
          },
        },
      });

      await indexGithubRepo(project.id, input.githubUrl, input.githubToken);
      await pollCommits(project.id);

      return project;
    }),
  getProjects: privateProcedure.query(async ({ ctx }) => {
    return ctx.db.project.findMany({
      where: {
        UserToProject: {
          some: {
            userId: ctx.user.userId!,
          },
        },
        deletedAt: null,
      },
    });
  }),
  archiveProject: privateProcedure
    .input(z.object({ projectId: z.string() }))
    .mutation(async ({ ctx, input }) => {
      return await ctx.db.project.update({
        where: {
          id: input.projectId,
        },
        data: {
          deletedAt: new Date(),
        },
      });
    }),
  getProject: privateProcedure
    .input(z.object({ projectId: z.string() }))
    .query(async ({ ctx, input }) => {
      return await ctx.db.project.findUnique({
        where: {
          id: input.projectId,
        },
      });
    }),
  getTeamMembers: privateProcedure
    .input(z.object({ projectId: z.string() }))
    .query(async ({ ctx, input }) => {
      return await ctx.db.userToProject.findMany({
        where: {
          projectId: input.projectId,
        },
        include: {
          user: true,
        },
      });
    }),
});
