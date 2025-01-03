import { Bot, CreditCard, LayoutDashboard, Presentation } from "lucide-react";

export const sidebar_items = [
  {
    id: 1,
    title: "Dashboard",
    url: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    id: 2,
    title: "Q&A",
    url: "/dashboard/qa",
    icon: Bot,
  },
  {
    id: 3,
    title: "Meetings",
    url: "/dashboard/meetings",
    icon: Presentation,
  },
  {
    id: 4,
    title: "Billing",
    url: "/dashboard/billing",
    icon: CreditCard,
  },
];
