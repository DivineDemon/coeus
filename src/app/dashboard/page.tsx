"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";

import { Archive, Clipboard, ExternalLink, Github } from "lucide-react";
import { toast } from "sonner";

import AskQuestionCard from "@/components/dashboard/ask-question-card";
import CommitLog from "@/components/dashboard/commit-log";
import MeetingCard from "@/components/dashboard/meeting-card";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import WarningModal from "@/components/warning-modal";
import useProject from "@/hooks/use-project";
import useRefetch from "@/hooks/use-refetch";
import { api } from "@/trpc/react";

const Page = () => {
  const refetch = useRefetch();
  const { project } = useProject();
  const [warn, setWarn] = useState<boolean>(false);
  const [invite, setInvite] = useState<boolean>(false);
  const archiveProject = api.project.archiveProject.useMutation();
  const { data: members } = api.project.getTeamMembers.useQuery({
    projectId: project?.id!,
  });

  return (
    <>
      <Dialog open={invite} onOpenChange={setInvite}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Invite Members</DialogTitle>
            <DialogDescription>
              Ask them to copy and paste this link.
            </DialogDescription>
          </DialogHeader>
          <div className="flex w-full items-center justify-center gap-2.5 rounded-lg bg-gray-100 px-2.5 py-1.5">
            <span className="flex-1 text-left text-sm font-medium">
              {window.location.origin}/join/{project?.id}
            </span>
            <Button
              onClick={() => {
                navigator.clipboard.writeText(
                  `${window.location.origin}/join/${project?.id}`
                );
                toast.success("Copied to Clipboard!");
              }}
              type="button"
              variant="default"
              size="icon"
            >
              <Clipboard />
            </Button>
          </div>
        </DialogContent>
      </Dialog>
      <WarningModal
        open={warn}
        setOpen={setWarn}
        loading={archiveProject.isPending}
        message={`archive ${project?.name}`}
        cta={() =>
          archiveProject.mutate(
            { projectId: project!.id },
            {
              onSuccess: () => {
                toast.success("Project Archived Successfully!");
                setWarn(false);
                refetch();
              },
              onError: () => {
                toast.error("Failed to archive project!");
              },
            }
          )
        }
      />
      <div className="flex flex-wrap items-center justify-between gap-y-4">
        <div className="w-fit rounded-md bg-primary px-4 py-3">
          <div className="flex items-center">
            <Github className="size-5 text-white" />
            <div className="ml-2">
              <p className="text-sm font-medium text-white">
                This project is linked to&nbsp;
                <Link
                  href={project?.githubUrl ?? ""}
                  className="inline-flex items-center text-white/80 hover:underline"
                >
                  {project?.githubUrl}
                  <ExternalLink className="ml-1 size-4" />
                </Link>
              </p>
            </div>
          </div>
        </div>
        <div className="h-4" />
        <div className="flex items-center gap-4">
          <div className="flex items-center -space-x-2">
            {members?.map((member) => (
              <Image
                key={member.id}
                src={`${member.user.imageUrl}`}
                alt="team-member-image"
                width={30}
                height={30}
                className="rounded-full border-2 border-gray-200"
              />
            ))}
          </div>
          <Button
            onClick={() => setInvite(true)}
            type="button"
            className="h-[44px]"
          >
            Invite Members
          </Button>
          <Button
            type="button"
            onClick={() => setWarn(true)}
            variant="destructive"
            className="h-[44px]"
          >
            <Archive />
          </Button>
        </div>
      </div>
      <div className="mt-4">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-5">
          <AskQuestionCard />
          <MeetingCard />
        </div>
      </div>
      <div className="mt-8">
        <CommitLog />
      </div>
    </>
  );
};

export default Page;
