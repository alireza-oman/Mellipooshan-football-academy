// static/js/profile.js

document.addEventListener('DOMContentLoaded', () => {
    const avatarInput = document.getElementById('avatar-input');
    const avatarPreview = document.getElementById('avatar-preview');
    const uploadTrigger = document.getElementById('upload-trigger');

    // وقتی روی دکمه فرعی کلیک شد، فیلد فایل اصلی را تحریک کند
    if (uploadTrigger && avatarInput) {
        uploadTrigger.addEventListener('click', () => {
            avatarInput.click();
        });
    }

    // پیش‌نمایش تصویر انتخابی کاربر قبل از آپلود
    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});