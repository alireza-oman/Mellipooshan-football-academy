// static/js/base.js

document.addEventListener('DOMContentLoaded', () => {

    // ===================================================
    // ۱. مدیریت منوی موبایل (با شرط محافظ برای جلوگیری از کرش)
    // ===================================================
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) { // 🌟 شرط ضربه‌گیر: فقط اگر المان‌ها در صفحه بودند اجرا شود
        navToggle.addEventListener('click', () => {
            const open = navLinks.classList.toggle('open');
            navToggle.setAttribute('aria-expanded', open);
        });

        navLinks.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', () => {
                navLinks.classList.remove('open');
                navToggle.setAttribute('aria-expanded', false);
            });
        });
    }

    // ===================================================
    // ۲. انیمیشن اسکرول صفحات عمومی (Scroll Reveal)
    // ===================================================
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduceMotion && 'IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('in-view');
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.15 });

        document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
    } else {
        document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('in-view'));
    }

    // ===================================================
    // ۳. مدیریت پیام‌های فلش (Toast Notifications)
    // ===================================================
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach(toast => {
        // بستن خودکار بعد از ۵ ثانیه
        const autoDismiss = setTimeout(() => {
            if (document.body.contains(toast)) {
                toast.classList.add('fade-out');
                setTimeout(() => toast.remove(), 400);
            }
        }, 5000);

        // بستن دستی با زدن دکمه ضربدر
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(autoDismiss); // لغو تایمر خودکار
                toast.classList.add('fade-out');
                setTimeout(() => toast.remove(), 400);
            });
        }
    });

});