"use client";

import { Video } from "lucide-react";

import { api } from "@/trpc/react";

import IssueCard from "./issue-card";

interface IssuesListProps {
  meetingId: string;
}

const IssuesList = ({ meetingId }: IssuesListProps) => {
  const { data: meeting, isLoading } = api.meeting.getMeeting.useQuery(
    {
      meetingId,
    },
    { refetchInterval: 4000 }
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!meeting) {
    return <div>Meeting not found</div>;
  }

  return (
    <div className="p-8">
      <div className="mx-auto flex max-w-2xl items-center justify-between gap-x-8 border-b pb-6 lg:mx-0 lg:max-w-none">
        <div className="flex items-center gap-x-6">
          <div className="rounded-full border bg-white p-3">
            <Video />
          </div>
          <div className="flex flex-col items-center gap-1">
            <span className="w-full text-left text-sm leading-6 text-gray-600">
              Meeting on&nbsp;{meeting.createdAt.toLocaleDateString()}
            </span>
            <span className="text-base font-semibold leading-6 text-gray-900">
              {meeting.name}
            </span>
          </div>
        </div>
      </div>
      <div className="h-4" />
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        {meeting.Issue.map((issue) => (
          <IssueCard key={issue.id} issue={issue} />
        ))}
      </div>
    </div>
  );
};

export default IssuesList;
