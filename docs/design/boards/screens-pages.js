/* Phone and navigation, and the pages outside the trip. A screen opened with ?tab=trip shows the phone Trip tab first, and ?at=...
   scrolls the page to a section (or "fare", the Flights widget that View in trip leads to), so a board frame can show that part.
   screen.js sets up the tabs, the section index and its current section. */
document.addEventListener("DOMContentLoaded", function () {
  if (/[?&]tab=trip\b/.test(location.search)) {
    var tab = document.getElementById("tab-trip");
    if (tab) { tab.click(); }
  }
});

window.addEventListener("load", function () {
  var match = /[?&]at=([a-z-]+)/.exec(location.search);
  if (!match) { return; }
  var canvas = document.querySelector(".canvas");
  if (!canvas) { return; }
  var index = canvas.querySelector(".section-index");
  var target = match[1] === "fare"
    ? (document.getElementById("fare-title") || {}).parentNode
    : document.getElementById(match[1]);
  if (target && match[1] === "fare") { target = target.closest(".widget"); }
  if (!target) { return; }
  function go() {
    var offset = (index ? index.offsetHeight : 0) + 8;
    canvas.scrollTo({ top: canvas.scrollTop + target.getBoundingClientRect().top - canvas.getBoundingClientRect().top - offset, behavior: "instant" });
  }
  go();
  setTimeout(go, 60);
});
