"use client";

import { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function Shell({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  // Check window size to switch between mobile drawer and desktop sidebar
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 1024;
      setIsMobile(mobile);
      if (mobile) {
        setCollapsed(false);
      }
    };
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const sidebarWidth = isMobile ? 0 : collapsed ? 80 : 280;

  return (
    <div className="min-h-screen text-zinc-100 flex" style={{ background: "#09090B" }}>
      {/* Sidebar - Desktop and Mobile */}
      <Sidebar
        collapsed={collapsed}
        onToggle={() => setCollapsed(!collapsed)}
        mobileOpen={mobileOpen}
        onMobileClose={() => setMobileOpen(false)}
        isMobile={isMobile}
      />

      {/* Main Content Area */}
      <div
        className="flex-1 flex flex-col min-w-0 transition-all duration-300 ease-in-out"
        style={{ paddingLeft: sidebarWidth }}
      >
        <div className="relative max-w-[1500px] w-full mx-auto flex flex-col min-h-screen px-4 sm:px-6 md:px-8">
          <Topbar
            sidebarWidth={sidebarWidth}
            isMobile={isMobile}
            onMenuClick={() => setMobileOpen(!mobileOpen)}
          />
          <main className="flex-1 pb-12 pt-28 flex flex-col">
            {children}
          </main>
        </div>
      </div>

      {/* Mobile Drawer Overlay Background */}
      {isMobile && mobileOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 transition-opacity duration-300"
          onClick={() => setMobileOpen(false)}
        />
      )}
    </div>
  );
}
