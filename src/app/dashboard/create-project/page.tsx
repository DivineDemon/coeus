"use client";

import Image from "next/image";

import { ArrowRight, Info, Loader2 } from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import CreateImage from "@/assets/img/create-img.svg";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import useRefetch from "@/hooks/use-refetch";
import { api } from "@/trpc/react";

type FormSchema = {
  repoUrl: string;
  projectName: string;
  githubToken?: string;
};

const Page = () => {
  const refetch = useRefetch();
  const checkCredits = api.user.seeCredits.useMutation();
  const createProject = api.project.createProject.useMutation();
  const { register, handleSubmit, reset } = useForm<FormSchema>();

  const onSubmit = async (data: FormSchema) => {
    if (!!checkCredits.data) {
      createProject.mutate(
        {
          name: data.projectName,
          githubUrl: data.repoUrl,
          githubToken: data.githubToken,
        },
        {
          onSuccess: () => {
            toast.success("Project created successfully!");
            refetch();
            reset();
          },
          onError: () => {
            toast.error(
              "Please verify if your repository is public. If it is private or it belongs to an organization, please provide a valid GitHub token."
            );
          },
        }
      );
    } else {
      checkCredits.mutate(
        {
          githubUrl: data.repoUrl,
          githubToken: data.githubToken,
        },
        {
          onError: () => {
            toast.error("Not enough credits!");
          },
        }
      );
    }
  };

  const hasEnoughCredits = checkCredits?.data?.userCredits
    ? checkCredits.data.fileCount <= checkCredits.data.userCredits
    : true;

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
          {!!checkCredits.data && (
            <div className="mt-4 rounded-md border border-orange-200 bg-orange-50 px-4 py-2 text-orange-700">
              <div className="flex items-center gap-2">
                <Info className="size-4" />
                <p className="text-sm">
                  You will be charged&nbsp;
                  <strong>{checkCredits.data?.fileCount}</strong>&nbsp;credits.
                </p>
              </div>
              <p className="ml-6 text-sm text-blue-600">
                You have <strong>{checkCredits.data?.userCredits}</strong>
                &nbsp;credits remaining.
              </p>
            </div>
          )}
          <div className="h-4" />
          <Button
            disabled={
              createProject.isPending ||
              checkCredits.isPending ||
              !hasEnoughCredits
            }
            type="submit"
            variant="default"
            size="sm"
          >
            {createProject.isPending ? (
              <>
                <Loader2 className="animate-spin" /> Please Wait...
              </>
            ) : checkCredits.isPending ? (
              <>
                <Loader2 className="animate-spin" /> Checking...
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
