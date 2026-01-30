
from django.urls import path
from . import views

urlpatterns = [
    # 1. Các trang chính (Tên name='...' phải khớp với base.html)
    path('', views.index, name='index'),           # Trang chủ (Lưu ý: name='index')
    path('gioi-thieu/', views.gioithieu, name='gioithieu'),
    path('dich-vu/', views.dichvu, name='dichvu'),
    path('chi-nhanh/', views.chinhanh, name='chinhanh'),
    path('lien-he/', views.lienhe, name='lienhe'),

    # 2. Phần Tài khoản (Đăng ký/Nhập/Xuất)
    path('dang-ky/', views.dangky, name='dangky'),
    path('dang-nhap/', views.dangnhap, name='dangnhap'),
    path('dang-xuat/', views.dangxuat, name='dangxuat'),
    path('dat-lich-hen/', views.dat_lich, name='dat_lich'),
    path('lich-su/', views.lich_su, name='lich_su'),
    # Trong urlpatterns
path('xac-nhan-dat-lich/<int:id_lich_hen>/', views.xac_nhan_lich_hen, name='xac_nhan_lich_hen'),
]