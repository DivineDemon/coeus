"use client";

import { useUser } from "@clerk/nextjs";

const Page = () => {
  const { user } = useUser();

  return <div>Page</div>;
};

export default Page;
