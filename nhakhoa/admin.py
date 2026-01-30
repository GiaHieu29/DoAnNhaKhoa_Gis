from django.contrib import admin
from .models import DichVu, ChiNhanh,  LichHen

# 1. Admin cho Dịch vụ
@admin.register(DichVu)
class DichVuAdmin(admin.ModelAdmin):
    list_display = ('ten_dich_vu', 'gia', 'link_anh')
    search_fields = ('ten_dich_vu',)
# Đăng ký bảng GIS
@admin.register(ChiNhanh)
class ChiNhanhAdmin(admin.ModelAdmin):
    list_display = ('ten_chi_nhanh', 'kinh_do', 'vi_do', 'dia_chi')
# 2. Admin cho Lịch Hẹn (ĐÃ SỬA LỖI)
@admin.register(LichHen)
class LichHenAdmin(admin.ModelAdmin):
    # Thay 'ngay_hen' cũ bằng các cột mới: chi_nhanh, ngay_hen_mong_muon
    list_display = ('ho_ten', 'so_dien_thoai', 'chi_nhanh', 'dich_vu', 'ngay_hen_mong_muon', 'trang_thai', 'tong_tien')
    
    # Bộ lọc: Thêm lọc theo chi nhánh và ngày tạo
    list_filter = ('trang_thai', 'chi_nhanh', 'ngay_hen_mong_muon', 'thoi_gian_tao')
    
    # Tìm kiếm: Thêm tìm theo Email
    search_fields = ('ho_ten', 'so_dien_thoai', 'email')
    
    # Cho phép sửa nhanh trạng thái và tiền ngay bên ngoài
    list_editable = ('trang_thai', 'tong_tien')

    # Sắp xếp: Đưa đơn mới nhất (theo thời gian tạo) lên đầu
    ordering = ('-thoi_gian_tao',)