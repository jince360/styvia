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
    const indicators = Array.from(carousel.querySelectorAll("[data-carousel-indicator]"));
    const pagination = carousel.querySelector("[data-carousel-pagination]");

    if (!slides.length) return;

    let currentIndex = slides.findIndex((slide) => !slide.classList.contains("opacity-0"));
    if (currentIndex < 0) currentIndex = 0;
    const AUTO_SLIDE_INTERVAL = 5000;
    const RESUME_DELAY = 1200;
    const SWIPE_THRESHOLD = 40;
    let autoSlideTimer = null;
    let touchStartX = 0;
    let touchStartY = 0;
    let touchDeltaX = 0;
    let touchDeltaY = 0;

    const updateCarousel = (index) => {
        slides.forEach((slide, slideIndex) => {
            const isActive = slideIndex === index;
            slide.classList.toggle("opacity-100", isActive);
            slide.classList.toggle("opacity-0", !isActive);
            slide.classList.toggle("pointer-events-none", !isActive);
        });

        indicators.forEach((indicator, indicatorIndex) => {
            const isActive = indicatorIndex === index;
            indicator.classList.toggle("bg-white", isActive);
            indicator.classList.toggle("bg-white/50", !isActive);
            indicator.setAttribute("aria-current", isActive ? "true" : "false");
        });

    };

    const goToSlide = (index) => {
        currentIndex = (index + slides.length) % slides.length;
        updateCarousel(currentIndex);
    };

    const stopAutoSlide = () => {
        if (!autoSlideTimer) return;
        clearTimeout(autoSlideTimer);
        autoSlideTimer = null;
    };

    const scheduleNextAutoSlide = (delay = AUTO_SLIDE_INTERVAL) => {
        if (slides.length <= 1) return;
        stopAutoSlide();
        autoSlideTimer = setTimeout(() => {
            goToSlide(currentIndex + 1);
            scheduleNextAutoSlide(AUTO_SLIDE_INTERVAL);
        }, delay);
    };

    const startAutoSlide = () => {
        scheduleNextAutoSlide(AUTO_SLIDE_INTERVAL);
    };

    const handleNavigation = (index) => {
        goToSlide(index);
        scheduleNextAutoSlide(AUTO_SLIDE_INTERVAL);
    };

    const onTouchStart = (event) => {
        if (!event.touches?.length) return;
        touchStartX = event.touches[0].clientX;
        touchStartY = event.touches[0].clientY;
        touchDeltaX = 0;
        touchDeltaY = 0;
        stopAutoSlide();
    };

    const onTouchMove = (event) => {
        if (!event.touches?.length) return;
        touchDeltaX = event.touches[0].clientX - touchStartX;
        touchDeltaY = event.touches[0].clientY - touchStartY;
    };

    const onTouchEnd = () => {
        const isHorizontalSwipe = Math.abs(touchDeltaX) > Math.abs(touchDeltaY);
        const hasEnoughDistance = Math.abs(touchDeltaX) >= SWIPE_THRESHOLD;

        if (isHorizontalSwipe && hasEnoughDistance) {
            if (touchDeltaX < 0) {
                handleNavigation(currentIndex + 1);
            } else {
                handleNavigation(currentIndex - 1);
            }
            return;
        }

        scheduleNextAutoSlide(RESUME_DELAY);
    };

    prevButton?.addEventListener("click", () => handleNavigation(currentIndex - 1));
    nextButton?.addEventListener("click", () => handleNavigation(currentIndex + 1));
    indicators.forEach((indicator, index) => {
        indicator.addEventListener("click", () => handleNavigation(index));
    });

    carousel.addEventListener("mouseenter", stopAutoSlide);
    carousel.addEventListener("mouseleave", () => scheduleNextAutoSlide(RESUME_DELAY));
    carousel.addEventListener("focusin", stopAutoSlide);
    carousel.addEventListener("focusout", () => scheduleNextAutoSlide(RESUME_DELAY));
    carousel.addEventListener("touchstart", onTouchStart, { passive: true });
    carousel.addEventListener("touchmove", onTouchMove, { passive: true });
    carousel.addEventListener("touchend", onTouchEnd, { passive: true });
    carousel.addEventListener("touchcancel", () => scheduleNextAutoSlide(RESUME_DELAY), { passive: true });

    document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
            stopAutoSlide();
            return;
        }
        scheduleNextAutoSlide(RESUME_DELAY);
    });

    if (slides.length <= 1) {
        prevButton?.classList.add("hidden");
        nextButton?.classList.add("hidden");
        pagination?.classList.add("hidden");
    }

    updateCarousel(currentIndex);
    startAutoSlide();
})();

