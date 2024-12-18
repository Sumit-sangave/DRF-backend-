# Generated by Django 5.1.2 on 2024-11-16 16:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0005_like_unique_user_product_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='text',
        ),
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='firstapp.product'),
        ),
        migrations.CreateModel(
            name='ProductLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_products', through='firstapp.ProductLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
