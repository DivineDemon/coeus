"use client";

import type { Dispatch, SetStateAction } from "react";

import MDEditor from "@uiw/react-md-editor";
import { Waypoints } from "lucide-react";

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import CodeReferences from "./code-references";

interface AnswerDialogProps {
  open: boolean;
  answer: string;
  files: StreamFileOutput[];
  setOpen: Dispatch<SetStateAction<boolean>>;
}

const AnswerDialog = ({ open, answer, files, setOpen }: AnswerDialogProps) => {
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-fit">
        <DialogHeader>
          <DialogTitle>
            <Waypoints className="size-8 text-primary" />
          </DialogTitle>
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
