import { questionSchema } from "@/lib/validators";
import { createTRPCRouter, privateProcedure } from "@/server/api/trpc";

export const questionRouter = createTRPCRouter({
  saveAnswer: privateProcedure
    .input(questionSchema)
    .mutation(async ({ ctx, input }) => {
      return ctx.db.question.create({
        data: {
          answer: input.answer,
          userId: ctx.user.userId!,
          question: input.question,
          projectId: input.projectId,
          fileReferences: input.filesReference,
        },
      });
    }),
});
