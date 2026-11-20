/* Shared behaviour for the board screens: theme from the URL hash, phone tabs, section index.
   The theme comes from the hash (#light or #dark) because a board page cannot reach into a frame
   that was opened from disk (file://). */
(function () {
  var root = document.documentElement;

  function applyTheme() {
    var wanted = location.hash.replace("#", "");
    if (wanted === "dark" || wanted === "light") {
      root.setAttribute("data-theme", wanted);
    }
  }
  applyTheme();
  window.addEventListener("hashchange", applyTheme);

  document.addEventListener("DOMContentLoaded", function () {
    var phone = window.matchMedia("(max-width: 63.99rem)");
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    var workspace = document.querySelector(".workspace");
    var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
    var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
    var chatLog = document.querySelector(".chat__log");

    function showView(view) {
      workspace.setAttribute("data-view", view);
      tabs.forEach(function (tab) {
        var on = tab.getAttribute("data-view") === view;
        tab.setAttribute("aria-selected", on ? "true" : "false");
        tab.tabIndex = on ? 0 : -1;
      });
      if (view === "chat" && chatLog) { chatLog.scrollTop = chatLog.scrollHeight; }
      // Opening the Trip tab clears its "3 new" badge.
      if (view === "trip") {
        Array.prototype.forEach.call(document.querySelectorAll(".tab__badge"), function (b) { b.hidden = true; });
      }
    }

    function setRoles() {
      panels.forEach(function (panel) {
        if (phone.matches) { panel.setAttribute("role", "tabpanel"); } else { panel.removeAttribute("role"); }
      });
    }

    if (workspace && tabs.length) {
      tabs.forEach(function (tab, i) {
        tab.addEventListener("click", function () { showView(tab.getAttribute("data-view")); });
        tab.addEventListener("keydown", function (event) {
          var next = event.key === "ArrowRight" ? i + 1 : event.key === "ArrowLeft" ? i - 1 : null;
          if (next === null) { return; }
          var target = tabs[(next + tabs.length) % tabs.length];
          showView(target.getAttribute("data-view"));
          target.focus();
        });
      });
      setRoles();
      if (phone.addEventListener) { phone.addEventListener("change", setRoles); }
    }

    if (chatLog) { chatLog.scrollTop = chatLog.scrollHeight; }

    // "Jump to latest": shows when the traveller has scrolled up in a long chat.
    var jump = document.getElementById("jump");
    if (jump && chatLog) {
      var updateJump = function () { jump.hidden = chatLog.scrollHeight - chatLog.scrollTop - chatLog.clientHeight < 120; };
      chatLog.addEventListener("scroll", updateJump, { passive: true });
      jump.addEventListener("click", function () {
        chatLog.scrollTo({ top: chatLog.scrollHeight, behavior: reduce.matches ? "auto" : "smooth" });
        chatLog.focus({ preventScroll: true });
      });
      updateJump();
    }

    // "View trip" on the trip strip and "View in trip" on a compact card open the Trip tab.
    Array.prototype.forEach.call(document.querySelectorAll("[data-goto-tab]"), function (b) {
      b.addEventListener("click", function () {
        showView(b.getAttribute("data-goto-tab"));
        var tab = document.getElementById("tab-" + b.getAttribute("data-goto-tab"));
        if (tab) { tab.focus(); }
      });
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-goto]"), function (b) {
      b.addEventListener("click", function () {
        showView("trip");
        var widget = document.getElementById(b.getAttribute("data-goto")).closest(".widget");
        var canvasEl = document.querySelector(".canvas");
        var index = canvasEl.querySelector(".section-index");
        canvasEl.scrollTop = canvasEl.scrollTop + widget.getBoundingClientRect().top - canvasEl.getBoundingClientRect().top - index.offsetHeight - 8;
        document.getElementById("tab-trip").focus();
      });
    });

    // Links that would leave the board (home, How it works) do nothing here, so the theme hash stays.
    Array.prototype.forEach.call(document.querySelectorAll('a[href="#top"], a[href="#how"]'), function (a) {
      a.addEventListener("click", function (event) { event.preventDefault(); });
    });

    // Section index: jump to a section, and mark the current one while the canvas scrolls.
    var canvas = document.querySelector(".canvas");
    var links = Array.prototype.slice.call(document.querySelectorAll(".section-index a"));
    if (!canvas || !links.length) { return; }
    var sections = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });

    links.forEach(function (a, i) {
      a.addEventListener("click", function (event) {
        event.preventDefault();
        var top = sections[i].offsetTop - canvas.querySelector(".section-index").offsetHeight;
        canvas.scrollTo({ top: top, behavior: reduce.matches ? "auto" : "smooth" });
      });
    });

    function mark() {
      var line = canvas.scrollTop + canvas.clientHeight * 0.6;
      var current = 0;
      sections.forEach(function (section, i) { if (section.offsetTop <= line) { current = i; } });
      links.forEach(function (a, i) {
        if (i === current) { a.setAttribute("aria-current", "true"); } else { a.removeAttribute("aria-current"); }
      });
      var active = links[current];
      var list = active.closest(".section-index__list");
      if (list && list.scrollWidth > list.clientWidth) {
        list.scrollLeft = active.offsetLeft - list.clientWidth / 2 + active.offsetWidth / 2;
      }
    }
    canvas.addEventListener("scroll", mark, { passive: true });
    window.addEventListener("resize", mark);
    mark();
  });
})();
