# Generated by Django 2.1 on 2019-09-15 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='financecategory',
            name='color',
            field=models.CharField(max_length=7, null=True),
        ),
    ]