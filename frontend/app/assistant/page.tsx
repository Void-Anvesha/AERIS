"use client";

export const dynamic = "force-dynamic";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, Send, Sparkles, User, Paperclip, Mic, ArrowUp } from "lucide-react";
import PageHeader from "@/components/shared/PageHeader";
import { sendChatMessage } from "@/services/api";
import { suggestedQuestions } from "@/services/mockData";
import type { ChatMessage } from "@/types";

export default function AssistantPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hello! I'm **AERIS AI**, your premium air quality intelligence assistant. I can help you analyze pollution data, identify hotspots, run compliance scenarios, and recommend directives. What would you like to explore today?",
      timestamp: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = async (text?: string) => {
    const msg = text || input.trim();
    if (!msg) return;

    const userMsg: ChatMessage = {
      id: `u-${Date.now()}`,
      role: "user",
      content: msg,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await sendChatMessage(msg);
      const assistantMsg: ChatMessage = {
        id: `a-${Date.now()}`,
        role: "assistant",
        content: response,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: `e-${Date.now()}`,
          role: "assistant",
          content: "I apologize, but I encountered an error processing your request. Please try again.",
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div style={{ height: "calc(100vh - 8rem)" }} className="flex flex-col max-w-4xl mx-auto w-full">
      <div className="pb-3 border-b border-white/[0.04]">
        <PageHeader
          title="AI Co-Pilot"
          subtitle="Ask AERIS anything about urban air quality, compliance, and multi-agent directives"
          icon={<Bot className="w-5 h-5" style={{ color: "#3B82F6" }} />}
        />
      </div>

      {/* Messages Canvas */}
      <div className="flex-1 flex flex-col min-h-0 relative">
        <div ref={scrollRef} className="flex-1 overflow-y-auto py-6 space-y-6 scrollbar-thin pr-2">
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                {msg.role === "assistant" && (
                  <div
                    className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                    style={{ background: "rgba(59, 130, 246, 0.12)" }}
                  >
                    <Sparkles className="w-3.5 h-3.5" style={{ color: "#3B82F6" }} />
                  </div>
                )}
                <div
                  className={`max-w-[80%] px-4 py-3 rounded-2xl text-xs leading-relaxed ${
                    msg.role === "user"
                      ? "text-zinc-50 font-normal shadow-md"
                      : "text-zinc-300 border border-white/[0.04] bg-zinc-900/30"
                  }`}
                  style={
                    msg.role === "user"
                      ? {
                          background: "linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)",
                          borderBottomRightRadius: 4,
                        }
                      : {
                          borderBottomLeftRadius: 4,
                        }
                  }
                >
                  {msg.content.split("\n").map((line, i) => {
                    // Render simple headers or bullets/lists
                    const isBullet = line.trim().startsWith("-") || line.trim().startsWith("•") || line.trim().startsWith("* ");
                    const isHeader = line.trim().startsWith("###");
                    let content = line;
                    if (isBullet) content = content.replace(/^[-•*]\s*/, "");
                    if (isHeader) content = content.replace(/^###\s*/, "");

                    return (
                      <p key={i} className={`${i > 0 ? "mt-2" : ""} ${isBullet ? "pl-3 relative before:content-['•'] before:absolute before:left-0 before:text-blue-500" : ""}`}>
                        {isHeader ? (
                          <span className="font-bold text-zinc-100 uppercase tracking-wider block text-[10px] mb-1">{content}</span>
                        ) : (
                          content.split(/(\*\*.*?\*\*)/).map((part, j) =>
                            part.startsWith("**") && part.endsWith("**") ? (
                              <strong key={j} className="font-bold text-zinc-100">
                                {part.slice(2, -2)}
                              </strong>
                            ) : (
                              <span key={j}>{part}</span>
                            )
                          )
                        )}
                      </p>
                    );
                  })}
                </div>
                {msg.role === "user" && (
                  <div
                    className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                    style={{ background: "rgba(255, 255, 255, 0.04)", border: "1px solid rgba(255, 255, 255, 0.06)" }}
                  >
                    <User className="w-3.5 h-3.5 text-zinc-400" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing Indicator */}
          {isTyping && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-4 items-center">
              <div className="w-7 h-7 rounded-lg flex items-center justify-center" style={{ background: "rgba(59, 130, 246, 0.12)" }}>
                <Sparkles className="w-3.5 h-3.5" style={{ color: "#3B82F6" }} />
              </div>
              <div className="flex gap-1 px-4 py-2.5 rounded-2xl border border-white/[0.04] bg-zinc-900/30">
                <span className="w-1.5 h-1.5 rounded-full bg-zinc-500 typing-dot-1" />
                <span className="w-1.5 h-1.5 rounded-full bg-zinc-500 typing-dot-2" />
                <span className="w-1.5 h-1.5 rounded-full bg-zinc-500 typing-dot-3" />
              </div>
            </motion.div>
          )}
        </div>

        {/* Suggested Questions Grid (Bottom anchor above input) */}
        {messages.length === 1 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="pb-4 pt-2 flex-shrink-0 border-t border-white/[0.02] mt-auto"
          >
            <p className="text-[10px] text-zinc-500 uppercase tracking-wider mb-2.5 font-bold">Suggested Inquiries</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2">
              {suggestedQuestions.slice(0, 4).map((q, i) => (
                <button
                  key={i}
                  onClick={() => handleSend(q)}
                  className="p-3 text-left rounded-xl text-[11px] font-medium transition-all hover:bg-white/[0.02] text-zinc-400 hover:text-zinc-200 border border-white/5 bg-zinc-900/20"
                >
                  {q}
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Input Bar (Centered large pill layout) */}
        <div className="pb-4 pt-2 flex-shrink-0">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2 p-1.5 rounded-2xl border border-white/5 bg-zinc-900/40 focus-within:border-blue-500/30 transition-all focus-within:ring-1 focus-within:ring-blue-500/10 shadow-lg"
          >
            {/* Attachment Button */}
            <button
              type="button"
              className="p-2 rounded-xl text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              <Paperclip className="w-4 h-4" />
            </button>

            {/* Input Element */}
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask AERIS AI..."
              className="flex-1 min-w-0 bg-transparent text-xs text-zinc-100 placeholder-zinc-500 outline-none px-2"
              disabled={isTyping}
            />

            {/* Voice Mic Button */}
            <button
              type="button"
              className="p-2 rounded-xl text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              <Mic className="w-4 h-4" />
            </button>

            {/* Send Button */}
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="p-2 rounded-xl transition-all disabled:opacity-20 flex items-center justify-center"
              style={{
                background: input.trim() && !isTyping ? "linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)" : "rgba(255,255,255,0.02)",
                color: "#FAFAFA",
              }}
            >
              <ArrowUp className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
