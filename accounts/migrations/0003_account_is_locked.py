# Generated by Django 4.2.16 on 2024-12-02 21:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_account_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="is_locked",
            field=models.BooleanField(default=False),
        ),
    ]
