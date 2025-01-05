"use server";

import { createOpenAI } from "@ai-sdk/openai";
import { streamText } from "ai";
import { createStreamableValue } from "ai/rsc";

import { env } from "@/env";
import { getEmbeddings } from "@/lib/openai";
import { db } from "@/server/db";

const openAI = createOpenAI({
  apiKey: env.OPENAI_KEY,
});

export async function askQuestion(question: string, projectId: string) {
  const stream = createStreamableValue();
  const queryVector = await getEmbeddings(question);
  const vectorQuery = `[${queryVector?.join(",")}]`;

  const result = (await db.$queryRaw`
    SELECT "fileName", "sourceCode", "summary",
    1 - ("summaryEmbedding" <=> ${vectorQuery}::vector) AS similarity
    FROM "SourceCodeEmbedding"
    WHERE 1 - ("summaryEmbedding" <=> ${vectorQuery}::vector) > .5
    AND "projectId" = ${projectId}
    ORDER BY similarity DESC
    LIMIT 10
  `) as {
    summary: string;
    fileName: string;
    sourceCode: string;
  }[];

  let context = "";

  for (const doc of result) {
    context += `source: ${doc.fileName}\ncode content: ${doc.sourceCode}\nsummary: ${doc.summary}\n\n`;
  }

  (async () => {
    const { textStream } = await streamText({
      model: openAI("chatgpt-4o-latest"),
      prompt: `You are an AI code assistant who answers questions about the codebase. Your target audience is a technical intern who is looking to understand the codebase.
      AI assistant is a brand new, powerful, human-like artificial intelligence.
      The traits of AI include expert knowledge, helpfulness, cleverness and articulateness.
      AI is a well-behaved and well-mannered individual.
      AI is always friendly, kind and inspiring, and he is eager to provide vivid and thoughtful responses to the user.
      AI has the sum of all knowledge in their brain, and is able to accurately answer nearly any question about any topic in conversation.
      If the question is asking about code or a specific file, AI will provide the detailed answer, giving step by step instructions, including code snippets.
      START CONTEXT BLOCK
      ${context}
      END CONTEXT BLOCK

      START QUESTION
      ${question}
      END QUESTION.
      AI assistant will take into account any CONTEXT BLOCK that is provided in a conversation. If the context does not provide the answer to question, the AI assistant will say, 'I'm sorry, but I don't know the answer to your question.'. AI will not apologize for previous response but will instead indicate that new information was gained. AI assistant will not invent anything that is not drawn directly from that context. Answer in markdown syntax, with code snippets if needed. Be as detailed as possible when answering, make sure there is no mistake in your response.`,
    });

    for await (const delta of textStream) {
      stream.update(delta);
    }

    stream.done();
  })();

  return {
    output: stream.value,
    filesReference: result,
  };
}
