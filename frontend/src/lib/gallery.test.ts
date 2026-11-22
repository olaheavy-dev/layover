import { galleryEnabled, isGalleryPath } from "./gallery";

describe("the gallery setting", () => {
  it("is off when the setting is unset or blank", () => {
    expect(galleryEnabled({})).toBe(false);
    expect(galleryEnabled({ ENABLE_WIDGET_GALLERY: "" })).toBe(false);
  });

  it("is on only for 1 or true, whatever the case or spaces", () => {
    for (const value of ["1", "true", "TRUE", " True ", " 1 "]) {
      expect(galleryEnabled({ ENABLE_WIDGET_GALLERY: value })).toBe(true);
    }
  });

  it("stays off for any other value, so a setting that says no is not read as yes", () => {
    for (const value of ["0", "false", "no", "off", "yes", "2", "   "]) {
      expect(galleryEnabled({ ENABLE_WIDGET_GALLERY: value })).toBe(false);
    }
  });

  it("matches /dev/widgets exactly", () => {
    expect(isGalleryPath("/dev/widgets")).toBe(true);
    expect(isGalleryPath("/dev/widgets/")).toBe(true);
    expect(isGalleryPath("/dev/widgets/x")).toBe(false);
    expect(isGalleryPath("/dev")).toBe(false);
    expect(isGalleryPath("/dev/widgetsx")).toBe(false);
  });
});
