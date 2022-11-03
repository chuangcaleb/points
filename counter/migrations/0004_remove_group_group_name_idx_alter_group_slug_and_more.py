# Generated by Django 4.0 on 2022-11-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0003_alter_event_id_alter_group_id'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='group',
            name='group_name_idx',
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(max_length=64, null=True, verbose_name='slug'),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together={('event', 'slug')},
        ),
    ]