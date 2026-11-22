// The development widget gallery (/dev/widgets) is on only when ENABLE_WIDGET_GALLERY is "1" or
// "true" (any case, spaces ignored). Any other value, such as "0" or "false", leaves it off, so a
// setting that says no is never read as yes. Read per request, like API_BASE_URL, so one build
// serves every environment. Not server-only: the proxy reads it too.
export const GALLERY_PATH = "/dev/widgets";

export function galleryEnabled(env: Record<string, string | undefined> = process.env): boolean {
  const value = env.ENABLE_WIDGET_GALLERY?.trim().toLowerCase();
  return value === "1" || value === "true";
}

// True for /dev/widgets (with or without a trailing slash) and nothing else.
export function isGalleryPath(pathname: string): boolean {
  return pathname === GALLERY_PATH || pathname === `${GALLERY_PATH}/`;
}
