import type { Metadata } from "next";
import { Inter as FontSans } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils"

const fontSans = FontSans({
  subsets: ["latin"],
  variable: "--font-sans",
})

export const metadata: Metadata = {
  title: {
    default: "EvuLearn",
    template: "%s | EvuLearn"
  },
  description: "AI-powered YouTube video Summarizer and Quiz generator",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://learntuber.vercel.app",
    siteName: "EvuLearn",
    title: "EvuLearn",
    description: "AI-powered YouTube video Summarizer and Quiz generator",
    images: [
      {
        url: "https://learntuber.vercel.app/og-image.png",
        width: 1200,
        height: 630,
        alt: "EvuLearn - AI-powered YouTube video Summarizer and Quiz generator",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "EvuLearn - AI-powered YouTube Learning",
    description: "Transform your YouTube watching into an interactive learning experience with AI-powered summaries and quizzes.",
    images: ["https://learntuber.vercel.app/og-image.png"],
    creator: "@NirbhaySirsikar",
  },
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/site.webmanifest",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body className={cn(
          "min-h-screen bg-background font-sans antialiased",
          fontSans.variable
        )}
      >
        <div className="h-full w-full bg-white  relative flex items-center justify-center">
          <div className="absolute pointer-events-none inset-0 flex items-center justify-center"></div>

          {children}
        </div>
      </body>
    </html>
  );
}
