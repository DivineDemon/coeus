import { Octokit } from "octokit";

import { env } from "@/env";
import { db } from "@/server/db";

import { summariseCommit } from "./gemini";

type GitResponse = {
  commitHash: string;
  commitDate: string;
  commitMessage: string;
  commitAuthorName: string;
  commitAuthorAvatar: string;
};

async function fetchProjectGithubUrl(projectId: string) {
  const project = await db.project.findUnique({
    where: {
      id: projectId,
    },
    select: {
      githubUrl: true,
    },
  });

  if (!project?.githubUrl) {
    throw new Error("Project does not have a GitHub URL");
  }

  return {
    project,
    githubUrl: project.githubUrl,
  };
}

async function filterUnprocessedCommits(
  projectId: string,
  commitHashes: GitResponse[]
) {
  const processedCommits = await db.commit.findMany({
    where: {
      projectId,
    },
  });

  const unprocessCommits = commitHashes.filter(
    (commit) =>
      !processedCommits.some(
        (processedCommit) => processedCommit.commitHash === commit.commitHash
      )
  );

  return unprocessCommits;
}

async function callSummarizer(githubUrl: string, commitHash: string) {
  const data = await fetch(`${githubUrl}/commit/${commitHash}.diff`, {
    method: "GET",
    headers: {
      Accept: "application/vnd.github.v3.diff",
    },
  });

  return (await summariseCommit(await data.text())) || "";
}

export const octokit = new Octokit({
  auth: env.GITHUB_TOKEN,
});

export const getCommitHashes = async (
  githubUrl: string
): Promise<GitResponse[]> => {
  const [owner, repo] = githubUrl.split("/").slice(-2);

  if (!owner || !repo) {
    throw new Error("Invalid GitHub URL");
  }

  const { data } = await octokit.rest.repos.listCommits({
    owner,
    repo,
  });

  const sortedCommits = data.sort(
    (a, b) =>
      new Date(`${b.commit.author?.date}`).getTime() -
      new Date(`${a.commit.author?.date}`).getTime()
  );

  return sortedCommits.slice(0, 10).map((commit) => ({
    commitHash: commit.sha as string,
    commitMessage: commit.commit.message ?? "",
    commitDate: `${commit.commit.author?.date}`,
    commitAuthorName: commit.commit.author?.name ?? "",
    commitAuthorAvatar: commit.author?.avatar_url ?? "",
  }));
};

export const pollCommits = async (projectId: string) => {
  const { githubUrl } = await fetchProjectGithubUrl(projectId);
  const commitHashes = await getCommitHashes(githubUrl);
  const unprocessedCommits = await filterUnprocessedCommits(
    projectId,
    commitHashes
  );
  const processedResponses = await Promise.allSettled(
    unprocessedCommits.map((commit) => {
      return callSummarizer(githubUrl, commit.commitHash);
    })
  );
  const summaries = processedResponses.map((response) => {
    if (response.status === "fulfilled") {
      return response.value as string;
    }

    return "";
  });

  const createCommits = await db.commit.createMany({
    data: summaries.map((summary, idx) => {
      return {
        projectId,
        commitHash: unprocessedCommits[idx]!.commitHash,
        commitMessage: unprocessedCommits[idx]!.commitMessage,
        commitAuthorName: unprocessedCommits[idx]!.commitAuthorName,
        commitAuthorAvatar: unprocessedCommits[idx]!.commitAuthorAvatar,
        commitDate: unprocessedCommits[idx]!.commitDate,
        summary,
      };
    }),
  });

  return createCommits;
};
