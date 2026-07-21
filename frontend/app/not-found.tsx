"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { AlertTriangle, ArrowLeft } from "lucide-react";

export default function NotFound() {
  return (
    <div
      className="min-h-[70vh] flex flex-col items-center justify-center p-6 text-center select-none"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="max-w-md w-full p-8 rounded-2xl border flex flex-col items-center border-white/5 shadow-2xl"
        style={{
          background: "rgba(24, 24, 27, 0.65)",
          backdropFilter: "blur(20px)",
        }}
      >
        <div
          className="w-14 h-14 rounded-2xl flex items-center justify-center mb-5"
          style={{
            background: "rgba(245, 158, 11, 0.08)",
            border: "1px solid rgba(245, 158, 11, 0.2)",
          }}
        >
          <AlertTriangle className="w-6 h-6 text-amber-500" />
        </div>

        <h1 className="text-xl font-bold text-zinc-100 uppercase tracking-wider mb-2">
          404 - Not Found
        </h1>
        <p className="text-xs text-zinc-400 mb-6 leading-relaxed">
          The requested command path does not exist. The platform routing coordinates may be outdated or missing.
        </p>

        <Link href="/">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl text-xs font-bold transition-all"
            style={{
              background: "linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)",
              color: "#FAFAFA",
              boxShadow: "0 4px 12px rgba(59, 130, 246, 0.25)",
            }}
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Return to Command Center</span>
          </motion.button>
        </Link>
      </motion.div>
    </div>
  );
}
