/* CyberLavandaTea — ricerca client-side con Lunr.
   Richiede lunr.js caricato prima (vedi layouts/search/list.html).
   L'indice è /search.json (output format SearchIndex).
   Form: #search  ·  input: #search-input  ·  target risultati: .search-results
*/
(function () {
  "use strict";

  var form = document.getElementById("search");
  var input = document.getElementById("search-input");
  var target = document.querySelector(".search-results");
  var tpl = document.getElementById("search-result");
  if (!form || !input || !target) return;

  var index = null;
  var lookup = {};
  var pending = null;

  function truncate(text, minWords) {
    var match, result = "", n = 0, re = /(\S+)(\s*)/g;
    while ((match = re.exec(text))) {
      n++;
      if (n <= minWords) { result += match[0]; continue; }
      var c1 = match[1][match[1].length - 1];
      var c2 = match[2][0];
      if (/[.?!"]/.test(c1) || c2 === "\n") { result += match[1]; break; }
      result += match[0];
    }
    return result + (n > minWords ? " …" : "");
  }

  function build(docs) {
    index = lunr(function () {
      this.ref("uri");
      this.field("title", { boost: 8 });
      this.field("tags", { boost: 4 });
      this.field("categories", { boost: 4 });
      this.field("description", { boost: 2 });
      this.field("content");
      docs.forEach(function (d) { this.add(d); lookup[d.uri] = d; }, this);
    });
  }

  function render(term) {
    var results = index.search(term);
    target.innerHTML = "";
    var h = document.createElement("h2");
    h.className = "search-results-title";
    h.textContent = results.length === 0
      ? "Nessun risultato per «" + term + "»"
      : results.length + " risultati per «" + term + "»";
    target.appendChild(h);
    document.title = h.textContent;

    results.forEach(function (r) {
      var d = lookup[r.ref];
      var node;
      if (tpl) {
        node = tpl.content.cloneNode(true);
        node.querySelector(".search-result-link").href = d.uri;
        node.querySelector(".search-result-link").textContent = d.title;
        node.querySelector(".search-result-summary").textContent = truncate(d.content || "", 40);
        var t = node.querySelector(".search-result-date");
        if (t) t.textContent = d.date || "";
      } else {
        node = document.createElement("article");
        node.className = "post-item";
        node.innerHTML = '<h4 class="post-item-title"><a href="' + d.uri + '"></a></h4><p></p>';
        node.querySelector("a").textContent = d.title;
        node.querySelector("p").textContent = truncate(d.content || "", 40);
      }
      target.appendChild(node);
    });
  }

  function run(term) {
    term = (term || "").trim();
    if (!term) return;
    if (index) { render(term); return; }
    pending = term;
    if (build._started) return;
    build._started = true;
    var req = new XMLHttpRequest();
    req.open("GET", "/search.json");
    req.responseType = "json";
    req.onload = function () {
      build(req.response || []);
      if (pending) render(pending);
    };
    req.send();
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); run(input.value); });

  var q = new URLSearchParams(location.search).get("q");
  if (q) { input.value = q; run(q); }
})();
