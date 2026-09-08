/* CyberLavandaTea — "back to top" button (#totop). */
(function () {
  var btn = document.getElementById("totop");
  if (!btn) return;

  function onScroll() {
    if (window.scrollY > 600) btn.classList.add("is-visible");
    else btn.classList.remove("is-visible");
  }

  btn.addEventListener("click", function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();
