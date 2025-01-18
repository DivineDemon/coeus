"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { useMutation } from "@tanstack/react-query";
import { Presentation, Upload } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { toast } from "sonner";

import useProject from "@/hooks/use-project";
import { uploadFile } from "@/lib/firebase";
import { cn } from "@/lib/utils";
import { api } from "@/trpc/react";

import { Button } from "../ui/button";
import { Card } from "../ui/card";

const MeetingCard = () => {
  const router = useRouter();
  const { projectId } = useProject();
  const processMeeting = useMutation({
    mutationFn: async (data: { meetingUrl: string; meetingId: string }) => {
      const response = await fetch("/api/process-meeting", {
        method: "POST",
        body: JSON.stringify({
          meetingId: data.meetingId,
          meetingUrl: data.meetingUrl,
        }),
      });

      return await response.json();
    },
  });
  const [progress, setProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const uploadMeeting = api.meeting.uploadMeeting.useMutation();

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "audio/*": [".mp3", ".wav", ".m4a"],
    },
    multiple: false,
    maxSize: 50_000_000,
    onDrop: async (acceptedFiles) => {
      if (!projectId) {
        return;
      }

      setIsUploading(true);

      const file = acceptedFiles[0];

      if (!file) {
        return;
      }

      const downloadUrl = await uploadFile(file as File, setProgress);
      uploadMeeting.mutate(
        {
          projectId,
          meetingUrl: downloadUrl as string,
          name: file.name,
        },
        {
          onSuccess: (meeting) => {
            toast.success("Meeting Uploaded Successfully!");
            router.push("/dashboard/meetings");
            processMeeting.mutateAsync({
              meetingId: meeting.id,
              meetingUrl: downloadUrl as string,
            });
          },
          onError: () => {
            toast.error("Something went wrong, Please try again!");
          },
        }
      );

      setIsUploading(false);
    },
  });

  return (
    <Card
      className="col-span-2 flex flex-col items-center justify-center p-10"
      {...getRootProps()}
    >
      {!isUploading ? (
        <>
          <Presentation className="size-10 animate-bounce" />
          <span className="mt-2 text-sm font-semibold text-gray-900">
            Create a new meeting
          </span>
          <span className="mt-1 text-center text-sm text-gray-500">
            Analyse your meeting with Coeus.
            <br />
            Powered by AI.
          </span>
          <div className="mt-6">
            <Button type="button" disabled={isUploading}>
              <Upload className="-ml-0.5 mr-1.5 size-5" aria-hidden={true} />
              Upload Meeting
              <input className="hidden" {...getInputProps()} />
            </Button>
          </div>
        </>
      ) : (
        <div className="flex w-full flex-col items-center justify-center gap-2">
          <div className="h-3 w-full rounded-full bg-gray-100">
            <div
              className={cn("h-3 rounded-full bg-primary", `w-[${progress}%]`)}
            />
          </div>
          <span className="text-center text-sm text-gray-500">
            Uploading your Meeting...
          </span>
        </div>
      )}
    </Card>
  );
};

export default MeetingCard;
