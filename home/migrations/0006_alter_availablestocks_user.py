# Generated by Django 4.0.4 on 2022-04-27 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_history_availablestocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availablestocks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.stockuser'),
        ),
    ]
