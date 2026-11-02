(function () {
  "use strict";

  var STORAGE_KEY = "dsa-theme";
  var COLORS = {
    indigo: { primary: "indigo", accent: "indigo" },
    teal: { primary: "teal", accent: "cyan" },
    "deep-purple": { primary: "deep-purple", accent: "pink" },
    green: { primary: "green", accent: "light-green" },
    "deep-orange": { primary: "deep-orange", accent: "amber" },
    "blue-grey": { primary: "blue-grey", accent: "blue" }
  };

  var switcher = document.querySelector("[data-theme-switcher]");
  if (!switcher) {
    return;
  }

  var schemeButton = switcher.querySelector(".theme-switcher__scheme");
  var select = switcher.querySelector(".theme-switcher__select");
  if (!schemeButton || !select) {
    return;
  }

  function readState() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (error) {
      return {};
    }
  }

  function writeState(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (error) {
      // Storage can be unavailable in private browsing; the theme still applies.
    }
  }

  function currentScheme() {
    return document.body.getAttribute("data-md-color-scheme") === "slate" ? "slate" : "default";
  }

  function currentColor() {
    var primary = document.body.getAttribute("data-md-color-primary") || "indigo";
    return COLORS[primary] ? primary : "indigo";
  }

  function updateSchemeButton() {
    var label = currentScheme() === "slate" ? "Switch to light mode" : "Switch to dark mode";
    schemeButton.title = label;
    schemeButton.setAttribute("aria-label", label);
  }

  function applyColor(colorKey, persist) {
    var color = COLORS[colorKey] || COLORS.indigo;
    document.body.setAttribute("data-md-color-primary", color.primary);
    document.body.setAttribute("data-md-color-accent", color.accent);
    select.value = COLORS[colorKey] ? colorKey : "indigo";
    if (persist !== false) {
      saveState();
    }
  }

  function saveState() {
    writeState({
      scheme: currentScheme(),
      color: select.value,
      primary: document.body.getAttribute("data-md-color-primary"),
      accent: document.body.getAttribute("data-md-color-accent")
    });
  }

  var saved = readState();
  var initialColor = COLORS[saved.color]
    ? saved.color
    : COLORS[currentColor()]
      ? currentColor()
      : "indigo";
  var expected = COLORS[initialColor];
  if (
    document.body.getAttribute("data-md-color-primary") !== expected.primary ||
    document.body.getAttribute("data-md-color-accent") !== expected.accent
  ) {
    applyColor(initialColor, false);
  } else {
    select.value = initialColor;
  }
  updateSchemeButton();

  schemeButton.addEventListener("click", function () {
    document.body.setAttribute(
      "data-md-color-scheme",
      currentScheme() === "slate" ? "default" : "slate"
    );
    updateSchemeButton();
    saveState();
  });

  select.addEventListener("change", function () {
    applyColor(select.value);
  });

  window.addEventListener("storage", function (event) {
    if (event.key !== STORAGE_KEY || !event.newValue) {
      return;
    }
    try {
      var state = JSON.parse(event.newValue);
      if (state.scheme) {
        document.body.setAttribute("data-md-color-scheme", state.scheme);
        updateSchemeButton();
      }
      if (state.color && COLORS[state.color]) {
        applyColor(state.color, false);
      }
    } catch (error) {
      // Ignore malformed state from another tab.
    }
  });
})();
