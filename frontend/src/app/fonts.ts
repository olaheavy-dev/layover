import localFont from "next/font/local";

/*
 * Layover's two typefaces, served from this repository (design brief, "How the fonts are served"):
 * Source Serif 4 for display, Source Sans 3 for body text. Both are variable fonts, one upright and one
 * italic file each, copied from docs/design/boards/fonts/ (tools/check_copy.py keeps the copies identical).
 *
 * The `font-family` declaration is written into the CSS as it is, so each name is quoted: a name with a
 * number in it ("Source Sans 3") is not valid CSS without quotes, and the browser then drops the
 * whole @font-face rule without an error. The names match --font-family-display and --font-family-body
 * in styles/tokens.css. Next.js adds `size-adjust` fallbacks on its own. e2e/pages.spec.ts checks
 * that both fonts load.
 * Docs: https://nextjs.org/docs/app/api-reference/components/font#declarations
 */
export const sourceSerif = localFont({
  src: [
    { path: "../fonts/SourceSerif4Variable-Roman.woff2", weight: "200 900", style: "normal" },
    { path: "../fonts/SourceSerif4Variable-Italic.woff2", weight: "200 900", style: "italic" },
  ],
  display: "swap",
  declarations: [{ prop: "font-family", value: '"Source Serif 4"' }],
  variable: "--font-source-serif",
});

export const sourceSans = localFont({
  src: [
    { path: "../fonts/SourceSans3VF-Upright.woff2", weight: "200 900", style: "normal" },
    { path: "../fonts/SourceSans3VF-Italic.woff2", weight: "200 900", style: "italic" },
  ],
  display: "swap",
  declarations: [{ prop: "font-family", value: '"Source Sans 3"' }],
  variable: "--font-source-sans",
});
