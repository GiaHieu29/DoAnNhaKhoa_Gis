"""
Django settings for dental_project project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-qn$+*n2o6r^=u9zk7d*=ob-3!=*=b1k27btzswa+xfi#@9+0#v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 1. Thêm 'jazzmin' lên TRÊN CÙNG để nó thay đổi giao diện Admin
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "nhakhoa", 
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dental_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "dental_project.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# 2. Chuyển sang Tiếng Việt và Giờ Việt Nam
LANGUAGE_CODE = "vi"  # Tiếng Việt

TIME_ZONE = "Asia/Ho_Chi_Minh" # Giờ Việt Nam

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Cấu hình Media (Dành cho việc upload ảnh sau này)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================
# 3. CẤU HÌNH GIAO DIỆN JAZZMIN (ADMIN ĐẸP)
# ==============================================
JAZZMIN_SETTINGS = {
    # Tiêu đề tab trình duyệt
    "site_title": "Quản Trị Nha Khoa Smile",
    
    # Tiêu đề ở màn hình đăng nhập
    "site_header": "Hệ Thống Quản Trị",
    
    # Logo chữ ở góc trái menu
    "site_brand": "Nha Khoa Admin",
    
    # Thông báo chào mừng ở trang login
    "welcome_sign": "Chào mừng bạn quay trở lại!",
    
    # Bản quyền ở chân trang
    "copyright": "Nha Khoa Smile Ltd",
    
    # Cho phép tìm kiếm User và Dịch vụ ngay trên thanh menu
    "search_model": ["auth.User", "nhakhoa.DichVu"],

    # Giao diện người dùng
    "show_ui_builder": True,  # Hiện nút chỉnh màu (góc phải màn hình) để bạn tự chọn màu thích
    
    # Menu bên trái
    "topmenu_links": [
        {"name": "Trang chủ", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Xem Website", "url": "/", "new_window": True},
    ],
    
    # Thay đổi icon cho các mục (Bạn có thể đổi icon khác tùy thích)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "nhakhoa.DichVu": "fas fa-tooth",       # Icon cái răng
        "nhakhoa.LichHen": "fas fa-calendar-check", # Icon lịch
    },
}

# Tùy chỉnh giao diện (Màu sắc mặc định)
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",   # Giao diện phẳng, hiện đại
    "dark_mode_theme": "darkly", # Giao diện tối (nếu bật dark mode)
}