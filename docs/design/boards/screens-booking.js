/* Booking screens: on a phone, the Trip tab opens at the Booking section, the part that matters (the board frames are short).
   Other screens have no #booking section, so this does nothing there. screen.js sets up the tabs. */
(function () {
  function toBooking() {
    var canvas = document.querySelector(".canvas");
    var section = document.getElementById("booking");
    var index = document.querySelector(".section-index");
    if (!canvas || !section || !index || !window.matchMedia("(max-width: 63.99rem)").matches) { return; }
    canvas.scrollTo({ top: section.offsetTop - index.offsetHeight, behavior: "instant" });
  }
  window.addEventListener("load", function () {
    var tab = document.getElementById("tab-trip");
    if (tab) { tab.addEventListener("click", function () { setTimeout(toBooking, 0); }); }
    toBooking();
  });
})();
