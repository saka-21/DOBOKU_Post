# Generated by Django 3.0.3 on 2020-06-20 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0011_delete_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.Post', verbose_name='対象記事'),
        ),
    ]