// static/JS/profile.js

document.addEventListener('DOMContentLoaded', () => {
    const avatarInput = document.getElementById('avatar-input');
    const avatarPreview = document.getElementById('avatar-preview');
    const uploadTrigger = document.getElementById('upload-trigger');

    if (uploadTrigger && avatarInput) {
        uploadTrigger.addEventListener('click', () => {
            avatarInput.click();
        });
    }

    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;

            // اعتبارسنجی فرانت‌اند نوع فایل (جلوگیری از آپلود فایل نامعتبر)
            const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
            if (!allowedTypes.includes(file.type)) {
                alert('لطفاً فقط فایل‌های تصویری با فرمت JPG، PNG یا WEBP انتخاب کنید.');
                avatarInput.value = '';
                return;
            }

            // بررسی حداکثر حجم (۱۰ مگابایت)
            if (file.size > 10 * 1024 * 1024) {
                alert('حجم تصویر نباید بیشتر از ۱۰ مگابایت باشد.');
                avatarInput.value = '';
                return;
            }

            // پیش‌نمایش آنی
            const reader = new FileReader();
            reader.onload = (event) => {
                avatarPreview.src = event.target.result;
            };
            reader.readAsDataURL(file);
        });
    }
});