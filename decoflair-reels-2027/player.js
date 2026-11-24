(() => {
  "use strict";

  const catalog = window.DECOFLAIR_CATALOG;
  const ui = Object.fromEntries([
    "series-title", "chapters", "reel", "product-title", "product-image",
    "product-category", "unit-price", "availability", "buy", "watch-product",
    "quantity", "minus", "plus", "subtotal", "checked",
  ].map(id => [id, document.getElementById(id)]));
  const seriesButtons = [...document.querySelectorAll("[data-series]")];
  const names = {interior: "Interioare în detaliu", exterior: "Fațade cu caracter"};
  const timing = catalog.timeline;
  const format = new Intl.NumberFormat("ro-RO", {minimumFractionDigits: 2, maximumFractionDigits: 2});
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  const maxQuantity = Number(ui.quantity.max);
  let products = [];
  let active = -1;
  let animation;
  let selectedSeries;

  function money(cents) {
    return format.format(cents / 100) + " lei";
  }

  function quantity() {
    const parsed = Math.trunc(ui.quantity.valueAsNumber);
    return Number.isFinite(parsed) ? Math.min(maxQuantity, Math.max(1, parsed)) : 1;
  }

  function updateSubtotal() {
    const amount = quantity();
    ui.minus.disabled = amount <= 1;
    ui.plus.disabled = amount >= maxQuantity;
    ui.subtotal.value = money(products[active].price * amount);
  }

  function animatePrice() {
    if (animation) animation.cancel();
    if (reduced.matches) return;
    animation = ui["unit-price"].animate(
      [{opacity: 0, transform: "translateY(8px)"}, {opacity: 1, transform: "translateY(0)"}],
      {duration: 240, easing: "ease-out"},
    );
  }

  function showProduct(index) {
    if (active === index) return;
    active = index;
    const product = products[index];
    ui["product-image"].src = product.image;
    ui["product-image"].alt = product.name;
    ui["product-category"].textContent = product.category;
    ui["product-title"].textContent = product.name;
    ui["unit-price"].textContent = money(product.price);
    ui.availability.textContent = product.availability;
    ui.buy.href = product.url;
    ui.quantity.value = "1";
    [...ui.chapters.children].forEach((button, i) => {
      if (index === i) button.setAttribute("aria-current", "true");
      else button.removeAttribute("aria-current");
    });
    updateSubtotal();
    animatePrice();
  }

  function jump(index, offset) {
    showProduct(index);
    ui.reel.currentTime = timing.start + index * timing.chapter + offset;
  }

  function readTime() {
    if (ui.reel.seeking || ui.reel.readyState < 1) return;
    const index = Math.floor((ui.reel.currentTime - timing.start + 0.002) / timing.chapter);
    showProduct(Math.max(0, Math.min(products.length - 1, index)));
  }

  function showSeries(group) {
    if (selectedSeries === group) return;
    selectedSeries = group;
    products = catalog.products.filter(product => product.group === group);
    active = -1;
    for (const button of seriesButtons) {
      button.setAttribute("aria-pressed", String(button.dataset.series === group));
    }
    ui["series-title"].textContent = names[group];
    ui.reel.pause();
    ui.reel.poster = group + "-coperta.jpg";
    ui.reel.src = "decoflair-" + group + "-reel.mp4";
    ui.reel.setAttribute("aria-label", "Reel " + names[group]);
    ui.chapters.replaceChildren(...products.map((product, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = product.category;
      button.addEventListener("click", () => jump(index, 0.045));
      return button;
    }));
    showProduct(0);
  }

  seriesButtons.forEach(button => button.addEventListener("click", () => {
    window.history.replaceState(null, "", "#" + button.dataset.series);
    showSeries(button.dataset.series);
  }));
  if ("requestVideoFrameCallback" in ui.reel) {
    const followFrame = () => {
      readTime();
      ui.reel.requestVideoFrameCallback(followFrame);
    };
    ui.reel.requestVideoFrameCallback(followFrame);
  } else {
    ui.reel.addEventListener("timeupdate", readTime);
  }
  ui.reel.addEventListener("seeked", readTime);
  ui["watch-product"].addEventListener("click", () => {
    jump(active, timing.reveal);
    if (window.matchMedia("(max-width: 779px)").matches) {
      ui.reel.scrollIntoView({block: "center", behavior: reduced.matches ? "auto" : "smooth"});
    }
  });
  ui.quantity.addEventListener("input", updateSubtotal);
  ui.quantity.addEventListener("change", () => {
    ui.quantity.value = String(quantity());
    updateSubtotal();
  });
  ui.minus.addEventListener("click", () => {
    ui.quantity.value = String(quantity() - 1);
    updateSubtotal();
  });
  ui.plus.addEventListener("click", () => {
    ui.quantity.value = String(quantity() + 1);
    updateSubtotal();
  });
  ui.checked.dateTime = catalog.checked;
  ui.checked.textContent = catalog.checked.split("-").reverse().join(".");
  showSeries(window.location.hash === "#exterior" ? "exterior" : "interior");
})();
