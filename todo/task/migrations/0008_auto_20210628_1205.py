# Generated by Django 2.1.15 on 2021-06-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_auto_20210622_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='<small>Can be added by the Django administration panel</small>', to='task.Tag'),
        ),
    ]