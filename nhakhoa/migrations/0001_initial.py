import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChiNhanh",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ten_chi_nhanh",
                    models.CharField(max_length=200, verbose_name="Tên chi nhánh"),
                ),
                (
                    "dia_chi",
                    models.CharField(max_length=500, verbose_name="Địa chỉ hiển thị"),
                ),
                ("kinh_do", models.FloatField(verbose_name="Kinh độ (Longitude)")),
                ("vi_do", models.FloatField(verbose_name="Vĩ độ (Latitude)")),
                (
                    "link_google_map",
                    models.TextField(verbose_name="Link Embed Map (Iframe)"),
                ),
            ],
            options={
                "verbose_name": "Chi nhánh (GIS)",
                "verbose_name_plural": "2. Quản lý Chi nhánh & Tọa độ",
            },
        ),
        migrations.CreateModel(
            name="DichVu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ten_dich_vu",
                    models.CharField(max_length=200, verbose_name="Tên dịch vụ"),
                ),
                ("mo_ta", models.TextField(verbose_name="Mô tả ngắn")),
                ("gia", models.CharField(max_length=100, verbose_name="Giá tiền")),
                (
                    "link_anh",
                    models.CharField(
                        default="images/niengrang.jpg",
                        max_length=500,
                        verbose_name="Link ảnh (static)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Dịch vụ",
                "verbose_name_plural": "1. Quản lý Dịch vụ",
            },
        ),
        migrations.CreateModel(
            name="LichHen",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ho_ten",
                    models.CharField(max_length=100, verbose_name="Tên khách hàng"),
                ),
                (
                    "so_dien_thoai",
                    models.CharField(max_length=15, verbose_name="Số điện thoại"),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name="Email"
                    ),
                ),
                (
                    "ngay_hen_mong_muon",
                    models.DateField(
                        blank=True, null=True, verbose_name="Ngày khách chọn"
                    ),
                ),
                (
                    "noi_dung",
                    models.TextField(blank=True, verbose_name="Ghi chú / Tình trạng"),
                ),
                (
                    "thoi_gian_tao",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Thời gian gửi"
                    ),
                ),
                (
                    "trang_thai",
                    models.CharField(
                        choices=[
                            ("cho_xac_nhan", "Chờ xác nhận"),
                            ("da_xac_nhan", "Đã xác nhận"),
                            ("hoan_thanh", "Đã khám xong"),
                            ("huy", "Đã hủy"),
                        ],
                        default="cho_xac_nhan",
                        max_length=20,
                        verbose_name="Trạng thái",
                    ),
                ),
                (
                    "tong_tien",
                    models.DecimalField(
                        decimal_places=0,
                        default=0,
                        max_digits=12,
                        verbose_name="Thực thu (VNĐ)",
                    ),
                ),
                (
                    "chi_nhanh",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nhakhoa.chinhanh",
                        verbose_name="Chi nhánh đăng ký",
                    ),
                ),
                (
                    "dich_vu",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nhakhoa.dichvu",
                        verbose_name="Dịch vụ quan tâm",
                    ),
                ),
            ],
            options={
                "verbose_name": "Lịch Hẹn",
                "verbose_name_plural": "3. Quản lý Lịch Hẹn",
                "ordering": ["-thoi_gian_tao"],
            },
        ),
    ]
