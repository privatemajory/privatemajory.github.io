(function () {
  "use strict";

  var gallery = document.querySelector("[data-gallery]");
  var filters = document.querySelectorAll("[data-filter]");
  var count = document.querySelector("[data-gallery-count]");
  var empty = document.querySelector("[data-gallery-empty]");

  function visibleCards() {
    return Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]")).filter(function (card) {
      return !card.closest("[hidden]");
    });
  }

  function updateCount() {
    if (!gallery) return;
    var total = gallery.querySelectorAll("[data-lightbox]").length;
    var visible = visibleCards().length;
    if (count) {
      count.textContent = visible === total ? total + " maps" : visible + " of " + total + " maps";
    }
    if (empty) {
      empty.hidden = visible !== 0;
    }
  }

  if (filters.length) {
    filters.forEach(function (button) {
      button.addEventListener("click", function () {
        var filter = button.getAttribute("data-filter");
        filters.forEach(function (other) {
          other.setAttribute("aria-pressed", other === button ? "true" : "false");
        });
        document.querySelectorAll("[data-map-item]").forEach(function (item) {
          var matches = filter === "everything" || item.getAttribute("data-category") === filter;
          item.hidden = !matches;
        });
        updateCount();
      });
    });
  }

  updateCount();

  var dialog = document.getElementById("lightbox");
  if (!dialog) return;

  var image = dialog.querySelector("[data-lightbox-image]");
  var title = dialog.querySelector("[data-lightbox-title]");
  var caption = dialog.querySelector("[data-lightbox-caption]");
  var counter = dialog.querySelector("[data-lightbox-counter]");
  var closeButton = dialog.querySelector("[data-lightbox-close]");
  var prevButton = dialog.querySelector("[data-lightbox-prev]");
  var nextButton = dialog.querySelector("[data-lightbox-next]");
  var currentIndex = 0;
  var trigger = null;

  function cards() {
    return visibleCards();
  }

  function preload(index) {
    var list = cards();
    var card = list[index];
    if (!card) return;
    var source = card.getAttribute("data-full");
    if (!source) return;
    var preloadImage = new Image();
    preloadImage.src = source;
  }

  function show(index) {
    var list = cards();
    if (!list.length) return;
    currentIndex = (index + list.length) % list.length;
    var card = list[currentIndex];
    image.src = card.getAttribute("data-full");
    image.alt = card.getAttribute("data-alt") || "";
    title.textContent = card.getAttribute("data-title") || "";
    caption.textContent = card.getAttribute("data-caption") || "";
    counter.textContent = currentIndex + 1 + " / " + list.length;
    preload(currentIndex + 1);
    preload(currentIndex - 1);
  }

  function open(event) {
    event.preventDefault();
    trigger = event.currentTarget;
    var list = cards();
    var index = list.indexOf(trigger);
    dialog.showModal();
    document.body.classList.add("lightbox-open");
    if (index >= 0) show(index);
  }

  document.querySelectorAll("[data-lightbox]").forEach(function (card) {
    card.addEventListener("click", open);
  });

  closeButton.addEventListener("click", function () {
    dialog.close();
  });

  prevButton.addEventListener("click", function () {
    show(currentIndex - 1);
  });

  nextButton.addEventListener("click", function () {
    show(currentIndex + 1);
  });

  dialog.addEventListener("click", function (event) {
    if (event.target === dialog) {
      dialog.close();
    }
  });

  dialog.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      show(currentIndex - 1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      show(currentIndex + 1);
    }
  });

  var touchStartX = null;
  var figure = dialog.querySelector(".lightbox__figure");
  if (figure) {
    figure.addEventListener(
      "touchstart",
      function (event) {
        touchStartX = event.changedTouches[0].clientX;
      },
      { passive: true }
    );
    figure.addEventListener(
      "touchend",
      function (event) {
        if (touchStartX === null) return;
        var delta = event.changedTouches[0].clientX - touchStartX;
        if (Math.abs(delta) > 50) {
          show(delta > 0 ? currentIndex - 1 : currentIndex + 1);
        }
        touchStartX = null;
      },
      { passive: true }
    );
  }

  dialog.addEventListener("close", function () {
    document.body.classList.remove("lightbox-open");
    image.removeAttribute("src");
    if (trigger) {
      trigger.focus();
      trigger = null;
    }
  });
})();
