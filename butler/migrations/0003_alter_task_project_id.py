# Generated by Django 5.1.3 on 2024-11-09 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butler', '0002_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='butler.project'),
        ),
    ]
