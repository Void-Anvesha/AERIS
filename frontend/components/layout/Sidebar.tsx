"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  Map,
  TrendingUp,
  Flame,
  Bot,
  Globe,
  Users,
  Settings,
  ChevronLeft,
  ChevronRight,
  Wind,
  X,
} from "lucide-react";

const menuItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/" },
  { icon: Map, label: "AQI Map", href: "/map" },
  { icon: TrendingUp, label: "Forecast", href: "/forecast" },
  { icon: Flame, label: "Hotspots", href: "/hotspots" },
  { icon: Bot, label: "AI Assistant", href: "/assistant" },
  { icon: Globe, label: "Google Earth", href: "/earth" },
  { icon: Users, label: "Citizen Advisory", href: "/advisory" },
  { icon: Settings, label: "Settings", href: "/settings" },
];

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
  mobileOpen: boolean;
  onMobileClose: () => void;
  isMobile: boolean;
}

export default function Sidebar({
  collapsed,
  onToggle,
  mobileOpen,
  onMobileClose,
  isMobile,
}: SidebarProps) {
  const pathname = usePathname();

  // Mobile drawer styling vs Desktop floating sidebar
  const sidebarVariants = {
    mobileHidden: { x: "-110%", width: 260 },
    mobileVisible: { x: 0, width: 260 },
    desktopExpanded: { x: 0, width: 260 },
    desktopCollapsed: { x: 0, width: 80 },
  };

  const getActiveVariant = () => {
    if (isMobile) {
      return mobileOpen ? "mobileVisible" : "mobileHidden";
    }
    return collapsed ? "desktopCollapsed" : "desktopExpanded";
  };

  return (
    <motion.aside
      initial={isMobile ? "mobileHidden" : "desktopExpanded"}
      animate={getActiveVariant()}
      variants={sidebarVariants}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      className={`fixed z-40 flex flex-col ${
        isMobile
          ? "left-0 top-0 h-screen"
          : "left-4 top-4 h-[calc(100vh-2rem)] rounded-2xl"
      }`}
      style={{
        background: "rgba(24, 24, 27, 0.75)",
        backdropFilter: "blur(20px)",
        border: "1px solid rgba(255, 255, 255, 0.05)",
        boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
      }}
    >
      {/* Sidebar Header */}
      <div className="flex items-center justify-between px-5 h-16 border-b border-white/[0.04] flex-shrink-0">
        <div className="flex items-center gap-3">
          <div
            className="flex items-center justify-center w-8 h-8 rounded-xl flex-shrink-0"
            style={{
              background: "rgba(59, 130, 246, 0.1)",
              border: "1px solid rgba(59, 130, 246, 0.2)",
            }}
          >
            <Wind className="w-4.5 h-4.5" style={{ color: "#3B82F6" }} />
          </div>
          <AnimatePresence>
            {(!collapsed || isMobile) && (
              <motion.div
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -8 }}
                transition={{ duration: 0.15 }}
                className="overflow-hidden whitespace-nowrap"
              >
                <h1 className="text-sm font-bold tracking-wider leading-none text-zinc-100">
                  AERIS
                </h1>
                <p className="tracking-widest uppercase mt-0.5 text-zinc-500 font-medium" style={{ fontSize: 8 }}>
                  Smart Air Intelligence
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Close button on mobile */}
        {isMobile && (
          <button
            onClick={onMobileClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-white/5 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-3.5 space-y-1 overflow-y-auto">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href} onClick={isMobile ? onMobileClose : undefined}>
              <motion.div
                whileHover={{ x: 2 }}
                whileTap={{ scale: 0.98 }}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all duration-200 ${
                  isActive
                    ? "text-zinc-50 font-semibold"
                    : "text-zinc-400 hover:text-zinc-200 hover:bg-white/[0.02]"
                }`}
                style={
                  isActive
                    ? {
                        background: "rgba(59, 130, 246, 0.08)",
                        borderLeft: "2px solid #3B82F6",
                        boxShadow: "0 0 15px rgba(59, 130, 246, 0.05)",
                      }
                    : { background: "transparent" }
                }
              >
                <item.icon
                  className="w-4 h-4 flex-shrink-0 transition-colors"
                  style={isActive ? { color: "#3B82F6" } : undefined}
                />
                <AnimatePresence>
                  {(!collapsed || isMobile) && (
                    <motion.span
                      initial={{ opacity: 0, width: 0 }}
                      animate={{ opacity: 1, width: "auto" }}
                      exit={{ opacity: 0, width: 0 }}
                      transition={{ duration: 0.15 }}
                      className="text-xs whitespace-nowrap overflow-hidden"
                    >
                      {item.label}
                    </motion.span>
                  )}
                </AnimatePresence>
                {isActive && (!collapsed || isMobile) && (
                  <motion.div
                    layoutId="sidebar-indicator"
                    className="ml-auto w-1 h-1 rounded-full flex-shrink-0"
                    style={{ background: "#3B82F6", boxShadow: "0 0 8px #3B82F6" }}
                  />
                )}
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* Collapse Toggle - Only visible on desktop */}
      {!isMobile && (
        <div className="px-3.5 py-3 border-t border-white/[0.04] flex-shrink-0">
          <button
            onClick={onToggle}
            className="flex items-center justify-center w-full py-2 rounded-xl text-zinc-500 hover:text-zinc-300 transition-colors"
            style={{
              background: "rgba(255, 255, 255, 0.02)",
              border: "1px solid rgba(255, 255, 255, 0.04)",
            }}
          >
            {collapsed ? <ChevronRight className="w-3.5 h-3.5" /> : <ChevronLeft className="w-3.5 h-3.5" />}
          </button>
        </div>
      )}
    </motion.aside>
  );
}
