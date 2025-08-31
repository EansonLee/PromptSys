import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "提示词生成系统 - AI驱动的创意提示词生成",
  description: "专业的提示词生成系统，支持Android应用开发的创意提示词自动生成，集成多种主题模板和AI Agent自动化功能",
  keywords: ["提示词", "AI", "Android开发", "自动生成", "Claude AI"],
  authors: [{ name: "提示词生成系统" }],
  creator: "提示词生成系统",
  publisher: "提示词生成系统",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'),
  openGraph: {
    title: "提示词生成系统",
    description: "AI驱动的创意提示词生成平台",
    type: "website",
    locale: "zh_CN",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#0a0a0a' }
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" className={`${geistSans.variable} ${geistMono.variable}`}>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <meta name="format-detection" content="telephone=no" />
      </head>
      <body className="antialiased min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 text-glass-primary selection:bg-blue-200 selection:text-gray-800 overflow-x-hidden">
        <div className="min-h-screen flex flex-col relative">
          {/* Light Premium Background Effects */}
          <div className="fixed inset-0 -z-30 pointer-events-none">
            {/* Primary gradient background */}
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50/80 via-white/60 to-cyan-50/80" />
            
            {/* Animated light gradient orbs */}
            <div className="absolute top-0 left-0 w-96 h-96 bg-gradient-to-r from-blue-200/30 to-cyan-200/20 rounded-full blur-3xl animate-floating" />
            <div className="absolute top-1/3 right-0 w-80 h-80 bg-gradient-to-l from-pink-200/25 to-purple-200/20 rounded-full blur-3xl animate-floating" style={{ animationDelay: '1s' }} />
            <div className="absolute bottom-0 left-1/3 w-72 h-72 bg-gradient-to-tr from-cyan-200/25 to-blue-200/20 rounded-full blur-3xl animate-floating" style={{ animationDelay: '2s' }} />
            
            {/* Subtle light grid pattern */}
            <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%23000000%22%20fill-opacity%3D%220.03%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%221%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-50" />
            
            {/* Soft radial light effect */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_40%,rgba(59,130,246,0.08)_0%,transparent_50%)]" />
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_60%,rgba(34,211,238,0.06)_0%,transparent_50%)]" />
          </div>
          
          {/* Content overlay with glass effect */}
          <div className="relative min-h-screen backdrop-blur-[2px]">
            <main className="flex-1 relative z-10">
              {children}
            </main>
          </div>
          
          {/* Light floating particles effect */}
          <div className="fixed inset-0 -z-20 pointer-events-none overflow-hidden">
            <div className="absolute w-2 h-2 bg-blue-300/25 rounded-full animate-floating" style={{ left: '10%', top: '20%', animationDuration: '4s' }} />
            <div className="absolute w-1 h-1 bg-cyan-400/30 rounded-full animate-floating" style={{ left: '20%', top: '60%', animationDuration: '5s', animationDelay: '1s' }} />
            <div className="absolute w-1.5 h-1.5 bg-purple-300/25 rounded-full animate-floating" style={{ left: '80%', top: '30%', animationDuration: '6s', animationDelay: '2s' }} />
            <div className="absolute w-2 h-2 bg-pink-300/20 rounded-full animate-floating" style={{ left: '70%', top: '70%', animationDuration: '4.5s', animationDelay: '0.5s' }} />
            <div className="absolute w-1 h-1 bg-blue-400/35 rounded-full animate-floating" style={{ left: '90%', top: '15%', animationDuration: '7s', animationDelay: '3s' }} />
          </div>
        </div>
      </body>
    </html>
  );
}
