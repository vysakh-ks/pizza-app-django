# Generated by Django 4.2.7 on 2023-11-04 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('pizza_name', models.CharField(max_length=100)),
                ('pizza_desc', models.TextField()),
                ('pizza_price', models.FloatField()),
                ('image_url', models.URLField(default='')),
            ],
        ),
    ]
