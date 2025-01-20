"use client";

import { useState } from "react";

import { Info } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { createCheckoutSession } from "@/lib/stripe";
import { api } from "@/trpc/react";

const Page = () => {
  const { data: credits } = api.user.getMyCredits.useQuery();
  const [creditsToBuy, setCreditsToBuy] = useState<number[]>([100]);
  const creditsToBuyAmount = creditsToBuy[0]!;
  const price = (creditsToBuyAmount / 50).toFixed(2);

  return (
    <div>
      <span className="text-xl font-semibold">Billing</span>
      <div className="h-2" />
      <span className="text-sm text-gray-500">
        You currently have {credits?.credits} credits.
      </span>
      <div className="h-2" />
      <div className="rounded-md border border-blue-200 bg-blue-50 px-4 py-2 text-blue-700">
        <div className="flex items-center gap-2">
          <Info className="size-4" />
          <span className="text-sm">
            Each credit allows you to index 1 file in a repository.
          </span>
        </div>
        <span className="text-sm">
          e.g. If your project has 100 files, you will need credits to index it.
        </span>
      </div>
      <div className="h-4" />
      <Slider
        defaultValue={[100]}
        min={30}
        max={1000}
        step={10}
        onValueChange={(value) => setCreditsToBuy(value)}
        value={creditsToBuy}
      />
      <div className="h-4" />
      <Button
        type="button"
        onClick={() => {
          createCheckoutSession(creditsToBuyAmount);
        }}
      >
        Buy {creditsToBuyAmount} credits for ${price}
      </Button>
    </div>
  );
};

export default Page;
