// static/JS/base.js

document.addEventListener('DOMContentLoaded', () => {

    // =========================================================================
    // ۱. افکت پیشرفته محو شدن تدریجی تصویر پس‌زمینه تیم در اسکرول (Parallax Fade)
    // =========================================================================
    const heroBackdrop = document.getElementById('heroTeamBackdrop');
    const heroSection = document.getElementById('heroSection');

    if (heroBackdrop && heroSection) {
        let isTicking = false;

        const updateBackdropOnScroll = () => {
            const scrollY = window.pageYOffset || document.documentElement.scrollTop;
            const heroHeight = heroSection.offsetHeight;

            // فقط تا زمانی که هیرو در دید است محاسبه انجام شود
            if (scrollY <= heroHeight) {
                // با افزایش اسکرول، شفافیت از 0.45 به 0.05 کاهش می‌یابد
                const progress = scrollY / heroHeight;
                const newOpacity = Math.max(0.04, 0.45 - (progress * 0.42));
                const newScale = 1.02 + (progress * 0.08); // افکت زوم نرم هم‌زمان

                heroBackdrop.style.opacity = newOpacity;
                heroBackdrop.style.transform = `scale(${newScale}) translateY(${scrollY * 0.25}px)`;
            }

            isTicking = false;
        };

        window.addEventListener('scroll', () => {
            if (!isTicking) {
                window.requestAnimationFrame(updateBackdropOnScroll);
                isTicking = true;
            }
        }, { passive: true });
    }

    // =========================================================================
    // ۲. منوی کشویی موبایل
    // =========================================================================
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            const isOpen = navLinks.classList.toggle('open');
            navToggle.setAttribute('aria-expanded', isOpen);
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });

        // بستن خودکار منو پس از کلیک روی هر لینک
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            });
        });
    }

    // =========================================================================
    // ۳. انیمیشن اسکرول عناصر (Scroll Reveal)
    // =========================================================================
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!prefersReducedMotion && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -50px 0px'
        });

        document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
    } else {
        document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('in-view'));
    }

    // =========================================================================
    // ۴. مدیریت پیام‌های سیستم (Toast Notifications)
    // =========================================================================
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach(toast => {
        const timer = setTimeout(() => {
            dismissToast(toast);
        }, 5000);

        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(timer);
                dismissToast(toast);
            });
        }
    });

    function dismissToast(toastEl) {
        toastEl.style.transition = 'opacity 0.3s, transform 0.3s';
        toastEl.style.opacity = '0';
        toastEl.style.transform = 'translateY(-20px)';
        setTimeout(() => toastEl.remove(), 300);
    }

});