/* The chosen place, Stay and Days screens: a board frame is short, so a screen can open at the part that matters.
   data-scroll-to on the body names an element id; the canvas scrolls to it, under the section index.
   data-scroll-to-phone names another one for a phone, where the canvas is narrower and its sections are taller.
   screen.js sets up the tabs and the section index. */
(function () {
  function go() {
    var phone = window.matchMedia("(max-width: 63.99rem)").matches;
    var id = (phone && document.body.getAttribute("data-scroll-to-phone")) || document.body.getAttribute("data-scroll-to");
    var canvas = document.querySelector(".canvas");
    var target = id && document.getElementById(id);
    if (target && target.closest(".widget")) { target = target.closest(".widget"); }
    if (!canvas || !target || !canvas.offsetParent) { return; }
    var index = canvas.querySelector(".section-index");
    var offset = index ? index.offsetHeight : 0;
    canvas.scrollTo({ top: canvas.scrollTop + target.getBoundingClientRect().top - canvas.getBoundingClientRect().top - offset - 8, behavior: "instant" });
  }
  window.addEventListener("load", function () {
    go();
    var tab = document.getElementById("tab-trip");
    if (tab) { tab.addEventListener("click", function () { setTimeout(go, 0); }); }
  });
})();
