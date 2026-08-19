// static/js/register_course.js

document.addEventListener('DOMContentLoaded', () => {
    const formSteps = document.querySelectorAll('.form-step');
    const progressSteps = document.querySelectorAll('.step-progressbar li');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const submitBtn = document.getElementById('submitBtn');

    let currentStep = 0;

    // تابع برای به‌روزرسانی و نمایش مرحله فعال
    function updateFormSteps() {
        formSteps.forEach((step, index) => {
            if (index === currentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // به‌روزرسانی نوار پیشرفت (خط زمانی)
        progressSteps.forEach((step, index) => {
            if (index <= currentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // مدیریت نمایش دکمه قبلی
        if (currentStep === 0) {
            prevBtn.style.visibility = 'hidden';
        } else {
            prevBtn.style.visibility = 'visible';
        }

        // مدیریت دکمه‌های بعدی و ثبت نهایی
        if (currentStep === formSteps.length - 1) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'inline-flex';
        } else {
            nextBtn.style.display = 'inline-flex';
            submitBtn.style.display = 'none';
        }
    }

    // رویداد کلیک دکمه بعدی
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            // یک اعتبارسنجی اولیه فرانت‌اند (اختیاری برای بهبود کارایی)
            const currentStepFields = formSteps[currentStep].querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;

            // چک کردن اینکه فیلدهای اجباری مرحله فعلی خالی نباشند


            if (isValid) {
                if (currentStep < formSteps.length - 1) {
                    currentStep++;
                    updateFormSteps();
                    // اسکرول نرم صفحه به بالای فرم جهت راحتی کار کاربران
                    window.scrollTo({ top: 100, behavior: 'smooth' });
                }
            } else {
                alert('لطفاً ابتدا تمام فیلدهای الزامی این مرحله را پر کنید.');
            }
        });
    }

    // رویداد کلیک دکمه قبلی
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                updateFormSteps();
                window.scrollTo({ top: 100, behavior: 'smooth' });
            }
        });
    }
});