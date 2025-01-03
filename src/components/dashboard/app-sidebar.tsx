"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { PackageCheck, PackageOpen, Plus, Waypoints } from "lucide-react";

import { sidebar_items } from "@/lib/constants";
import { cn } from "@/lib/utils";

import { buttonVariants } from "../ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "../ui/sidebar";

const AppSidebar = () => {
  const { open } = useSidebar();
  const pathname = usePathname();

  return (
    <Sidebar collapsible="icon" variant="floating">
      <SidebarHeader>
        <div className="flex items-center gap-2 text-primary/80">
          <Waypoints
            className={cn("size-6 transition-[width]", {
              "size-8": !open,
            })}
          />
          {open && (
            <span className="flex-1 text-left text-xl font-bold">Coeus</span>
          )}
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Application</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {sidebar_items.map((item) => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton asChild>
                    <Link
                      href={item.url}
                      className={cn({
                        "bg-primary text-white hover:bg-primary/85 hover:text-white":
                          pathname === item.url,
                      })}
                    >
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Your Projects</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {[...Array(5)].map((_, idx) => (
                <SidebarMenuItem key={idx}>
                  <SidebarMenuButton asChild>
                    <div
                      className={cn(
                        "flex w-full items-center justify-center gap-2.5",
                        {
                          "bg-primary text-white": idx === 1,
                        }
                      )}
                    >
                      {idx === 1 ? <PackageOpen /> : <PackageCheck />}
                      {open && (
                        <span className="flex-1 text-left">
                          Project {idx + 1}
                        </span>
                      )}
                    </div>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
              <div className="h-2" />
              <SidebarMenuItem>
                <Link
                  href="/"
                  className={cn(
                    "w-fit",
                    buttonVariants({
                      variant: "outline",
                      size: "sm",
                    }),
                    {
                      "size-8": !open,
                    }
                  )}
                >
                  <Plus />
                  {open && "Create Project"}
                </Link>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
};

export default AppSidebar;
