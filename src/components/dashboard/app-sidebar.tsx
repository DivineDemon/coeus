"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { PackageCheck, PackageOpen, Plus, Waypoints } from "lucide-react";

import useProject from "@/hooks/use-project";
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
  const { projects, projectId, setProjectId } = useProject();

  return (
    <Sidebar collapsible="icon" variant="floating">
      <SidebarHeader>
        <div className="flex items-center gap-2 text-[rgba(37,99,235,0.8)]">
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
                      className={cn("hover:shadow-md", {
                        "bg-primary text-white hover:bg-primary hover:text-white":
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
              {projects?.map((project) => (
                <SidebarMenuItem key={project.id}>
                  <SidebarMenuButton asChild>
                    <div
                      onClick={() => setProjectId(project.id)}
                      className={cn(
                        "flex w-full cursor-pointer items-center justify-center gap-2.5 hover:shadow-md",
                        {
                          "bg-primary text-white hover:bg-primary hover:text-white":
                            project.id === projectId,
                        }
                      )}
                    >
                      {project.id === projectId ? (
                        <PackageOpen />
                      ) : (
                        <PackageCheck />
                      )}
                      {open && (
                        <span className="flex-1 text-left">{project.name}</span>
                      )}
                    </div>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
              <div className="h-2" />
              <SidebarMenuItem>
                <Link
                  href="/dashboard/create-project"
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
