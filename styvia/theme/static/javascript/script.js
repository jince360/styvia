(() => {
    const toggle = document.getElementById("mobile-menu-toggle");
    const close = document.getElementById("mobile-menu-close");
    const menu = document.getElementById("mobile-menu");
    const overlay = document.getElementById("mobile-menu-overlay");

    if (!toggle || !close || !menu || !overlay) return;

    const resetNestedMenus = () => {
        const nestedToggles = menu.querySelectorAll(".mobile-menu-arrow");

        nestedToggles.forEach((arrowButton) => {
            const targetId = arrowButton.dataset.target;
            const target = targetId ? document.getElementById(targetId) : null;
            const icon = arrowButton.querySelector(".material-symbols-outlined");

            if (target) {
                target.classList.add("hidden");
                target.style.display = "none";
            }
            arrowButton.setAttribute("aria-expanded", "false");
            if (icon) {
                icon.classList.remove("rotate-90");
            }
        });
    };

    const toggleNestedMenu = (arrowButton) => {
        const targetId = arrowButton.dataset.target;
        const target = targetId ? document.getElementById(targetId) : null;
        const icon = arrowButton.querySelector(".material-symbols-outlined");

        if (!target) return;

        const isExpanded = arrowButton.getAttribute("aria-expanded") === "true";
        const shouldExpand = !isExpanded;

        target.classList.toggle("hidden", !shouldExpand);
        target.style.display = shouldExpand ? "block" : "none";
        arrowButton.setAttribute("aria-expanded", shouldExpand ? "true" : "false");

        if (icon) {
            icon.classList.toggle("rotate-90", shouldExpand);
        }
    };

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
        resetNestedMenus();
    };

    toggle.addEventListener("click", openMenu);
    close.addEventListener("click", closeMenu);
    overlay.addEventListener("click", closeMenu);

    menu.addEventListener("click", (event) => {
        const arrowButton = event.target.closest(".mobile-menu-arrow");
        if (!arrowButton) return;

        event.preventDefault();
        event.stopPropagation();
        toggleNestedMenu(arrowButton);
    });
})();
