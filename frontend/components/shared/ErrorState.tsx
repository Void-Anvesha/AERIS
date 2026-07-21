"use client";

import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export default function ErrorState({
  message = "Something went wrong. Please try again.",
  onRetry,
}: ErrorStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col items-center justify-center py-16 px-4"
    >
      <div
        className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4"
        style={{ background: "rgba(239, 68, 68, 0.12)" }}
      >
        <AlertTriangle className="w-8 h-8" style={{ color: "#EF4444" }} />
      </div>
      <p className="text-slate-300 text-center mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
          style={{
            background: "rgba(0, 229, 255, 0.12)",
            color: "#00E5FF",
            border: "1px solid rgba(0, 229, 255, 0.2)",
          }}
        >
          Try Again
        </button>
      )}
    </motion.div>
  );
}
