# Generated by Django 4.1 on 2022-11-02 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bin_bank', '0002_supportmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bin_bank.myuser'),
        ),
    ]
