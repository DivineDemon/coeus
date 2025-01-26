import { Waypoints } from "lucide-react";

import Heading from "@/components/heading";
import BackgroundPattern from "@/components/ui/background-pattern";

const App = () => {
  return (
    <div className="flex w-full flex-1 items-center justify-center p-4">
      <BackgroundPattern className="absolute left-1/2 top-20 z-0 -translate-x-1/2 opacity-35" />
      <div className="relative z-10 flex -translate-y-1/2 flex-col items-center gap-6 text-center">
        <Waypoints className="size-12 text-primary" />
        <Heading className="bg-gradient-to-r from-blue-400 via-primary to-blue-900 bg-clip-text text-transparent">
          Collaboration, now a Breeze
        </Heading>
        <p className="max-w-prose text-base/7 text-gray-600">
          With <span className="font-bold text-primary">Coeus</span>, you can
          achieve with your team what you couldn't
          <br />
          before. Next gen team collaboration with an intuitive interface.
        </p>
      </div>
    </div>
  );
};

export default App;
