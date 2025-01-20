"use server";

import { redirect } from "next/navigation";

import { auth } from "@clerk/nextjs/server";
import Stripe from "stripe";

import { env } from "@/env";

const stripe = new Stripe(env.STRIPE_SECRET_KEY, {
  apiVersion: "2024-12-18.acacia",
});

export async function createCheckoutSession(credits: number) {
  const { userId } = await auth();

  if (!userId) {
    throw new Error("Unauthorized!");
  }

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ["card"],
    line_items: [
      {
        price_data: {
          currency: "usd",
          product_data: {
            name: `${credits} Coeus Credits`,
          },
          unit_amount: Math.round((credits / 50) * 100),
        },
        quantity: 1,
      },
    ],
    customer_creation: "always",
    mode: "payment",
    success_url: `${env.NEXT_PUBLIC_APP_URL}/dashboard/create-project`,
    cancel_url: `${env.NEXT_PUBLIC_APP_URL}/dashboard/billing`,
    client_reference_id: userId.toString(),
    metadata: {
      credits,
    },
  });

  return redirect(session.url!);
}
