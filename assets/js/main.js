(function () {
  "use strict";

  var root = document.documentElement;
  var header = document.querySelector(".site-header");
  var themeToggles = document.querySelectorAll("[data-theme-toggle]");
  var navToggle = document.querySelector("[data-nav-toggle]");
  var navDialog = document.getElementById("mobile-nav");
  var navClose = document.querySelector("[data-nav-close]");

  function themeSaved() {
    try {
      return Boolean(localStorage.getItem("theme"));
    } catch (error) {
      return false;
    }
  }

  function currentTheme() {
    return root.dataset.theme === "dark" ? "dark" : "light";
  }

  function updateThemeToggles() {
    var next = currentTheme() === "dark" ? "light" : "dark";
    themeToggles.forEach(function (toggle) {
      toggle.setAttribute("aria-label", "Switch to " + next + " theme");
      toggle.setAttribute("title", "Switch to " + next + " theme");
      var label = toggle.querySelector(".theme-switch__label");
      if (label) {
        label.textContent = "Switch to " + next + " theme";
      }
    });
  }

  function setTheme(theme) {
    root.dataset.theme = theme;
    try {
      localStorage.setItem("theme", theme);
    } catch (error) {
      /* Storage can be unavailable; the theme still applies for this page. */
    }
    updateThemeToggles();
  }

  if (themeToggles.length) {
    updateThemeToggles();
    themeToggles.forEach(function (toggle) {
      toggle.addEventListener("click", function () {
        setTheme(currentTheme() === "dark" ? "light" : "dark");
      });
    });
  }

  if (!themeSaved() && window.matchMedia) {
    var media = window.matchMedia("(prefers-color-scheme: dark)");
    var onSchemeChange = function (event) {
      if (themeSaved()) return;
      root.dataset.theme = event.matches ? "dark" : "light";
      updateThemeToggles();
    };
    if (media.addEventListener) {
      media.addEventListener("change", onSchemeChange);
    }
  }

  /* Mobile navigation dialog */

  function closeNav() {
    if (!navDialog) return;
    if (navDialog.open) navDialog.close();
  }

  if (navToggle && navDialog && typeof navDialog.showModal === "function") {
    navToggle.addEventListener("click", function () {
      navDialog.showModal();
      document.body.setAttribute("data-nav-open", "true");
      navToggle.setAttribute("aria-expanded", "true");
    });

    navDialog.addEventListener("close", function () {
      document.body.removeAttribute("data-nav-open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.focus();
    });

    if (navClose) {
      navClose.addEventListener("click", function () {
        navDialog.close();
      });
    }

    navDialog.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && navDialog.open) {
        navDialog.close();
      }
    });

    navDialog.addEventListener("click", function (event) {
      if (event.target !== navDialog) return;
      var box = navDialog.getBoundingClientRect();
      var outside =
        event.clientX < box.left ||
        event.clientX > box.right ||
        event.clientY < box.top ||
        event.clientY > box.bottom;
      if (outside) navDialog.close();
    });

    navDialog.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navDialog.close();
      });
    });

    var desktop = window.matchMedia("(min-width: 901px)");
    var onDesktop = function (event) {
      if (event.matches) closeNav();
    };
    if (desktop.addEventListener) {
      desktop.addEventListener("change", onDesktop);
    }
  }

  /* Header state on scroll */

  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Scroll reveal */

  var revealItems = document.querySelectorAll("[data-reveal]");
  if (revealItems.length) {
    if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      var revealObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              revealObserver.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
      );
      revealItems.forEach(function (item) {
        revealObserver.observe(item);
      });
    } else {
      revealItems.forEach(function (item) {
        item.classList.add("is-visible");
      });
    }
  }

  /* Table of contents */

  var toc = document.querySelector("[data-toc]");
  var article = document.querySelector("[data-article]");
  if (toc && article) {
    var headings = article.querySelectorAll("h2, h3");
    var list = toc.querySelector("ol");
    if (headings.length >= 2 && list) {
      headings.forEach(function (heading, index) {
        if (!heading.id) {
          heading.id = "section-" + (index + 1);
        }
        var item = document.createElement("li");
        item.className = heading.tagName === "H3" ? "toc-h3" : "toc-h2";
        var link = document.createElement("a");
        link.href = "#" + heading.id;
        link.textContent = heading.textContent;
        item.appendChild(link);
        list.appendChild(item);
      });
      toc.hidden = false;

      if ("IntersectionObserver" in window) {
        var tocLinks = Array.prototype.slice.call(list.querySelectorAll("a"));
        var spy = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              if (!entry.isIntersecting) return;
              tocLinks.forEach(function (link) {
                link.classList.toggle("is-active", link.getAttribute("href") === "#" + entry.target.id);
              });
            });
          },
          { rootMargin: "-20% 0px -70% 0px", threshold: 0 }
        );
        headings.forEach(function (heading) {
          spy.observe(heading);
        });
      }
    } else {
      toc.hidden = true;
    }
  }
})();
