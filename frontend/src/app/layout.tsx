import type { Metadata } from "next";
import "./globals.css";
import { sourceSans, sourceSerif } from "./fonts";

export const metadata: Metadata = {
  title: "App",
  description: "Replace with the product's name and one line about it.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${sourceSerif.variable} ${sourceSans.variable}`}>
      <body className="bg-bg-primary text-text-primary antialiased">{children}</body>
    </html>
  );
}
