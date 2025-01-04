"use client";

import Image from "next/image";

import { ArrowRight, Loader2 } from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import CreateImage from "@/assets/img/create-img.svg";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/trpc/react";

type FormSchema = {
  repoUrl: string;
  projectName: string;
  githubToken?: string;
};

const Page = () => {
  const createProject = api.project.createProject.useMutation();
  const { register, handleSubmit, reset } = useForm<FormSchema>();

  const onSubmit = async (data: FormSchema) => {
    createProject.mutate(
      {
        name: data.projectName,
        githubUrl: data.repoUrl,
        githubToken: data.githubToken,
      },
      {
        onSuccess: () => {
          toast.success("Project created successfully!");
          reset();
        },
        onError: (error) => {
          toast.error(error.message);
        },
      }
    );
  };

  return (
    <div className="flex h-full items-center justify-center gap-12">
      <Image src={CreateImage} alt="create-image" className="h-56 w-auto" />
      <div className="flex flex-col">
        <span className="text-2xl font-semibold">
          Link your GitHub Repository
        </span>
        <span className="text-sm text-muted-foreground">
          Enter the URL of your repository to link it to Coeus.
        </span>
        <div className="h-4" />
        <form onSubmit={handleSubmit(onSubmit)}>
          <Input
            {...register("projectName", { required: true })}
            placeholder="Project Name"
            required={true}
            type="text"
          />
          <div className="h-2" />
          <Input
            type="url"
            required={true}
            placeholder="Github Repository URL"
            {...register("repoUrl", { required: true })}
          />
          <div className="h-2" />
          <Input
            {...register("githubToken")}
            placeholder="Github Token (Optional)"
            type="text"
          />
          <div className="h-4" />
          <Button
            disabled={createProject.isPending}
            type="submit"
            variant="default"
            size="sm"
          >
            {createProject.isPending ? (
              <>
                <Loader2 className="animate-spin" /> Please Wait...
              </>
            ) : (
              <>
                Create Project <ArrowRight />
              </>
            )}
          </Button>
        </form>
      </div>
    </div>
  );
};

export default Page;
