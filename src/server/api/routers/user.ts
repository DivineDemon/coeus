import { currentUser } from "@clerk/nextjs/server";

import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";

export const userRouter = createTRPCRouter({
  syncUser: publicProcedure.mutation(async ({ ctx }) => {
    const auth = await currentUser();

    return ctx.db.user.upsert({
      where: {
        email: auth?.emailAddresses[0]?.emailAddress,
      },
      update: {
        imageUrl: auth?.imageUrl,
        firstName: auth?.firstName,
        lastName: auth?.lastName,
      },
      create: {
        id: auth?.id,
        email: auth?.emailAddresses[0]!.emailAddress!,
        imageUrl: auth?.imageUrl,
        firstName: auth?.firstName,
        lastName: auth?.lastName,
      },
    });
  }),
});
