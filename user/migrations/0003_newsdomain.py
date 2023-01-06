# Generated by Django 4.1.3 on 2023-01-06 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_newspreference"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsDomain",
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
                ("domain_name", models.CharField(max_length=255)),
                ("domain_source", models.TextField(max_length=1000)),
                ("domain_link", models.TextField(max_length=1000)),
                ("domain_image", models.TextField(max_length=1000)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
