(function () {
  "use strict";

  var root = document.querySelector("[data-catalog]");

  if (root) {
    var cards = Array.prototype.slice.call(root.querySelectorAll("[data-dataset]"));
    var search = root.querySelector("[data-dataset-search]");
    var count = root.querySelector("[data-dataset-count]");
    var empty = root.querySelector("[data-dataset-empty]");
    var grid = root.querySelector("[data-dataset-grid]");
    var sortSelect = root.querySelector("[data-dataset-sort]");
    var reset = root.querySelector("[data-dataset-reset]");
    var themeButtons = root.querySelectorAll("[data-dataset-theme]");
    var formatButtons = root.querySelectorAll("[data-dataset-format]");
    var total = cards.length;

    var state = { query: "", theme: "all", format: "all", sort: "theme" };

    function readUrl() {
      var params = new URLSearchParams(window.location.search);
      state.query = params.get("q") || "";
      state.theme = params.get("theme") || "all";
      state.format = params.get("format") || "all";
      state.sort = params.get("sort") || "theme";
      if (search) search.value = state.query;
      if (sortSelect) sortSelect.value = state.sort;
    }

    function writeUrl() {
      var params = new URLSearchParams();
      if (state.query) params.set("q", state.query);
      if (state.theme !== "all") params.set("theme", state.theme);
      if (state.format !== "all") params.set("format", state.format);
      if (state.sort !== "theme") params.set("sort", state.sort);
      var query = params.toString();
      window.history.replaceState(null, "", query ? "?" + query : window.location.pathname);
    }

    function syncButtons() {
      themeButtons.forEach(function (button) {
        button.setAttribute("aria-pressed", button.getAttribute("data-dataset-theme") === state.theme ? "true" : "false");
      });
      formatButtons.forEach(function (button) {
        button.setAttribute("aria-pressed", button.getAttribute("data-dataset-format") === state.format ? "true" : "false");
      });
    }

    function matches(card) {
      if (state.theme !== "all" && card.getAttribute("data-theme") !== state.theme) return false;
      if (state.format !== "all" && card.getAttribute("data-format") !== state.format) return false;
      if (!state.query) return true;
      var haystack = card.getAttribute("data-search") || "";
      return state.query
        .toLowerCase()
        .split(/\s+/)
        .filter(Boolean)
        .every(function (term) {
          return haystack.indexOf(term) !== -1;
        });
    }

    var comparators = {
      theme: function (a, b) {
        return (
          (a.getAttribute("data-theme") || "").localeCompare(b.getAttribute("data-theme") || "") ||
          (a.getAttribute("data-title") || "").localeCompare(b.getAttribute("data-title") || "")
        );
      },
      title: function (a, b) {
        return (a.getAttribute("data-title") || "").localeCompare(b.getAttribute("data-title") || "");
      },
      records: function (a, b) {
        return Number(b.getAttribute("data-records") || 0) - Number(a.getAttribute("data-records") || 0);
      },
      newest: function (a, b) {
        return (b.getAttribute("data-date") || "").localeCompare(a.getAttribute("data-date") || "");
      }
    };

    function render() {
      var visible = 0;
      cards.forEach(function (card) {
        var show = matches(card);
        card.hidden = !show;
        if (show) visible += 1;
      });

      var ordered = cards.slice().sort(comparators[state.sort] || comparators.theme);
      ordered.forEach(function (card) {
        grid.appendChild(card);
      });

      if (count) {
        count.textContent =
          visible === total
            ? total + (total === 1 ? " dataset" : " datasets")
            : visible + " of " + total + " datasets";
      }
      if (empty) empty.hidden = visible !== 0;
      syncButtons();
      writeUrl();
    }

    if (search) {
      var debounce;
      search.addEventListener("input", function () {
        window.clearTimeout(debounce);
        debounce = window.setTimeout(function () {
          state.query = search.value.trim();
          render();
        }, 120);
      });
    }

    themeButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        state.theme = button.getAttribute("data-dataset-theme");
        render();
      });
    });

    formatButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        state.format = button.getAttribute("data-dataset-format");
        render();
      });
    });

    if (sortSelect) {
      sortSelect.addEventListener("change", function () {
        state.sort = sortSelect.value;
        render();
      });
    }

    if (reset) {
      reset.addEventListener("click", function () {
        state = { query: "", theme: "all", format: "all", sort: state.sort };
        if (search) search.value = "";
        render();
      });
    }

    readUrl();
    render();
  }

  /* Copy-to-clipboard for the citation blocks. */

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    var original = button.textContent.trim();
    button.addEventListener("click", function () {
      var value = button.getAttribute("data-copy") || "";
      var done = function () {
        button.textContent = "Copied";
        window.setTimeout(function () {
          button.textContent = original;
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(done, done);
      } else {
        done();
      }
    });
  });
})();
