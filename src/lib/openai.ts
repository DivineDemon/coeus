import { type Document } from "@langchain/core/documents";
import OpenAI from "openai";

import { env } from "@/env";

const genAI = new OpenAI({
  apiKey: env.OPENAI_KEY,
});

export const summariseCommit = async (diff: string) => {
  const response = await genAI.chat.completions.create({
    model: "gpt-4-turbo",
    messages: [
      {
        role: "system",
        content:
          "You are an expert programmer specializing in summarizing git diffs.",
      },
      {
        role: "user",
        content: `You are an expert programmer, and you are trying to summarize a git diff.
        Reminders about the git diff format:
        For every file, there are a few metadata lines like (for example):
        \`\`\`
        diff --git a/lib/index.js b/lib/index.js
        index aadf691..bfef803 100644
        --- a/lib/index.js
        +++ b/lib/index.js
        \`\`\`
        This means that \`lib/index.js\` was modified in this commit. 
        A line starting with \`+\` means it was added. \`-\` means it was deleted.
        EXAMPLE SUMMARY COMMENTS:
        * Raised the amount of returned recordings from \`10\` to \`100\` [packages/server/recordings_api.ts]
        * Fixed a typo in the GitHub action name [.github/workflows/gpt-commit-summarizer.yml]
        * Added an OpenAI API for completions [packages/utils/apis/openai.ts]
        Please summarize the following diff file: \n\n${diff}`,
      },
    ],
    max_tokens: 500,
  });

  return response.choices[0]?.message.content;
};

export const summariseCode = async (doc: Document) => {
  const code = doc.pageContent.slice(0, 10000);
  try {
    const response = await genAI.chat.completions.create({
      model: "gpt-4-turbo",
      messages: [
        {
          role: "system",
          content:
            "You are an intelligent senior software engineer specializing in explaining code to junior developers.",
        },
        {
          role: "user",
          content: `You are onboarding a junior software engineer and explaining to them the purpose of the ${doc.metadata.source} file.
          Here is the code:
          ---
          ${code}
          ---
          Give a summary of the code above in no more than 100 words.`,
        },
      ],
      max_tokens: 300,
    });

    return response.choices[0]?.message.content;
  } catch (error) {
    console.error((error as Error).message);
    return "";
  }
};

export const getEmbeddings = async (summary: string) => {
  const response = await genAI.embeddings.create({
    model: "text-embedding-ada-002",
    input: summary,
  });

  return response.data[0]?.embedding;
};
