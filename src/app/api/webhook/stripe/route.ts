import { headers } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

import Stripe from "stripe";

import { env } from "@/env";
import { db } from "@/server/db";

const stripe = new Stripe(env.STRIPE_SECRET_KEY, {
  apiVersion: "2024-12-18.acacia",
});

export async function POST(request: NextRequest) {
  let event: Stripe.Event;
  const body = await request.text();
  const stripe_signature = (await headers()).get("Stripe-Signature") as string;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      stripe_signature,
      env.STRIPE_WEBHOOK_SECRET
    );
  } catch (error) {
    return NextResponse.json({ error: "Invalid signature!" }, { status: 400 });
  }

  const session = event.data.object as Stripe.Checkout.Session;

  if (event.type === "checkout.session.completed") {
    const credits = Number(session.metadata?.["credits"]);
    const userId = session.client_reference_id;

    if (!userId || !credits) {
      return NextResponse.json(
        { error: "Missing userId or credits!" },
        { status: 400 }
      );
    }

    await db.stripeTransaction.create({
      data: {
        credits,
        userId: userId!,
      },
    });

    await db.user.update({
      where: {
        id: userId,
      },
      data: {
        credits: {
          increment: credits,
        },
      },
    });

    return NextResponse.json(
      { success: true, message: "Purchased Credits Successfully!" },
      { status: 200 }
    );
  }

  return NextResponse.json({ message: "Hello Stripe! " });
}
