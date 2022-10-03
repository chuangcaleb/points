# Generated by Django 4.0.4 on 2022-10-02 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0002_alter_pointshistory_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_group', to='counter.event'),
        ),
    ]