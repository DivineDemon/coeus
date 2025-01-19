"use client";

import { useState } from "react";

import { Button } from "../ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";

interface IssueCardProps {
  issue: {
    meetingId: string;
    id: string;
    createdAt: Date;
    updatedAt: Date;
    summary: string;
    start: string;
    end: string;
    gist: string;
    headline: string;
  };
}

const IssueCard = ({ issue }: IssueCardProps) => {
  const [open, setOpen] = useState<boolean>(false);

  return (
    <>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{issue.gist}</DialogTitle>
            <DialogDescription>
              {issue.createdAt.toLocaleDateString()}
            </DialogDescription>
            <p className="text-gray-600">{issue.headline}</p>
            <blockquote className="mt-2 border-l-4 border-gray-300 bg-gray-50 p-4">
              <span className="text-sm text-gray-600">
                {issue.start}&nbsp;-&nbsp;{issue.end}
              </span>
              <p className="font-medium italic leading-relaxed text-gray-900">
                {issue.summary}
              </p>
            </blockquote>
          </DialogHeader>
        </DialogContent>
      </Dialog>
      <Card className="relative">
        <CardHeader>
          <CardTitle className="text-xl">
            {issue.gist}
            <div className="my-2 border-b" />
            <CardDescription>{issue.headline}</CardDescription>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Button type="button" onClick={() => setOpen(!open)}>
            Details
          </Button>
        </CardContent>
      </Card>
    </>
  );
};

export default IssueCard;
