import { galleryEnabled, isGalleryPath } from "./gallery";

describe("the gallery setting", () => {
  it("is off when the setting is unset or blank", () => {
    expect(galleryEnabled({})).toBe(false);
    expect(galleryEnabled({ ENABLE_WIDGET_GALLERY: "" })).toBe(false);
  });

  it("is on when the setting has a value", () => {
    expect(galleryEnabled({ ENABLE_WIDGET_GALLERY: "1" })).toBe(true);
  });

  it("matches /dev/widgets exactly", () => {
    expect(isGalleryPath("/dev/widgets")).toBe(true);
    expect(isGalleryPath("/dev/widgets/")).toBe(true);
    expect(isGalleryPath("/dev/widgets/x")).toBe(false);
    expect(isGalleryPath("/dev")).toBe(false);
    expect(isGalleryPath("/dev/widgetsx")).toBe(false);
  });
});
