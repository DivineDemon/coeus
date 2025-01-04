import { projectSchema } from "@/lib/validators";
import { createTRPCRouter, privateProcedure } from "@/server/api/trpc";

export const projectRouter = createTRPCRouter({
  createProject: privateProcedure
    .input(projectSchema)
    .mutation(async ({ ctx, input }) => {
      return ctx.db.project.create({
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
});
