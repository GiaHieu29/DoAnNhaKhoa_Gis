from django.contrib import admin
from .models import DichVu, ChiNhanh,  LichHen
@admin.register(DichVu)
class DichVuAdmin(admin.ModelAdmin):
    list_display = ('ten_dich_vu', 'gia', 'link_anh')
    search_fields = ('ten_dich_vu',)
@admin.register(ChiNhanh)
class ChiNhanhAdmin(admin.ModelAdmin):
    list_display = ('ten_chi_nhanh', 'kinh_do', 'vi_do', 'dia_chi')
@admin.register(LichHen)
class LichHenAdmin(admin.ModelAdmin):
    list_display = ('ho_ten', 'so_dien_thoai', 'chi_nhanh', 'dich_vu', 'ngay_hen_mong_muon', 'trang_thai', 'tong_tien')
    list_filter = ('trang_thai', 'chi_nhanh', 'ngay_hen_mong_muon', 'thoi_gian_tao')
    search_fields = ('ho_ten', 'so_dien_thoai', 'email')
    list_editable = ('trang_thai', 'tong_tien')
    ordering = ('-thoi_gian_tao',)