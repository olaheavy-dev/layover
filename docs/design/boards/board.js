/* Board page: the Light/Dark switch and the scaling of the 1440 px frame.
   The switch changes the hash of each frame's address (#light or #dark). The screen listens for that
   and sets its own theme. This works when the page is opened from disk (file://), where a page cannot
   reach into a frame. */
(function () {
  var root = document.documentElement;
  var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-theme-choice]"));
  var frames = Array.prototype.slice.call(document.querySelectorAll("iframe[data-screen]"));
  // Only a board screen (screens/name.html, with optional ?name=value pairs) is loaded, and only with a known theme.
  // Anything else leaves the frame as it is, so a changed attribute cannot point a frame at another page.
  var THEMES = ["light", "dark"];
  var SCREEN = /^screens\/[a-z0-9-]+\.html(\?[a-z]+=[a-z0-9-]+(&[a-z]+=[a-z0-9-]+)*)?$/;

  function setTheme(theme) {
    if (THEMES.indexOf(theme) === -1) { return; }
    root.setAttribute("data-theme", theme);
    buttons.forEach(function (button) {
      button.setAttribute("aria-pressed", button.getAttribute("data-theme-choice") === theme ? "true" : "false");
    });
    frames.forEach(function (frame) {
      var screen = frame.getAttribute("data-screen");
      if (SCREEN.test(screen)) { frame.src = screen + "#" + theme; }
    });
    try { history.replaceState(null, "", "#" + theme); } catch (e) { /* some browsers refuse on disk */ }
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () { setTheme(button.getAttribute("data-theme-choice")); });
  });

  var first = location.hash.replace("#", "") === "dark" ? "dark" : "light";
  setTheme(first);

  var desktops = Array.prototype.slice.call(document.querySelectorAll(".frame--desktop"));
  function fit() {
    desktops.forEach(function (desktop) {
      var scale = Math.min(1, desktop.clientWidth / 1440);
      desktop.style.setProperty("--scale", String(scale));
    });
  }
  window.addEventListener("resize", fit);
  fit();
})();
