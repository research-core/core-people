# Generated by Django 2.2.4 on 2019-08-06 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20190806_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='auth_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]