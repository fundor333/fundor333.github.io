/* CyberLavandaTea — baseline behaviour, no dependencies. */
(function () {
  "use strict";

  // --- Mobile menu: close it when a link is tapped -------------------------
  var trigger = document.getElementById("menu-trigger");
  if (trigger) {
    document.querySelectorAll(".trigger-container a").forEach(function (a) {
      a.addEventListener("click", function () {
        trigger.checked = false;
      });
    });
  }

  // --- Permalink anchor on prose headings --------------------------------
  document.querySelectorAll(".e-content h2[id], .e-content h3[id], .e-content h4[id]").forEach(function (h) {
    if (h.querySelector(".heading-anchor")) return;
    var a = document.createElement("a");
    a.className = "heading-anchor";
    a.href = "#" + h.id;
    a.setAttribute("aria-label", "Link to this section");
    a.textContent = "¶"; // pilcrow
    a.style.marginLeft = "0.4em";
    a.style.opacity = "0";
    a.style.textDecoration = "none";
    a.style.transition = "opacity 120ms ease";
    h.addEventListener("mouseenter", function () { a.style.opacity = "0.6"; });
    h.addEventListener("mouseleave", function () { a.style.opacity = "0"; });
    h.appendChild(a);
  });

  // --- "Cite this post": copy the permalink ------------------------------
  var citeBtn = document.getElementById("cite-copy");
  if (citeBtn) {
    citeBtn.addEventListener("click", function () {
      var input = document.getElementById("cite-url");
      if (!input) return;
      navigator.clipboard.writeText(input.value).then(function () {
        var old = citeBtn.textContent;
        citeBtn.textContent = "Copied ✓";
        setTimeout(function () { citeBtn.textContent = old; }, 1600);
      });
    });
  }
})();
