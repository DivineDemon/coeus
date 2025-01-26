"use client";

import Image from "next/image";

import * as Clerk from "@clerk/elements/common";
import * as SignIn from "@clerk/elements/sign-in";
import { Waypoints } from "lucide-react";

import GithubIcon from "@/assets/img/github.svg";
import GoogleIcon from "@/assets/img/google.svg";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const Page = () => {
  return (
    <div className="grid w-full flex-grow items-center bg-white px-4 sm:justify-center">
      <SignIn.Root>
        <SignIn.Step
          name="start"
          className="w-full space-y-6 rounded-2xl px-4 py-10 sm:w-96 sm:px-8"
        >
          <header className="flex flex-col items-center text-center">
            <Waypoints className="size-10 text-primary" />
            <h1 className="mt-4 text-xl font-medium tracking-tight text-neutral-950">
              Sign in to&nbsp;<span className="text-primary">Coeus</span>
            </h1>
          </header>
          <Clerk.GlobalError className="block text-sm text-red-600" />
          <Clerk.Field name="identifier">
            <Clerk.Label className="sr-only">Email</Clerk.Label>
            <Clerk.Input
              type="email"
              required
              placeholder="Email"
              className="w-full border-b border-neutral-200 bg-white pb-2 text-sm/6 text-neutral-950 outline-none placeholder:text-neutral-400 hover:border-neutral-300 focus:border-neutral-600 data-[invalid]:border-red-600 data-[invalid]:text-red-600"
            />
            <Clerk.FieldError className="mt-2 block text-xs text-red-600" />
          </Clerk.Field>
          <Clerk.Field name="password" className="space-y-2">
            <Clerk.Label className="sr-only">Password</Clerk.Label>
            <Clerk.Input
              type="password"
              required
              placeholder="Password"
              className="w-full border-b border-neutral-200 bg-white pb-2 text-sm/6 text-neutral-950 outline-none placeholder:text-neutral-400 hover:border-neutral-300 focus:border-neutral-600 data-[invalid]:border-red-600 data-[invalid]:text-red-600"
            />
            <Clerk.FieldError className="mt-2 block text-xs text-red-600" />
          </Clerk.Field>
          <SignIn.Action
            submit
            className={cn(
              "w-full",
              buttonVariants({
                variant: "default",
              })
            )}
          >
            Sign In
          </SignIn.Action>
          <div className="rounded-xl bg-neutral-100 p-5">
            <p className="mb-4 text-center text-sm/5 text-neutral-500">
              Alternatively, sign in with these platforms
            </p>
            <div className="space-y-2">
              <Clerk.Connection
                name="google"
                className="flex w-full items-center justify-center gap-x-3 rounded-md bg-gradient-to-b from-white to-neutral-50 px-2 py-1.5 text-sm font-medium text-neutral-950 shadow outline-none ring-1 ring-black/5 hover:to-neutral-100 focus-visible:outline-offset-2 focus-visible:outline-neutral-600 active:text-neutral-950/60"
              >
                <Image src={GoogleIcon} alt="google-icon" className="size-5" />
                Login with Google
              </Clerk.Connection>
              <Clerk.Connection
                name="github"
                className="flex w-full items-center justify-center gap-x-3 rounded-md bg-gradient-to-b from-white to-neutral-50 px-2 py-1.5 text-sm font-medium text-neutral-950 shadow outline-none ring-1 ring-black/5 hover:to-neutral-100 focus-visible:outline-offset-2 focus-visible:outline-neutral-600 active:text-neutral-950/60"
              >
                <Image src={GithubIcon} alt="github-icon" className="size-5" />
                Login with Github
              </Clerk.Connection>
            </div>
          </div>
          <p className="text-center text-sm text-neutral-500">
            Don&apos;t have an account?&nbsp;
            <Clerk.Link
              navigate="sign-up"
              className="rounded px-1 py-0.5 text-neutral-700 outline-none hover:bg-neutral-100 focus-visible:bg-neutral-100"
            >
              Sign up
            </Clerk.Link>
          </p>
        </SignIn.Step>
      </SignIn.Root>
    </div>
  );
};

export default Page;
