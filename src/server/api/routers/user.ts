import { userSchema } from "@/lib/validators";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";

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
});
