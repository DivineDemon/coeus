import { type Metadata } from "next";
import { EB_Garamond, Inter } from "next/font/google";

import { ClerkProvider } from "@clerk/nextjs";

import "@/assets/css/globals.css";
import { Toaster } from "@/components/ui/sonner";
import { cn } from "@/lib/utils";
import { TRPCReactProvider } from "@/trpc/react";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const eb_garamond = EB_Garamond({
  subsets: ["latin"],
  variable: "--font-heading",
});

export const metadata: Metadata = {
  title: "Coeus",
  description: "Generated by create-t3-app",
  icons: [{ rel: "icon", url: "/favicon.png" }],
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <ClerkProvider>
      <html lang="en" className={cn(inter.variable, eb_garamond.variable)}>
        <body className="flex min-h-[calc(100vh-1px)] flex-col bg-gray-50 font-sans antialiased">
          <main className="relative flex flex-1 flex-col">
            <TRPCReactProvider>
              <Toaster richColors={true} />
              {children}
            </TRPCReactProvider>
          </main>
        </body>
      </html>
    </ClerkProvider>
  );
}
