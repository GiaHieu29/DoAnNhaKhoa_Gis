from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nhakhoa", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chinhanh",
            name="so_dien_thoai",
            field=models.CharField(
                default="0909.xxx.xxx", max_length=20, verbose_name="Hotline"
            ),
        ),
        migrations.AlterField(
            model_name="chinhanh",
            name="kinh_do",
            field=models.CharField(
                help_text="Ví dụ: 106.660172 (Số thứ 2 khi click chuột phải trên Google Map)",
                max_length=50,
                verbose_name="Kinh độ (Longitude)",
            ),
        ),
        migrations.AlterField(
            model_name="chinhanh",
            name="link_google_map",
            field=models.TextField(
                help_text="Link trong thẻ src='...' khi chọn Chia sẻ -> Nhúng bản đồ",
                verbose_name="Link Embed Map (Iframe)",
            ),
        ),
        migrations.AlterField(
            model_name="chinhanh",
            name="vi_do",
            field=models.CharField(
                help_text="Ví dụ: 10.762622 (Số thứ 1 khi click chuột phải trên Google Map)",
                max_length=50,
                verbose_name="Vĩ độ (Latitude)",
            ),
        ),
    ]
