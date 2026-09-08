/* CyberLavandaTea is a dark-only theme.
   No toggle: lock the dark scheme as early as possible to avoid a flash and
   to keep any component that reads data-theme consistent. */
(function () {
  var el = document.documentElement;
  el.classList.add("dark");
  el.classList.remove("light");
  el.setAttribute("data-theme", "dark");
  el.style.colorScheme = "dark";
})();
