"use client";

import Link from "next/link";

import { Loader2, Music, OctagonAlert, Trash } from "lucide-react";
import { toast } from "sonner";

import MeetingCard from "@/components/dashboard/meeting-card";
import { Button, buttonVariants } from "@/components/ui/button";
import Indicator from "@/components/ui/indicator";
import useProject from "@/hooks/use-project";
import useRefetch from "@/hooks/use-refetch";
import { cn } from "@/lib/utils";
import { api } from "@/trpc/react";

const Page = () => {
  const refetch = useRefetch();
  const { projectId } = useProject();
  const deleteMeeting = api.meeting.deleteMeeting.useMutation();
  const { data: meetings, isLoading } = api.meeting.getMeetings.useQuery(
    { projectId },
    {
      refetchInterval: 4000,
    }
  );

  return (
    <>
      <MeetingCard />
      <div className="h-6" />
      <span className="text-xl font-semibold">Meetings</span>
      <div className="h-6" />
      {meetings && meetings.length === 0 && (
        <div className="flex w-full flex-col items-center justify-center rounded-lg border bg-white p-10 shadow">
          <OctagonAlert className="mb-5 size-20 text-primary" />
          <span className="w-full text-center text-lg font-semibold text-gray-700">
            No Meetings Found!
          </span>
          <span className="w-full text-center text-sm text-gray-500">
            Start by Uploading a Meeting!
          </span>
        </div>
      )}
      {isLoading ? (
        <div className="flex w-full items-center justify-center">
          <Loader2 className="size-10 animate-spin text-primary" />
        </div>
      ) : (
        <ul className="flex flex-col items-start gap-y-5 divide-y divide-gray-200">
          {meetings?.map((meeting) => (
            <li
              key={meeting.id}
              className="flex w-full items-center justify-between rounded border bg-white p-5 shadow"
            >
              <div className="flex items-center justify-center gap-2.5">
                <div className="relative size-12 rounded-full border p-2 shadow">
                  <Music className="size-full text-primary" />
                  <Indicator
                    className="absolute left-0 top-0"
                    type={meeting.status === "PROCESSING" ? "pending" : "done"}
                  />
                </div>
                <div className="flex flex-col items-center gap-0.5">
                  <span className="w-full text-left text-xl font-semibold">
                    {meeting.name}
                  </span>
                  <span className="w-full text-left text-sm text-gray-500">
                    {meeting.createdAt.toLocaleDateString()} |&nbsp;
                    {meeting.Issue.length} issues
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-center gap-2.5">
                <Link
                  href={`/dashboard/meetings/${meeting.id}`}
                  className={cn(
                    buttonVariants({
                      variant: "outline",
                      size: "lg",
                    })
                  )}
                >
                  View Meeting
                </Link>
                <Button
                  onClick={() =>
                    deleteMeeting.mutate(
                      { meetingId: meeting.id },
                      {
                        onSuccess: () => {
                          toast.success("Successfully Deleted Meeting!");
                          refetch();
                        },
                        onError: () => {
                          toast.error(
                            "Something went wrong, Please try again!"
                          );
                        },
                      }
                    )
                  }
                  variant="destructive"
                  size="icon"
                >
                  <Trash />
                </Button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </>
  );
};

export default Page;
