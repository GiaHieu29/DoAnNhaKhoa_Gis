from django.db import models
from django.utils import timezone

# 1. MODEL DỊCH VỤ (Giữ nguyên)
class DichVu(models.Model):
    ten_dich_vu = models.CharField(max_length=200, verbose_name="Tên dịch vụ")
    mo_ta = models.TextField(verbose_name="Mô tả ngắn")
    gia = models.CharField(max_length=100, verbose_name="Giá tiền")
    link_anh = models.CharField(max_length=500, default="images/niengrang.jpg", verbose_name="Link ảnh (static)")

    def __str__(self):
        return self.ten_dich_vu
    class Meta:
        verbose_name = "Dịch vụ"
        verbose_name_plural = "1. Quản lý Dịch vụ"

# 2. MODEL CHI NHÁNH (Đây là phần GIS - QUAN TRỌNG)
class ChiNhanh(models.Model):
    ten_chi_nhanh = models.CharField(max_length=200, verbose_name="Tên chi nhánh")
    dia_chi = models.CharField(max_length=500, verbose_name="Địa chỉ hiển thị")
    
    # --- TRƯỜNG DỮ LIỆU GIS (TỌA ĐỘ) ---
    kinh_do = models.FloatField(verbose_name="Kinh độ (Longitude)")  # Ví dụ: 106.653...
    vi_do = models.FloatField(verbose_name="Vĩ độ (Latitude)")       # Ví dụ: 10.790...
    
    link_google_map = models.TextField(verbose_name="Link Embed Map (Iframe)")

    def __str__(self):
        return self.ten_chi_nhanh
    class Meta:
        verbose_name = "Chi nhánh (GIS)"
        verbose_name_plural = "2. Quản lý Chi nhánh & Tọa độ"

# 3. MODEL LỊCH HẸN (Sửa lại để liên kết với Chi Nhánh)
class LichHen(models.Model):
    TRANG_THAI_CHOICES = [
        ('cho_xac_nhan', 'Chờ xác nhận'),
        ('da_xac_nhan', 'Đã xác nhận'),
        ('hoan_thanh', 'Đã khám xong'),
        ('huy', 'Đã hủy'),
    ]

    ho_ten = models.CharField(max_length=100, verbose_name="Tên khách hàng")
    so_dien_thoai = models.CharField(max_length=15, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    
    # Thay vì lưu text, ta liên kết khóa ngoại với bảng ChiNhanh để lấy tọa độ
    chi_nhanh = models.ForeignKey(ChiNhanh, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Chi nhánh đăng ký")
    
    dich_vu = models.ForeignKey(DichVu, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Dịch vụ quan tâm")
    ngay_hen_mong_muon = models.DateField(verbose_name="Ngày khách chọn", blank=True, null=True)
    noi_dung = models.TextField(blank=True, verbose_name="Ghi chú / Tình trạng")
    thoi_gian_tao = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian gửi")
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='cho_xac_nhan', verbose_name="Trạng thái")
    tong_tien = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Thực thu (VNĐ)")

    def __str__(self):
        return f"{self.ho_ten} - {self.so_dien_thoai}"

    class Meta:
        verbose_name = "Lịch Hẹn"
        verbose_name_plural = "3. Quản lý Lịch Hẹn"
        ordering = ['-thoi_gian_tao']