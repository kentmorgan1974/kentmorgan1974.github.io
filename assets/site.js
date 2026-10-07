// Progressive enhancement only: every page works without this file.
(function () {
  // Light / dark toggle. The choice is remembered in this browser only.
  var root = document.documentElement;
  var btn = document.querySelector(".theme");
  var dark = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function current() {
    var a = root.getAttribute("data-theme");
    return a || (dark && dark.matches ? "dark" : "light");
  }
  function label() {
    if (!btn) return;
    var next = current() === "dark" ? "light" : "dark";
    btn.textContent = next === "dark" ? "Dark" : "Light";
    btn.setAttribute("aria-label", "Switch to " + next + " mode");
  }
  if (btn) {
    btn.hidden = false;
    label();
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
      label();
    });
    if (dark && dark.addEventListener) dark.addEventListener("change", label);
  }

  var ua = navigator.userAgent || "";
  var isMac = /Mac|iPhone|iPad/.test(ua) && !/Windows/.test(ua);

  // Put the visitor's own platform first in the download box.
  document.querySelectorAll(".dl[data-has-os]").forEach(function (box) {
    var mine = box.querySelector('[data-os="' + (isMac ? "mac" : "win") + '"]');
    var other = box.querySelector('[data-os="' + (isMac ? "win" : "mac") + '"]');
    if (mine && other) {
      mine.classList.remove("ghost");
      other.classList.add("ghost");
      mine.parentNode.insertBefore(mine, other);
      var tag = box.querySelector(".yours");
      if (tag) tag.textContent = "Detected: " + (isMac ? "Mac" : "Windows");
    }
  });

  // Show each product's current released version, read from its GitHub release.
  document.querySelectorAll("[data-version-repo]").forEach(function (el) {
    fetch("https://api.github.com/repos/" + el.getAttribute("data-version-repo") + "/releases/latest")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (d && d.tag_name) {
          var day = (d.published_at || "").slice(0, 10);
          el.textContent = "Version " + d.tag_name.replace(/^v/, "") + (day ? ", released " + day : "");
        }
      })
      .catch(function () {});
  });
})();
