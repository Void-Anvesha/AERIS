import './globals.css';
import type { Metadata } from 'next';
import Script from 'next/script';

export const metadata: Metadata = {
  title: 'AERIS',
  description: 'AI Powered Urban Air Quality Intelligence Platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';
  const googleMapsUrl = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;

  return (
    <html lang="en">
      <head>
        {apiKey && (
          <Script
            src={googleMapsUrl}
            strategy="beforeInteractive"
          />
        )}
      </head>
      <body>{children}</body>
    </html>
  );
}

