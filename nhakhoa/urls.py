from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('gioi-thieu/', views.gioithieu, name='gioithieu'),
    path('dich-vu/', views.dichvu, name='dichvu'),
    path('chi-nhanh/', views.chinhanh, name='chinhanh'),
    path('lien-he/', views.lienhe, name='lienhe'),
    path('dang-ky/', views.dangky, name='dangky'),
    path('dang-nhap/', views.dangnhap, name='dangnhap'),
    path('dang-xuat/', views.dangxuat, name='dangxuat'),
    path('dat-lich-hen/', views.dat_lich, name='dat_lich'),
    path('lich-su/', views.lich_su, name='lich_su'),
    path('xac-nhan-dat-lich/<int:id_lich_hen>/', views.xac_nhan_lich_hen, name='xac_nhan_lich_hen'),
    path('ban-do-so/', views.ban_do_so, name='ban_do_so'),
]
