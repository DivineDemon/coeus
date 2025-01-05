"use client";

import { useState } from "react";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { lucario } from "react-syntax-highlighter/dist/esm/styles/prism";

import { cn } from "@/lib/utils";

import { Tabs, TabsContent } from "../ui/tabs";

type CodeReferencesProps = {
  fileReferences: StreamFileOutput[];
};

const CodeReferences = ({ fileReferences }: CodeReferencesProps) => {
  const [tab, setTab] = useState(fileReferences[0]?.fileName);

  if (!fileReferences.length) {
    return null;
  }

  return (
    <div className="max-w-[70vw]">
      <Tabs value={tab} onValueChange={setTab}>
        <div className="flex gap-2 overflow-scroll rounded-md bg-gray-200 p-1">
          {fileReferences.map((file, idx) => (
            <button
              key={idx}
              onClick={() => setTab(file.fileName)}
              className={cn(
                "whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted",
                {
                  "bg-primary text-primary-foreground hover:bg-[rgba(37,99,235,0.8)]":
                    tab === file.fileName,
                }
              )}
              type="button"
            >
              {file.fileName}
            </button>
          ))}
        </div>
        {fileReferences.map((file, idx) => (
          <TabsContent
            key={idx}
            value={file.fileName}
            className="max-h-[40vh] max-w-full overflow-scroll rounded-md"
          >
            <SyntaxHighlighter language="typescript" style={lucario}>
              {file.sourceCode}
            </SyntaxHighlighter>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
};

export default CodeReferences;
