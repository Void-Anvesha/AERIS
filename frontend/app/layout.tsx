import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/Providers";
import Shell from "@/components/layout/Shell";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "AERIS — AI-Powered Urban Air Quality Intelligence",
  description:
    "Real-time air quality monitoring, forecasting, and AI-driven insights for Smart City governance across India.",
  keywords: ["air quality", "AQI", "pollution", "smart city", "India", "AI", "monitoring"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} dark`}>
      <head>
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          crossOrigin=""
        />
      </head>
      <body className="font-sans antialiased selection:bg-cyan-500/30 selection:text-cyan-200" style={{ background: "#0F172A" }}>
        <Providers>
          <Shell>{children}</Shell>
        </Providers>
      </body>
    </html>
  );
}
