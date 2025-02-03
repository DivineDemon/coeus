import { redirect } from "next/navigation";

import { getKindeServerSession } from "@kinde-oss/kinde-auth-nextjs/server";

import Heading from "@/components/heading";
import LoadingSpinner from "@/components/loading-spinner";
import BackgroundPattern from "@/components/ui/background-pattern";
import { api } from "@/trpc/server";

interface PageProps {
  params: Promise<{ projectId: string }>;
}

const Page = async (props: PageProps) => {
  const { getUser } = getKindeServerSession();
  const { projectId } = await props.params;
  const user = await getUser();

  if (!user) {
    return redirect("/sign-in");
  }

  const dbUser = await api.user.getUser({ id: user.id });

  if (!dbUser) {
    await api.user.syncUser({
      id: user.id,
      lastName: user.family_name ?? "",
      imageUrl: user.picture ?? "",
      firstName: user.family_name ?? "",
      email: user.email ?? "",
    });
  }

  const project = await api.project.getProject({ projectId });

  if (!project) {
    return redirect("/dashboard");
  }

  const response = await api.user.linkToProject({
    userId: user.id,
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
