# Generated by Django 5.0 on 2024-01-04 12:55

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(choices=[('中心部', '中心部'), ('東部', '東部'), ('西部', '西部'), ('南部', '南部'), ('北部', '北部')], max_length=5, unique=True, verbose_name='エリア名')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('和食', '和食'), ('洋食', '洋食'), ('中華', '中華'), ('エスニック', 'エスニック'), ('イタリアン', 'イタリアン'), ('フレンチ', 'フレンチ'), ('居酒屋', '居酒屋'), ('カフェ・喫茶店', 'カフェ・喫茶店'), ('ファストフード', 'ファストフード'), ('焼肉', '焼肉'), ('うどん・そば', 'うどん・そば'), ('ラーメン', 'ラーメン'), ('その他', 'その他')], max_length=15, unique=True, verbose_name='カテゴリ名')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='会社名')),
                ('name_kana', models.CharField(max_length=100, verbose_name='会社名フリガナ')),
                ('ceo', models.CharField(max_length=30, verbose_name='代表者名')),
                ('founding_date', models.DateField(verbose_name='設立日')),
                ('capital', models.PositiveIntegerField(verbose_name='資本金(万円)')),
                ('activity', models.CharField(max_length=300, verbose_name='事業内容')),
                ('post_code', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(regex='^\\d{3}-\\d{4}$')], verbose_name='郵便番号')),
                ('tel', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(regex='^\\d{10,11}$')], verbose_name='電話番号')),
                ('email', models.EmailField(max_length=254, verbose_name='メールアドレス')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday', models.CharField(blank=True, choices=[('月曜日', '月曜日'), ('火曜日', '火曜日'), ('水曜日', '水曜日'), ('木曜日', '木曜日'), ('金曜日', '金曜日'), ('土曜日', '土曜日'), ('日曜日', '日曜日')], max_length=5, unique=True, verbose_name='定休日')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='PayMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymethod', models.CharField(choices=[('現金', '現金'), ('クレジットカード', 'クレジットカード'), ('交通系ICカード', '交通系ICカード'), ('電子マネー', '電子マネー')], max_length=15, unique=True, verbose_name='支払い方法')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='店舗名')),
                ('name_kana', models.CharField(max_length=100, verbose_name='店舗名フリガナ')),
                ('image', models.ImageField(upload_to='nagoyameshi/restaurant/image/', verbose_name='店舗画像')),
                ('introduction', models.CharField(max_length=100, verbose_name='店舗紹介文')),
                ('post_code', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(regex='^\\d{3}-\\d{4}$')], verbose_name='郵便番号')),
                ('address', models.CharField(max_length=100, verbose_name='住所')),
                ('tel', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(regex='^\\d{10,11}$')], verbose_name='電話番号')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='メールアドレス')),
                ('has_parking', models.BooleanField(verbose_name='駐車場の有無')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('category', models.ManyToManyField(to='nagoyameshi.category', verbose_name='カテゴリ')),
                ('holiday', models.ManyToManyField(to='nagoyameshi.holiday', verbose_name='定休日')),
                ('paymethod', models.ManyToManyField(to='nagoyameshi.paymethod', verbose_name='支払い方法')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateTimeField(verbose_name='予約日')),
                ('headcount', models.PositiveIntegerField(verbose_name='人数')),
                ('note', models.CharField(blank=True, max_length=100, verbose_name='備考')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='予約者')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nagoyameshi.restaurant', verbose_name='店舗')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='件名')),
                ('content', models.CharField(max_length=1000, verbose_name='内容')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nagoyameshi.restaurant', verbose_name='店舗')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
    ]
