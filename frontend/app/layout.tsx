import "./globals.css";
import type { Metadata } from "next";

import { Footer } from "../components/Footer";
import { Navbar } from "../components/Navbar";

export const metadata: Metadata = {
  title: "ILoveLaTeX",
  description: "LaTeX, Word, and PDF conversions for academics and professionals.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <Navbar />
        <main className="mx-auto w-full max-w-6xl px-6 py-12">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
