import { GithubRepoLoader } from "@langchain/community/document_loaders/web/github";
import { type Document } from "@langchain/core/documents";

import { db } from "@/server/db";

import { getEmbeddings, summariseCode } from "./openai";

const generateEmbeddings = async (docs: Document[]) => {
  return await Promise.all(
    docs.map(async (doc) => {
      const summary = await summariseCode(doc);
      const embedding = await getEmbeddings(summary!);

      return {
        summary,
        embedding,
        fileName: doc.metadata.source,
        sourceCode: JSON.parse(JSON.stringify(doc.pageContent)),
      };
    })
  );
};

export const loadGithubRepo = async (
  githubUrl: string,
  githubToken: string
) => {
  const loader = new GithubRepoLoader(githubUrl, {
    accessToken: githubToken,
    branch: "main",
    ignoreFiles: [
      "package-lock.json",
      "yarn.lock",
      "pnpm-lock.yaml",
      "bun.lockb",
    ],
    recursive: true,
    unknown: "warn",
    maxConcurrency: 5,
  });

  const docs = await loader.load();

  return docs;
};

export const indexGithubRepo = async (
  projectId: string,
  githubUrl: string,
  githubToken: string
) => {
  const docs = await loadGithubRepo(githubUrl, githubToken);
  const allEmbeddings = await generateEmbeddings(docs);

  await Promise.allSettled(
    allEmbeddings.map(async (embedding) => {
      if (!embedding) {
        return;
      }

      const sourceCodeEmbedding = await db.sourceCodeEmbedding.create({
        data: {
          projectId,
          summary: embedding.summary!,
          fileName: embedding.fileName,
          sourceCode: embedding.sourceCode,
        },
      });

      await db.$executeRaw`
        UPDATE "SourceCodeEmbedding"
        SET "summaryEmbedding" = ${embedding.embedding}::vector
        WHERE "id" = ${sourceCodeEmbedding.id}
      `;
    })
  );
};
