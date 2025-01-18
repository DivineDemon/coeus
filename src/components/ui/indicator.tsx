import { cn } from "@/lib/utils";

interface IndicatorProps {
  type: "pending" | "done" | "error";
  className?: string;
}

const Indicator = ({ type, className }: IndicatorProps) => {
  return (
    <div
      className={cn(
        "relative inline-block size-3 rounded-full bg-green-500",
        {
          "bg-red-500": type === "error",
          "bg-green-500": type === "done",
          "bg-yellow-500": type === "pending",
        },
        className
      )}
    >
      <div
        className={cn("absolute inset-0 size-3 animate-ping rounded-full", {
          "bg-red-500": type === "error",
          "bg-green-500": type === "done",
          "bg-yellow-500": type === "pending",
        })}
      />
    </div>
  );
};

export default Indicator;
