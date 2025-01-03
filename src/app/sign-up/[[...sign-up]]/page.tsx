import { SignUp } from "@clerk/nextjs";

const Page = () => {
  return (
    <div className="flex h-screen w-full items-center justify-center">
      <SignUp />
    </div>
  );
};

export default Page;
