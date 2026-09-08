/* CyberLavandaTea — tema dark-only.
   Nessun toggle: fissiamo lo schema scuro il prima possibile per evitare
   il flash e per coerenza con eventuali componenti che leggono data-theme. */
(function () {
  var el = document.documentElement;
  el.classList.add("dark");
  el.classList.remove("light");
  el.setAttribute("data-theme", "dark");
  el.style.colorScheme = "dark";
})();
