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

(() => {
    const carousel = document.querySelector("[data-carousel]");
    if (!carousel) return;

    const slides = Array.from(carousel.querySelectorAll("[data-carousel-slide]"));
    const prevButton = carousel.querySelector("[data-carousel-prev]");
    const nextButton = carousel.querySelector("[data-carousel-next]");

    if (!slides.length) return;

    let currentIndex = slides.findIndex((slide) => !slide.classList.contains("opacity-0"));
    if (currentIndex < 0) currentIndex = 0;

    const updateCarousel = (index) => {
        slides.forEach((slide, slideIndex) => {
            const isActive = slideIndex === index;
            slide.classList.toggle("opacity-100", isActive);
            slide.classList.toggle("opacity-0", !isActive);
            slide.classList.toggle("pointer-events-none", !isActive);
        });

    };

    const goToSlide = (index) => {
        currentIndex = (index + slides.length) % slides.length;
        updateCarousel(currentIndex);
    };

    prevButton?.addEventListener("click", () => goToSlide(currentIndex - 1));
    nextButton?.addEventListener("click", () => goToSlide(currentIndex + 1));

    if (slides.length <= 1) {
        prevButton?.classList.add("hidden");
        nextButton?.classList.add("hidden");
    }

    updateCarousel(currentIndex);
})();
