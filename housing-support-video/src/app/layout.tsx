import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "राष्ट्रीय आवास सहायता वीडियो गाइड",
  description:
    "हिंदी में 60 सेकंड का शैक्षणिक वीडियो जो राष्ट्रीय आवास सहायता कार्यक्रम के उद्देश्य, पात्रता, ऑनलाइन आवेदन और प्रमुख लाभ समझाता है।",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
