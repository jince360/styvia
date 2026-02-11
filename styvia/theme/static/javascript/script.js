(() => {
    const toggle = document.getElementById("mobile-menu-toggle");
    const close = document.getElementById("mobile-menu-close");
    const menu = document.getElementById("mobile-menu");
    const overlay = document.getElementById("mobile-menu-overlay");

    if (!toggle || !close || !menu || !overlay) return;

    const openMenu = () => {
        menu.classList.remove("-translate-x-full");
        overlay.classList.remove("opacity-0", "pointer-events-none");
        overlay.classList.add("opacity-100");
        menu.setAttribute("aria-hidden", "false");
        toggle.setAttribute("aria-expanded", "true");
    };

    const closeMenu = () => {
        menu.classList.add("-translate-x-full");
        overlay.classList.add("opacity-0", "pointer-events-none");
        overlay.classList.remove("opacity-100");
        menu.setAttribute("aria-hidden", "true");
        toggle.setAttribute("aria-expanded", "false");
    };

    toggle.addEventListener("click", openMenu);
    close.addEventListener("click", closeMenu);
    overlay.addEventListener("click", closeMenu);
})();