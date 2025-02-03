"use client";

import Image from "next/image";
import { Fragment, useState } from "react";

import MDEditor from "@uiw/react-md-editor";
import { OctagonAlert } from "lucide-react";

import AskQuestionCard from "@/components/dashboard/ask-question-card";
import CodeReferences from "@/components/dashboard/code-references";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import useProject from "@/hooks/use-project";
import { api } from "@/trpc/react";

const Page = () => {
  const { projectId } = useProject();
  const [questionIndex, setQuestionIndex] = useState<number>(0);
  const { data: questions } = api.question.getQuestions.useQuery({ projectId });

  return (
    <Sheet>
      <AskQuestionCard />
      <div className="h-4" />
      <h1 className="text-xl font-semibold">Saved Questions</h1>
      <div className="h-2" />
      <div className="flex flex-col gap-2">
        {questions && questions.length === 0 && (
          <div className="flex w-full flex-col items-center justify-center rounded-lg border bg-white p-10 shadow">
            <OctagonAlert className="mb-5 size-20 text-primary" />
            <span className="w-full text-center text-lg font-semibold text-gray-700">
              No Questions Found!
            </span>
            <span className="w-full text-center text-sm text-gray-500">
              Start by Asking a Question!
            </span>
          </div>
        )}
        {questions?.map((question, idx) => {
          return (
            <Fragment key={question.id}>
              <SheetTrigger onClick={() => setQuestionIndex(idx + 1)}>
                <div className="flex items-center gap-4 rounded-lg border bg-white p-4 shadow">
                  <Image
                    src={question.user.imageUrl ?? ""}
                    className="rounded-full"
                    width={30}
                    height={30}
                    alt="user-dp"
                  />
                  <div className="flex flex-col text-left">
                    <div className="flex items-center gap-2">
                      <p className="line-clamp-1 text-lg font-medium text-gray-700">
                        {question.question}
                      </p>
                      <span className="whitespace-nowrap text-xs text-gray-400">
                        {question.createdAt.toLocaleDateString()}
                      </span>
                    </div>
                    <p className="line-clamp-1 text-gray-400">
                      {question.answer}
                    </p>
                  </div>
                </div>
              </SheetTrigger>
            </Fragment>
          );
        })}
      </div>
      {questionIndex !== 0 && (
        <SheetContent className="sm:max-w-[70vw]">
          <SheetHeader>
            <SheetTitle>{questions?.[questionIndex - 1]?.question}</SheetTitle>
            <MDEditor.Markdown
              source={questions?.[questionIndex - 1]?.answer}
              className="max-h-[45vh] overflow-scroll rounded-lg p-3"
            />
            <CodeReferences
              fileReferences={
                questions?.[questionIndex - 1]?.fileReferences ?? ([] as any)
              }
            />
          </SheetHeader>
        </SheetContent>
      )}
    </Sheet>
  );
};

export default Page;
