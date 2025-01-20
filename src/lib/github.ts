import { Octokit } from "octokit";

import { env } from "@/env";
import { db } from "@/server/db";

import { summariseCommit } from "./openai";

type GitResponse = {
  commitHash: string;
  commitDate: string;
  commitMessage: string;
  commitAuthorName: string;
  commitAuthorAvatar: string;
};

async function getFileCount(
  path: string,
  octokit: Octokit,
  githubOwner: string,
  githubRepo: string,
  acc: number = 0
) {
  const { data } = await octokit.rest.repos.getContent({
    owner: githubOwner,
    repo: githubRepo,
    path,
  });

  if (!Array.isArray(data) && data.type === "file") {
    return acc + 1;
  }

  if (Array.isArray(data)) {
    let fileCount = 0;
    const directories: string[] = [];

    for (const item of data) {
      if (item.type === "dir") {
        directories.push(item.path);
      } else {
        fileCount++;
      }
    }

    if (directories.length > 0) {
      const directoryCounts = await Promise.all(
        directories.map((dirPath) =>
          getFileCount(dirPath, octokit, githubOwner, githubRepo, 0)
        )
      );

      fileCount += directoryCounts.reduce((acc, count) => acc! + count!, 0)!;
    }
    return acc + fileCount;
  }

  return acc;
}

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

export const checkCredits = async (githubUrl: string, githubToken?: string) => {
  const octokit = new Octokit({ auth: githubToken });
  const githubOwner = githubUrl.split("/")[3];
  const githubRepo = githubUrl.split("/")[4];

  if (!githubOwner || !githubRepo) {
    return 0;
  }

  const fileCount = await getFileCount("", octokit, githubOwner, githubRepo, 0);
  return fileCount;
};
