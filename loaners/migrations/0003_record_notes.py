# Generated by Django 2.1.11 on 2020-04-12 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loaners', '0002_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='notes',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
