// The development widget gallery (/dev/widgets) is on only when ENABLE_WIDGET_GALLERY is set to a
// value. Read per request, like API_BASE_URL, so one build serves every environment. Not
// server-only: the proxy reads it too.
export const GALLERY_PATH = "/dev/widgets";

export function galleryEnabled(env: Record<string, string | undefined> = process.env): boolean {
  return Boolean(env.ENABLE_WIDGET_GALLERY);
}

// True for /dev/widgets (with or without a trailing slash) and nothing else.
export function isGalleryPath(pathname: string): boolean {
  return pathname === GALLERY_PATH || pathname === `${GALLERY_PATH}/`;
}
