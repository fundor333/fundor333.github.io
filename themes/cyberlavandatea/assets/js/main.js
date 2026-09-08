/* CyberLavandaTea — comportamenti di base, senza dipendenze. */
(function () {
  "use strict";

  // --- Menu mobile: chiudi al click su una voce -----------------------------
  var trigger = document.getElementById("menu-trigger");
  if (trigger) {
    document.querySelectorAll(".trigger-container a").forEach(function (a) {
      a.addEventListener("click", function () {
        trigger.checked = false;
      });
    });
  }

  // --- Anchor sui heading della prosa (link permanente) --------------------
  document.querySelectorAll(".e-content h2[id], .e-content h3[id], .e-content h4[id]").forEach(function (h) {
    if (h.querySelector(".heading-anchor")) return;
    var a = document.createElement("a");
    a.className = "heading-anchor";
    a.href = "#" + h.id;
    a.setAttribute("aria-label", "Link a questa sezione");
    a.textContent = "¶"; // ¶
    a.style.marginLeft = "0.4em";
    a.style.opacity = "0";
    a.style.textDecoration = "none";
    a.style.transition = "opacity 120ms ease";
    h.addEventListener("mouseenter", function () { a.style.opacity = "0.6"; });
    h.addEventListener("mouseleave", function () { a.style.opacity = "0"; });
    h.appendChild(a);
  });

  // --- Copia permalink ("cita questo post") --------------------------------
  var citeBtn = document.getElementById("cite-copy");
  if (citeBtn) {
    citeBtn.addEventListener("click", function () {
      var input = document.getElementById("cite-url");
      if (!input) return;
      navigator.clipboard.writeText(input.value).then(function () {
        var old = citeBtn.textContent;
        citeBtn.textContent = "Copiato ✓";
        setTimeout(function () { citeBtn.textContent = old; }, 1600);
      });
    });
  }
})();
