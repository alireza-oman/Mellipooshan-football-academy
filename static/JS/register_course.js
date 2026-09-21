// static/JS/register_course.js

document.addEventListener('DOMContentLoaded', () => {
    const pages = document.querySelectorAll('.form-step-page');
    const navItems = document.querySelectorAll('.step-nav-item');
    const progressBar = document.getElementById('stepperProgressBar');
    const nextBtn = document.getElementById('flipNextBtn');
    const prevBtn = document.getElementById('flipPrevBtn');
    const submitBtn = document.getElementById('finalSubmitBtn');

    let currentStep = 0;
    const totalSteps = pages.length;

    // تابع اصلی ورق زدن بین برگه‌ها
    function flipToStep(targetStep, direction = 'forward') {
        if (targetStep < 0 || targetStep >= totalSteps) return;

        const currentActivePage = pages[currentStep];
        const targetPage = pages[targetStep];

        // حذف کلاس‌های انیمیشن قبلی
        currentActivePage.classList.remove('active', 'flip-forward', 'flip-backward');

        // اعمال انیمیشن ورق زدن بر اساس جهت حرکت
        targetPage.classList.add('active');
        if (direction === 'forward') {
            targetPage.classList.add('flip-forward');
        } else {
            targetPage.classList.add('flip-backward');
        }

        currentStep = targetStep;

        // به‌روزرسانی نوار دایره‌های بالا
        navItems.forEach((item, idx) => {
            item.classList.toggle('active', idx === currentStep);
            item.classList.toggle('completed', idx < currentStep);
        });

        // به‌روزرسانی درصد نوار پیشرفت
        const percentage = ((currentStep + 1) / totalSteps) * 100;
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
        }

        // دکمه بازگشت (در صفحه اول مخفی است)
        if (prevBtn) {
            prevBtn.style.visibility = (currentStep === 0) ? 'hidden' : 'visible';
        }

        // در صفحه آخر دکمه Next تبدیل به دکمه Submit می‌شود
        if (currentStep === totalSteps - 1) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'inline-flex';
        } else {
            nextBtn.style.display = 'inline-flex';
            submitBtn.style.display = 'none';
        }

        // اسکرول نرم به بالای کادر در موبایل
        const cardBox = document.querySelector('.stepper-card-box');
        if (cardBox && window.innerWidth < 768) {
            cardBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // دکمه ورق زدن به بعد
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            if (currentStep < totalSteps - 1) {
                flipToStep(currentStep + 1, 'forward');
            }
        });
    }

    // دکمه ورق زدن به قبل
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentStep > 0) {
                flipToStep(currentStep - 1, 'backward');
            }
        });
    }

    // امکان کلیک مستقیم روی شماره‌های مرحله در بالای فرم جهت ورق زدن
    window.jumpToStep = function(targetIndex) {
        // کاربر فقط می‌تواند به مراحلی که قبلاً رفته یا مرحله فعلی بپرد
        if (targetIndex <= currentStep + 1 && targetIndex !== currentStep) {
            const dir = targetIndex > currentStep ? 'forward' : 'backward';
            flipToStep(targetIndex, dir);
        }
    };
});