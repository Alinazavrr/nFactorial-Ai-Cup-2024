# Generated by Django 4.2.13 on 2024-05-25 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.customuser'),
        ),
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.customuser'),
        ),
    ]
