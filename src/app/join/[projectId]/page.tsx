import { redirect } from "next/navigation";

import { auth, clerkClient } from "@clerk/nextjs/server";

import Heading from "@/components/heading";
import LoadingSpinner from "@/components/loading-spinner";
import BackgroundPattern from "@/components/ui/background-pattern";
import { api } from "@/trpc/server";

interface PageProps {
  params: Promise<{ projectId: string }>;
}

const Page = async (props: PageProps) => {
  const { userId } = await auth();
  const { projectId } = await props.params;

  if (!userId) {
    return redirect("/sign-in");
  }

  const dbUser = await api.user.getUser({ id: userId });

  const client = await clerkClient();
  const user = await client.users.getUser(userId!);

  if (!dbUser) {
    await api.user.syncUser({
      id: userId,
      lastName: user.lastName ?? "",
      imageUrl: user.imageUrl ?? "",
      firstName: user.firstName ?? "",
      email: user.emailAddresses[0]?.emailAddress ?? "",
    });
  }

  const project = await api.project.getProject({ projectId });

  if (!project) {
    return redirect("/dashboard");
  }

  const response = await api.user.linkToProject({
    userId,
    projectId,
  });

  if (response) {
    return redirect("/dashboard");
  }

  return (
    <div className="flex w-full flex-1 items-center justify-center p-4">
      <BackgroundPattern className="absolute inset-0 left-1/2 z-0 -translate-x-1/2 opacity-75" />
      <div className="relative z-10 flex -translate-y-1/2 flex-col items-center gap-6 text-center">
        <LoadingSpinner />
        <Heading className="text-primary">Adding you to the Project...</Heading>
        <p className="max-w-prose text-base/7 text-gray-600">
          Just a moment while we set things up for you.
        </p>
      </div>
    </div>
  );
};

export default Page;
