# Generated by Django 2.1 on 2019-09-22 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_financecategory_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactioncategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='transactioncategory',
            name='transaction',
        ),
        migrations.AddField(
            model_name='transaction',
            name='categories',
            field=models.ManyToManyField(to='finance.FinanceCategory'),
        ),
        migrations.DeleteModel(
            name='TransactionCategory',
        ),
    ]
