"use client";

import { useState } from "react";

import { readStreamableValue } from "ai/rsc";
import { Loader2 } from "lucide-react";

import { askQuestion } from "@/app/dashboard/(server-actions)/stream-text";
import useProject from "@/hooks/use-project";

import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Textarea } from "../ui/textarea";
import AnswerDialog from "./answer-dialog";

const AskQuestionCard = () => {
  const { project } = useProject();
  const [answer, setAnswer] = useState<string>("");
  const [open, setOpen] = useState<boolean>(false);
  const [question, setQuestion] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [files, setFiles] = useState<StreamFileOutput[]>([]);

  const onSubmit = async () => {
    setLoading(true);
    setFiles([]);
    setQuestion("");

    if (!project?.id) {
      return;
    }

    const { output, filesReference } = await askQuestion(question, project.id);
    setOpen(true);
    setFiles(filesReference);

    for await (const delta of readStreamableValue(output)) {
      if (delta) {
        setAnswer((prev) => prev + delta);
      }
    }

    setLoading(false);
  };

  return (
    <>
      <AnswerDialog
        open={open}
        files={files}
        answer={answer}
        setOpen={setOpen}
        question={question}
        projectId={project?.id ?? ""}
      />
      <Card className="relative col-span-3">
        <CardHeader>
          <CardTitle>Ask a question</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              onSubmit();
            }}
          >
            <Textarea
              placeholder="Which file should i edit to change the home page?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <div className="h-4" />
            <Button type="submit" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="animate-spin" /> Please Wait...
                </>
              ) : (
                "Ask Coeus!"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </>
  );
};

export default AskQuestionCard;
