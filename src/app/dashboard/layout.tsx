import { PropsWithChildren } from "react";

import { UserButton } from "@clerk/nextjs";

import AppSidebar from "@/components/dashboard/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";

const Layout = ({ children }: PropsWithChildren) => {
  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="m-2 w-full">
        <div className="flex items-center gap-2 rounded-md border border-sidebar-border bg-sidebar px-4 py-2 shadow">
          {/* <SearchBar /> */}
          <div className="ml-auto"></div>
          <UserButton />
        </div>
        <div className="h-4" />
        <div className="h-[calc(100vh-78px)] overflow-y-auto rounded-md border border-sidebar-border bg-sidebar p-4 shadow">
          {children}
        </div>
      </div>
    </SidebarProvider>
  );
};

export default Layout;