(() => {
    const brandCarousel = document.querySelector("[data-brand-carousel]");
    if (!brandCarousel) return;

    const track = brandCarousel.querySelector("[data-brand-track]");
    const prevButton = brandCarousel.querySelector("[data-brand-prev]");
    const nextButton = brandCarousel.querySelector("[data-brand-next]");
    const pagination = brandCarousel.closest("section")?.querySelector("[data-brand-pagination]");

    if (!track) return;

    const getPageWidth = () => track.clientWidth;
    const getMaxScroll = () => Math.max(track.scrollWidth - track.clientWidth, 0);
    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
    const getPageCount = () => {
        const width = getPageWidth();
        const maxScroll = getMaxScroll();
        if (!width) return 1;
        return Math.max(1, Math.ceil(maxScroll / width) + 1);
    };
    let dots = [];

    const getCurrentPage = () => {
        const width = getPageWidth();
        if (!width) return 0;
        return Math.round(track.scrollLeft / width);
    };

    const scrollToPage = (pageIndex) => {
        const width = getPageWidth();
        const maxScroll = getMaxScroll();
        if (!width || maxScroll <= 0) return;

        const target = clamp(pageIndex * width, 0, maxScroll);
        track.scrollTo({ left: target, behavior: "smooth" });
    };

    const renderDots = () => {
        if (!pagination) return;

        pagination.innerHTML = "";
        const pageCount = getPageCount();
        if (pageCount <= 1) {
            pagination.classList.add("hidden");
            dots = [];
            return;
        }

        pagination.classList.remove("hidden");
        dots = Array.from({ length: pageCount }, (_, index) => {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.className = "w-2 h-2 rounded-full bg-zinc-300 transition-colors";
            dot.setAttribute("aria-label", `Go to brand group ${index + 1}`);
            dot.addEventListener("click", () => scrollToPage(index));
            pagination.appendChild(dot);
            return dot;
        });
    };

    const updateDots = () => {
        if (!dots.length) return;
        const activePage = clamp(getCurrentPage(), 0, dots.length - 1);
        dots.forEach((dot, index) => {
            const isActive = index === activePage;
            dot.classList.toggle("bg-primary", isActive);
            dot.classList.toggle("bg-zinc-300", !isActive);
            dot.setAttribute("aria-current", isActive ? "true" : "false");
        });
    };

    const updateNavState = () => {
        const maxScroll = getMaxScroll();
        const hasCarouselPages = getPageCount() > 1;
        if (!hasCarouselPages || maxScroll <= 4) {
            if (prevButton) prevButton.style.display = "none";
            if (nextButton) nextButton.style.display = "none";
            return;
        }
        if (prevButton) prevButton.style.display = "";
        if (nextButton) nextButton.style.display = "";

        const atStart = track.scrollLeft <= 4;
        const atEnd = track.scrollLeft >= maxScroll - 4;
        if (prevButton) prevButton.style.display = atStart ? "none" : "";
        if (nextButton) nextButton.style.display = atEnd ? "none" : "";
        prevButton?.toggleAttribute("disabled", atStart);
        nextButton?.toggleAttribute("disabled", atEnd);
    };

    prevButton?.addEventListener("click", () => scrollToPage(getCurrentPage() - 1));
    nextButton?.addEventListener("click", () => scrollToPage(getCurrentPage() + 1));

    track.addEventListener("scroll", () => {
        updateDots();
        updateNavState();
    }, { passive: true });

    window.addEventListener("resize", () => {
        renderDots();
        updateDots();
        updateNavState();
    });

    renderDots();
    updateDots();
    updateNavState();
})();

