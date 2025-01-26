import { Check, Waypoints } from "lucide-react";

import Heading from "@/components/heading";
import MaxWidthWrapper from "@/components/max-width-wrapper";
import ShinyButton from "@/components/shiny-button";
import BackgroundPattern from "@/components/ui/background-pattern";

const App = () => {
  return (
    <>
      <section className="relative mt-16 flex h-[calc(100vh-64px)] flex-col items-center justify-center">
        <BackgroundPattern className="absolute left-1/2 top-20 z-0 -translate-x-1/2 opacity-35" />
        <div className="absolute left-1/2 top-1/2 z-0 size-72 rounded-full bg-primary/50 blur-[50px]" />
        <div className="absolute left-1/3 top-1/3 z-0 size-36 rounded-full bg-purple-500/50 blur-[50px]" />
        <div className="relative z-[1] flex h-full flex-col items-center justify-center gap-6 pb-16 text-center">
          <Waypoints className="size-12 text-primary" />
          <Heading className="bg-gradient-to-r from-blue-900 via-primary to-blue-400 bg-clip-text text-transparent">
            Collaboration, now a Breeze
          </Heading>
          <p className="max-w-prose text-base/7 text-gray-600">
            With <span className="font-bold text-primary">Coeus</span>, you can
            achieve with your team what you couldn't
            <br />
            before. Next gen team collaboration with an intuitive interface.
          </p>
          <ul className="flex flex-col items-start space-y-2 text-left text-base/7 text-gray-600">
            {[
              "Real-Time Code repository analysis.",
              "Repository Commits analysis.",
              "Seamless Team Collaboration.",
            ].map((item, idx) => (
              <li key={idx} className="flex items-center gap-1.5 text-left">
                <Check className="size-5 shrink-0 text-primary" />
                {item}
              </li>
            ))}
          </ul>
          <div className="w-full max-w-80">
            <ShinyButton
              href="/sign-up"
              className="relative z-10 h-14 w-full text-base shadow-lg transition-shadow duration-300 hover:shadow-xl"
            >
              Start for Free Today
            </ShinyButton>
          </div>
        </div>
      </section>
      <section className="relative bg-primary/75 pb-4">
        <div className="absolute inset-x-0 bottom-24 top-24 bg-primary" />
        <div className="relative mx-auto">
          <MaxWidthWrapper className="relative">
            <div className="-m-2 rounded-xl bg-gray-900/5 p-2 ring-1 ring-inset ring-gray-900/10 lg:-m-4 lg:rounded-2xl lg:p-4"></div>
          </MaxWidthWrapper>
        </div>
      </section>
    </>
  );
};

export default App;
