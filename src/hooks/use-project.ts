import { useLocalStorage } from "usehooks-ts";

import { api } from "@/trpc/react";

const useProject = () => {
  const { data: projects } = api.project.getProjects.useQuery();
  const [projectId, setProjectId] = useLocalStorage("projectId", "");
  const project = projects?.find((project) => project.id === projectId);

  return {
    project,
    projects,
    projectId,
    setProjectId,
  };
};

export default useProject;
