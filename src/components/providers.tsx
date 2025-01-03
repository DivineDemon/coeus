import { type ReactNode } from "react";

import { TRPCReactProvider } from "@/trpc/react";

const Providers = ({ children }: { children: ReactNode }) => {
  return <TRPCReactProvider>{children}</TRPCReactProvider>;
};

export default Providers;
