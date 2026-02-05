from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nhakhoa", "0002_chinhanh_so_dien_thoai_alter_chinhanh_kinh_do_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chinhanh",
            name="link_google_map",
        ),
    ]
