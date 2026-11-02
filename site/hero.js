(function () {
  const heroFrame = document.querySelector(".heroFrame");
  const heroScene = document.getElementById("hero-scene");
  const playBtn = document.getElementById("hero-play");
  const mobilePlay = document.getElementById("mobile-hero-play");
  const mobileHero = document.getElementById("mobile-hero");
  const menuToggle = document.getElementById("menu-toggle");
  const menuPanel = document.getElementById("mobile-nav");
  const menuClose = document.getElementById("menu-close");

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let paused = reducedMotion;

  function applyMotionState() {
    if (heroScene) heroScene.classList.toggle("still", paused);
    if (mobileHero) mobileHero.classList.toggle("still", paused);
    const label = paused ? "Play scene" : "Pause scene";
    if (playBtn) {
      playBtn.textContent = label;
      playBtn.setAttribute("aria-pressed", String(paused));
    }
    if (mobilePlay) {
      mobilePlay.textContent = paused ? "Play" : "Pause";
      mobilePlay.setAttribute("aria-pressed", String(paused));
    }
  }

  function toggleMotion() {
    paused = !paused;
    applyMotionState();
  }

  if (heroFrame && heroScene) {
    const fit = () => {
      heroFrame.style.setProperty("--r", heroFrame.clientWidth / 1440);
      heroFrame.style.height = heroFrame.clientWidth * (900 / 1440) + "px";
    };
    new ResizeObserver(fit).observe(heroFrame);
    fit();
  }

  playBtn?.addEventListener("click", toggleMotion);
  mobilePlay?.addEventListener("click", toggleMotion);

  document.addEventListener("keydown", (ev) => {
    if (ev.key !== " " && ev.code !== "Space") return;
    const t = ev.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    if (!heroFrame && !mobileHero) return;
    const inHero =
      heroFrame?.contains(document.activeElement) ||
      mobileHero?.contains(document.activeElement) ||
      document.activeElement === document.body;
    if (!inHero) return;
    ev.preventDefault();
    toggleMotion();
  });

  applyMotionState();

  document.querySelectorAll(".case").forEach((link) => {
    link.addEventListener("click", (ev) => {
      ev.preventDefault();
      const dialog = document.querySelector(link.getAttribute("href"));
      if (!dialog || typeof dialog.showModal !== "function") return;
      dialog.showModal();
      dialog.addEventListener(
        "close",
        () => {
          link.focus();
        },
        { once: true },
      );
    });
  });

  document.querySelectorAll("dialog").forEach((dialog) => {
    dialog.addEventListener("cancel", (ev) => {
      ev.preventDefault();
      dialog.close();
    });
  });

  function openMenu() {
    if (!menuPanel || !menuToggle) return;
    menuPanel.hidden = false;
    menuToggle.setAttribute("aria-expanded", "true");
    menuClose?.focus();
  }

  function closeMenu() {
    if (!menuPanel || !menuToggle) return;
    menuPanel.hidden = true;
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.focus();
  }

  menuToggle?.addEventListener("click", () => {
    if (menuPanel?.hidden) openMenu();
    else closeMenu();
  });
  menuClose?.addEventListener("click", closeMenu);
  menuPanel?.addEventListener("click", (ev) => {
    if (ev.target === menuPanel) closeMenu();
  });
  menuPanel?.querySelectorAll("a").forEach((a) => {
    a.addEventListener("click", closeMenu);
  });

  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && menuPanel && !menuPanel.hidden) closeMenu();
  });

  document.querySelectorAll(".mobileChem button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const on = btn.getAttribute("aria-pressed") === "true";
      document.querySelectorAll(".mobileChem button").forEach((b) => b.setAttribute("aria-pressed", "false"));
      btn.setAttribute("aria-pressed", on ? "false" : "true");
    });
  });
})();
