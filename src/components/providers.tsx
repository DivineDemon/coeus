import { type ReactNode } from "react";

import { ClerkProvider } from "@clerk/nextjs";

import { TRPCReactProvider } from "@/trpc/react";

const Providers = ({ children }: { children: ReactNode }) => {
  return (
    <ClerkProvider>
      <TRPCReactProvider>{children}</TRPCReactProvider>
    </ClerkProvider>
  );
};

export default Providers;
