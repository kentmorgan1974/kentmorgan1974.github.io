// Progressive enhancement only: every page works without this file.
(function () {
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