(() => {
    const productCarousel = document.querySelector("[data-product-carousel]");
    if (!productCarousel) return;

    const track = productCarousel.querySelector("[data-product-track]");
    const prevButton = productCarousel.querySelector("[data-product-prev]");
    const nextButton = productCarousel.querySelector("[data-product-next]");
    const pagination = productCarousel.closest("section")?.querySelector("[data-product-pagination]");

    if (!track) return;

    const getPageWidth = () => track.clientWidth;
    const getMaxScroll = () => Math.max(track.scrollWidth - track.clientWidth, 0);
    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
    const getPageCount = () => {
        const width = getPageWidth();
        const maxScroll = getMaxScroll();
        if (!width) return 1;
        return Math.max(1, Math.ceil(maxScroll / width) + 1);
    };
    let dots = [];

    const getCurrentPage = () => {
        const width = getPageWidth();
        if (!width) return 0;
        return Math.round(track.scrollLeft / width);
    };

    const scrollToPage = (pageIndex) => {
        const width = getPageWidth();
        const maxScroll = getMaxScroll();
        if (!width || maxScroll <= 0) return;

        const target = clamp(pageIndex * width, 0, maxScroll);
        track.scrollTo({ left: target, behavior: "smooth" });
    };

    const renderDots = () => {
        if (!pagination) return;

        pagination.innerHTML = "";
        const pageCount = getPageCount();
        if (pageCount <= 1) {
            pagination.classList.add("hidden");
            dots = [];
            return;
        }

        pagination.classList.remove("hidden");
        dots = Array.from({ length: pageCount }, (_, index) => {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.className = "w-2 h-2 rounded-full bg-zinc-300 transition-colors";
            dot.setAttribute("aria-label", `Go to product group ${index + 1}`);
            dot.addEventListener("click", () => scrollToPage(index));
            pagination.appendChild(dot);
            return dot;
        });
    };

    const updateDots = () => {
        if (!dots.length) return;
        const activePage = clamp(getCurrentPage(), 0, dots.length - 1);
        dots.forEach((dot, index) => {
            const isActive = index === activePage;
            dot.classList.toggle("bg-primary", isActive);
            dot.classList.toggle("bg-zinc-300", !isActive);
            dot.setAttribute("aria-current", isActive ? "true" : "false");
        });
    };

    const updateNavState = () => {
        const maxScroll = getMaxScroll();
        const hasCarouselPages = getPageCount() > 1;
        if (!hasCarouselPages || maxScroll <= 4) {
            if (prevButton) prevButton.style.display = "none";
            if (nextButton) nextButton.style.display = "none";
            return;
        }
        if (prevButton) prevButton.style.display = "";
        if (nextButton) nextButton.style.display = "";

        const atStart = track.scrollLeft <= 4;
        const atEnd = track.scrollLeft >= maxScroll - 4;
        if (prevButton) prevButton.style.display = atStart ? "none" : "";
        if (nextButton) nextButton.style.display = atEnd ? "none" : "";
        prevButton?.toggleAttribute("disabled", atStart);
        nextButton?.toggleAttribute("disabled", atEnd);
    };

    prevButton?.addEventListener("click", () => scrollToPage(getCurrentPage() - 1));
    nextButton?.addEventListener("click", () => scrollToPage(getCurrentPage() + 1));

    track.addEventListener("scroll", () => {
        updateDots();
        updateNavState();
    }, { passive: true });

    window.addEventListener("resize", () => {
        renderDots();
        updateDots();
        updateNavState();
    });

    renderDots();
    updateDots();
    updateNavState();
})();

(() => {
    const openButton = document.getElementById("store-filter-open");
    const closeButton = document.getElementById("store-filter-close");
    const drawer = document.getElementById("store-filter-drawer");
    const overlay = document.getElementById("store-filter-overlay");
    const desktopMedia = window.matchMedia("(min-width: 1024px)");

    if (!openButton || !closeButton || !drawer || !overlay) return;

    const openDrawer = () => {
        drawer.classList.remove("-translate-x-full");
        overlay.classList.remove("opacity-0", "pointer-events-none");
        overlay.classList.add("opacity-100");
        drawer.setAttribute("aria-hidden", "false");
        openButton.setAttribute("aria-expanded", "true");
    };

    const closeDrawer = () => {
        drawer.classList.add("-translate-x-full");
        overlay.classList.add("opacity-0", "pointer-events-none");
        overlay.classList.remove("opacity-100");
        drawer.setAttribute("aria-hidden", "true");
        openButton.setAttribute("aria-expanded", "false");
    };

    openButton.addEventListener("click", openDrawer);
    closeButton.addEventListener("click", closeDrawer);
    overlay.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") closeDrawer();
    });

    const syncResponsiveState = () => {
        if (desktopMedia.matches) {
            overlay.classList.add("opacity-0", "pointer-events-none");
            overlay.classList.remove("opacity-100");
            drawer.setAttribute("aria-hidden", "false");
            openButton.setAttribute("aria-expanded", "false");
            return;
        }
        closeDrawer();
    };

    desktopMedia.addEventListener("change", syncResponsiveState);
    syncResponsiveState();
})();
