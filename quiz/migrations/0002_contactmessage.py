# Generated by Django 5.1.7 on 2025-03-23 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Imię')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('message', models.TextField(verbose_name='Wiadomość')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data wysłania')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Przetworzone')),
            ],
            options={
                'verbose_name': 'Wiadomość kontaktowa',
                'verbose_name_plural': 'Wiadomości kontaktowe',
                'ordering': ['-created_at'],
            },
        ),
    ]
