/* CyberLavandaTea — client-side search with Lunr.
   Requires lunr.js loaded first (see layouts/_partials/search-index.html).
   The index is /search.json (the SearchIndex output format).
   Form: #search  ·  input: #search-input  ·  results target: .search-results

   User input is tokenised and fed to lunr via index.query(), never to
   index.search() — so ":" "~" "+" "-" etc. can't trigger a QueryParseError
   and crash the page. */
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
      var builder = this;
      builder.ref("uri");
      builder.field("title", { boost: 8 });
      builder.field("tags", { boost: 4 });
      builder.field("categories", { boost: 4 });
      builder.field("description", { boost: 2 });
      builder.field("content");
      docs.forEach(function (d) {
        try { builder.add(d); lookup[d.uri] = d; } catch (e) { /* skip a bad doc */ }
      });
    });
  }

  // Split on whitespace and every lunr query metacharacter.
  function tokenize(term) {
    return (term || "")
      .toLowerCase()
      .split(/[\s:~^+\-*"'()[\]{}?!.,;/\\]+/)
      .filter(Boolean);
  }

  function search(term) {
    var toks = tokenize(term);
    if (!toks.length || !index) return [];
    try {
      return index.query(function (q) {
        toks.forEach(function (t) {
          q.term(t, { boost: 12 });                                      // exact
          if (t.length >= 3) q.term(t, { boost: 3, wildcard: lunr.Query.wildcard.TRAILING }); // prefix
          if (t.length >= 5) q.term(t, { boost: 1, editDistance: 1 });   // fuzzy
        });
      });
    } catch (e) {
      return [];
    }
  }

  function render(term) {
    var results = search(term);
    target.innerHTML = "";
    var h = document.createElement("h2");
    h.className = "search-results-title";
    h.textContent = results.length === 0
      ? "No results for “" + term + "”"
      : results.length + " results for “" + term + "”";
    target.appendChild(h);
    try { document.title = h.textContent; } catch (e) {}

    results.forEach(function (r) {
      var d = lookup[r.ref];
      if (!d) return;
      var node;
      if (tpl && tpl.content) {
        node = tpl.content.cloneNode(true);
        var link = node.querySelector(".search-result-link");
        link.href = d.uri;
        link.textContent = d.title || d.uri;
        node.querySelector(".search-result-summary").textContent = truncate(d.content || "", 40);
        var t = node.querySelector(".search-result-date");
        if (t) t.textContent = d.date || "";
      } else {
        node = document.createElement("article");
        node.className = "post-item";
        var a = document.createElement("a");
        a.href = d.uri; a.textContent = d.title || d.uri;
        var hh = document.createElement("h4"); hh.className = "post-item-title"; hh.appendChild(a);
        var p = document.createElement("p"); p.textContent = truncate(d.content || "", 40);
        node.appendChild(hh); node.appendChild(p);
      }
      target.appendChild(node);
    });
  }

  function run(term) {
    term = (term || "").trim();
    if (!term) return;
    if (index) { render(term); return; }
    pending = term;
    if (run._loading) return;
    run._loading = true;
    var req = new XMLHttpRequest();
    req.open("GET", "/search.json");
    req.responseType = "json";
    req.onload = function () {
      var data = req.response;
      if (!data && req.responseText) {
        try { data = JSON.parse(req.responseText); } catch (e) { data = []; }
      }
      build(Array.isArray(data) ? data : []);
      if (pending) render(pending);
    };
    req.onerror = function () { run._loading = false; };
    req.send();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    run(input.value);
  });

  var q = new URLSearchParams(location.search).get("q");
  if (q) { input.value = q; run(q); }
})();
