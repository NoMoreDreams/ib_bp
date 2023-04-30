# Generated by Django 4.2 on 2023-04-27 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iban', models.CharField(max_length=24)),
                ('balance', models.FloatField(default=100000)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('information', models.TextField(null=True)),
                ('variable_symbol', models.CharField(max_length=100, null=True)),
                ('specific_symbol', models.CharField(max_length=100, null=True)),
                ('constant_symbol', models.CharField(max_length=100, null=True)),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiary_transaction_set', to='banking.account')),
                ('payer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='payer_transaction_set', to='banking.account')),
            ],
        ),
    ]
