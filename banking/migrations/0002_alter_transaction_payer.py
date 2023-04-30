# Generated by Django 4.2 on 2023-04-27 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer_transaction_set', to='banking.account'),
        ),
    ]
