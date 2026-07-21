import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AERIS',
  description: 'AI Powered Urban Air Quality Intelligence Platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
