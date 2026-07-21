"use client";

import { motion } from "framer-motion";

interface LoadingSkeletonProps {
  count?: number;
  className?: string;
  variant?: "card" | "line" | "chart";
}

export default function LoadingSkeleton({ count = 6, className = "", variant = "card" }: LoadingSkeletonProps) {
  if (variant === "line") {
    return (
      <div className={`space-y-3 ${className}`}>
        {Array.from({ length: count }).map((_, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0 }}
            animate={{ opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.1 }}
            className="h-4 rounded-lg"
            style={{ background: "rgba(148, 163, 184, 0.1)", width: `${100 - i * 10}%` }}
          />
        ))}
      </div>
    );
  }

  if (variant === "chart") {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: [0.3, 0.6, 0.3] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className={`rounded-xl h-64 ${className}`}
        style={{ background: "rgba(148, 163, 184, 0.06)" }}
      />
    );
  }

  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 ${className}`}>
      {Array.from({ length: count }).map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0 }}
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.1 }}
          className="h-32 rounded-xl"
          style={{ background: "rgba(148, 163, 184, 0.06)", border: "1px solid rgba(148, 163, 184, 0.06)" }}
        />
      ))}
    </div>
  );
}
