"use client";

import Image from "next/image";
import { PropsWithChildren } from "react";

import {
  LogoutLink,
  useKindeBrowserClient,
} from "@kinde-oss/kinde-auth-nextjs";

import AppSidebar from "@/components/dashboard/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { clearLocalStorage } from "@/lib/utils";

const Layout = ({ children }: PropsWithChildren) => {
  const { user } = useKindeBrowserClient();

  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="m-2 w-full">
        <div className="flex items-center gap-2 rounded-md border border-sidebar-border bg-sidebar px-4 py-2 shadow">
          <div className="ml-auto" />
          {user && (
            <LogoutLink onClick={clearLocalStorage}>
              <Image
                src={
                  user?.picture
                    ? user?.picture
                    : "https://ui.shadcn.com/avatars/04.png"
                }
                alt="user-image"
                width={28}
                height={28}
                className="size-[28px] rounded-full"
              />
            </LogoutLink>
          )}
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
