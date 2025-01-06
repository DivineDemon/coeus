"use client";

import type { Dispatch, SetStateAction } from "react";

import MDEditor from "@uiw/react-md-editor";
import { Waypoints } from "lucide-react";
import { toast } from "sonner";

import { api } from "@/trpc/react";

import { Button } from "../ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import CodeReferences from "./code-references";

interface AnswerDialogProps {
  open: boolean;
  answer: string;
  question: string;
  projectId: string;
  files: StreamFileOutput[];
  setOpen: Dispatch<SetStateAction<boolean>>;
}

const AnswerDialog = ({
  open,
  files,
  answer,
  setOpen,
  question,
  projectId,
}: AnswerDialogProps) => {
  const saveAnswer = api.question.saveAnswer.useMutation();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-fit">
        <DialogHeader>
          <div className="flex items-center gap-2">
            <DialogTitle>
              <Waypoints className="size-8 text-primary" />
            </DialogTitle>
            <Button
              type="button"
              variant="outline"
              disabled={saveAnswer.isPending}
              onClick={() => {
                saveAnswer.mutate(
                  {
                    projectId,
                    question,
                    answer,
                    filesReference: files,
                  },
                  {
                    onSuccess: () => {
                      toast.success("Answer Saved!");
                    },
                    onError: () => {
                      toast.error("Failed to Save Answer!");
                    },
                  }
                );
              }}
            >
              Save Answer
            </Button>
          </div>
        </DialogHeader>
        <MDEditor.Markdown
          source={answer}
          className="!h-full max-h-[40vh] max-w-[70vw] overflow-scroll rounded-md p-3"
        />
        <CodeReferences fileReferences={files} />
      </DialogContent>
    </Dialog>
  );
};

export default AnswerDialog;
