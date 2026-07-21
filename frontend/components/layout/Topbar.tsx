"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bell,
  Search,
  User,
  Moon,
  Sun,
  ChevronDown,
  LogOut,
  Settings,
  HelpCircle,
  Menu,
} from "lucide-react";

interface TopbarProps {
  sidebarWidth?: number;
  isMobile?: boolean;
  onMenuClick?: () => void;
}

export default function Topbar({
  sidebarWidth = 280,
  isMobile = false,
  onMenuClick,
}: TopbarProps) {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [isDark, setIsDark] = useState(true);

  return (
    <header
      className="absolute top-4 left-4 right-4 sm:left-6 sm:right-6 md:left-8 md:right-8 z-30 h-16 flex items-center justify-between px-4 sm:px-6 rounded-2xl"
      style={{
        background: "rgba(24, 24, 27, 0.65)",
        backdropFilter: "blur(16px)",
        border: "1px solid rgba(255, 255, 255, 0.04)",
        boxShadow: "0 10px 30px -10px rgba(0,0,0,0.5)",
      }}
    >
      {/* Left section: Mobile menu trigger & Minimal Search */}
      <div className="flex items-center gap-3 flex-1">
        {isMobile && (
          <button
            onClick={onMenuClick}
            className="p-2 rounded-xl text-zinc-400 hover:text-white transition-colors"
            style={{
              background: "rgba(255, 255, 255, 0.02)",
              border: "1px solid rgba(255, 255, 255, 0.04)",
            }}
          >
            <Menu className="w-5 h-5" />
          </button>
        )}

        {/* Minimal Search Bar */}
        <div className="relative max-w-xs w-full hidden md:block">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
          <input
            type="text"
            placeholder="Search stations, metrics..."
            className="w-full pl-9 pr-4 py-2 rounded-xl text-xs bg-zinc-900/40 border border-white/5 text-zinc-200 focus:outline-none focus:border-blue-500/50 transition-all placeholder-zinc-500"
          />
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-2.5 sm:gap-3 flex-shrink-0">
        {/* Static Current AQI status badge */}
        <div
          className="flex items-center gap-2 px-3 py-1.5 rounded-full text-[11px] font-semibold"
          style={{
            background: "rgba(34, 197, 94, 0.08)",
            border: "1px solid rgba(34, 197, 94, 0.15)",
            color: "#22C55E",
          }}
        >
          <span className="w-1.5 h-1.5 rounded-full animate-pulse bg-emerald-500" />
          <span>AQI STATUS: HEALTHY</span>
        </div>

        {/* Theme Toggle */}
        <button
          onClick={() => setIsDark(!isDark)}
          className="p-2 sm:p-2.5 rounded-xl text-zinc-400 hover:text-white transition-colors"
          style={{
            background: "rgba(255, 255, 255, 0.02)",
            border: "1px solid rgba(255, 255, 255, 0.04)",
          }}
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => {
              setShowNotifications(!showNotifications);
              setShowProfile(false);
            }}
            className="p-2 sm:p-2.5 rounded-xl text-zinc-400 hover:text-white transition-colors relative"
            style={{
              background: "rgba(255, 255, 255, 0.02)",
              border: "1px solid rgba(255, 255, 255, 0.04)",
            }}
          >
            <Bell className="w-4 h-4" />
            <span
              className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"
            />
          </button>

          <AnimatePresence>
            {showNotifications && (
              <motion.div
                initial={{ opacity: 0, y: 8, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 8, scale: 0.95 }}
                className="absolute right-0 top-12 w-72 sm:w-80 rounded-2xl overflow-hidden z-50 p-1"
                style={{
                  background: "rgba(24, 24, 27, 0.95)",
                  backdropFilter: "blur(24px)",
                  border: "1px solid rgba(255, 255, 255, 0.06)",
                  boxShadow: "0 20px 40px rgba(0,0,0,0.6)",
                }}
              >
                <div className="px-3.5 py-2.5 border-b border-white/[0.04] flex items-center justify-between">
                  <h3 className="text-[10px] font-bold uppercase tracking-wider text-zinc-400">
                    Notifications
                  </h3>
                  <span
                    className="text-[9px] px-2 py-0.5 rounded-full font-bold bg-red-500/10 text-red-400"
                  >
                    4 New
                  </span>
                </div>
                <div className="max-h-60 overflow-y-auto divide-y divide-white/[0.03]">
                  {[
                    { msg: "Ghaziabad AQI crossed 300", time: "2 min ago", color: "#EF4444" },
                    { msg: "Delhi PM2.5 hazardous levels", time: "15 min ago", color: "#EF4444" },
                    { msg: "Kanpur emissions spike", time: "32 min ago", color: "#F59E0B" },
                    { msg: "Lucknow forecast worsening", time: "1 hr ago", color: "#F59E0B" },
                  ].map((n, i) => (
                    <div
                      key={i}
                      className="px-3.5 py-2.5 flex items-start gap-2.5 hover:bg-white/[0.02] cursor-pointer transition-colors"
                    >
                      <span
                        className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0"
                        style={{ background: n.color, boxShadow: `0 0 6px ${n.color}` }}
                      />
                      <div>
                        <p className="text-[11px] font-medium text-zinc-200">{n.msg}</p>
                        <p className="text-[9px] text-zinc-500 mt-0.5">{n.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Profile */}
        <div className="relative">
          <button
            onClick={() => {
              setShowProfile(!showProfile);
              setShowNotifications(false);
            }}
            className="flex items-center gap-2 pl-1.5 pr-2 py-1 rounded-xl transition-colors hover:bg-white/[0.02] border border-transparent hover:border-white/5"
          >
            <div
              className="w-7 h-7 rounded-lg flex items-center justify-center text-[10px] font-bold"
              style={{
                background: "rgba(59, 130, 246, 0.12)",
                color: "#3B82F6",
                border: "1px solid rgba(59, 130, 246, 0.2)",
              }}
            >
              A
            </div>
            <div className="text-left hidden sm:block">
              <p className="text-[10px] font-bold text-zinc-200 leading-tight">Admin</p>
              <p className="text-[8px] text-zinc-500 leading-tight">Control Desk</p>
            </div>
            <ChevronDown className="w-3 h-3 text-zinc-500" />
          </button>

          <AnimatePresence>
            {showProfile && (
              <motion.div
                initial={{ opacity: 0, y: 8, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 8, scale: 0.95 }}
                className="absolute right-0 top-12 w-48 rounded-2xl overflow-hidden z-50 p-1"
                style={{
                  background: "rgba(24, 24, 27, 0.95)",
                  backdropFilter: "blur(24px)",
                  border: "1px solid rgba(255, 255, 255, 0.06)",
                  boxShadow: "0 20px 40px rgba(0,0,0,0.6)",
                }}
              >
                {[
                  { icon: User, label: "Profile" },
                  { icon: Settings, label: "Settings" },
                  { icon: HelpCircle, label: "Help Center" },
                  { icon: LogOut, label: "Logout", danger: true },
                ].map((item, i) => (
                  <button
                    key={i}
                    className={`flex items-center gap-2 w-full px-3 py-2 rounded-xl text-[11px] font-medium transition-colors ${
                      item.danger
                        ? "text-red-400 hover:bg-red-500/10"
                        : "text-zinc-300 hover:text-white hover:bg-white/5"
                    }`}
                  >
                    <item.icon className="w-3.5 h-3.5" />
                    {item.label}
                  </button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </header>
  );
}
