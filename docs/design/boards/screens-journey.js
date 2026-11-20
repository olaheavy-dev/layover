/* Starting a trip and Comparing: a screen opened with ?tab=trip shows the phone Trip tab first.
   The board pages use this to show both phone tabs of one state. screen.js sets up the tabs. */
document.addEventListener("DOMContentLoaded", function () {
  if (/[?&]tab=trip\b/.test(location.search)) {
    var tab = document.getElementById("tab-trip");
    if (tab) { tab.click(); }
  }
});

/* Board frames are short, so a screen can open at the part that matters: data-scroll-end on the body scrolls the
   canvas to its end (the Choose and Try again buttons), and data-peek="last" on the card row shows the last card on a phone. */
(function () {
  function peek() {
    var canvas = document.querySelector(".canvas");
    var track = document.querySelector(".cmp-track[data-peek]");
    if (track && track.scrollWidth > track.clientWidth) { track.scrollLeft = track.scrollWidth; }
    if (canvas && document.body.hasAttribute("data-scroll-end")) { canvas.scrollTo({ top: canvas.scrollHeight, behavior: "instant" }); }
  }
  window.addEventListener("load", function () {
    peek();
    var tab = document.getElementById("tab-trip");
    if (tab) { tab.addEventListener("click", function () { setTimeout(peek, 0); }); }
  });
})();
