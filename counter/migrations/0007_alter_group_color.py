# Generated by Django 4.0.4 on 2022-10-04 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0006_event_heading_size_event_points_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='color',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
