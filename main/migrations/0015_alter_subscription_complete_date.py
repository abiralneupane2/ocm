# Generated by Django 3.2.7 on 2021-10-01 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_week_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='complete_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
