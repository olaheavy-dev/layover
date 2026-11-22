import type { Metadata } from "next";
import "./globals.css";
import { sourceSans, sourceSerif } from "./fonts";

export const metadata: Metadata = {
  // The welcome board's title is the default; each page's own title gets Layover's name last, as the
  // boards do (WCAG 2.4.2, Page Titled).
  title: { default: "Where to next? A new trip · Layover", template: "%s · Layover" },
  description: "An AI travel planner for people in the UK.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${sourceSerif.variable} ${sourceSans.variable}`}>
      <body className="bg-bg-primary text-text-primary antialiased">{children}</body>
    </html>
  );
}
