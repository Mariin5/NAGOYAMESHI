#調べること１：Choicesのモデルのつくりかた
#調べること２：１対多のモデルの作り方
#考えること１：他に必要なモデルがないかどうか
from django.db import models 

from django.utils import timezone 
from django.core.validators import RegexValidator

# ユーザーモデルを読み込みする(1対多)
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    # 和食、洋食、中華、エスニック、メニューの種類
    category_choice = [
        ("和食","和食"),
        ("洋食","洋食"),
        ("中華","中華"),
        ("エスニック","エスニック"),
        ("イタリアン","イタリアン"),
        ("フレンチ","フレンチ"),
        ("居酒屋","居酒屋"),
        ("カフェ・喫茶店","カフェ・喫茶店"),
        ("ファストフード","ファストフード"),
        ("焼肉","焼肉"),
        ("うどん・そば","うどん・そば"),
        ("ラーメン","ラーメン"),
        ("その他","その他"),
    ]
    category        = models.CharField(verbose_name="カテゴリ名", max_length=15 ,choices=category_choice)
    created_at  = models.DateTimeField(verbose_name="登録日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.category

class Area(models.Model):
    # 1対多 は選択肢の増減が考えられる場合に有効。
    # TODO: 名古屋の市町村データを前もって初期データとして用意しておく。
    area_choice = [
            ('中心部', '中心部'),
            ('東部', '東部'),
            ('西部', '西部'),
            ('南部', '南部'),
            ('北部', '北部'),
        ]
    area        = models.CharField(verbose_name="エリア名", max_length=5, choices=area_choice)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.area

class Paymethod(models.Model):
    # 現金、カード(Visa、MasterCard)、電子マネー(PayPayなど)
    paymethod_choice = [
        ("現金","現金"),
        ("クレジットカード","クレジットカード"),
        ("交通系ICカード","交通系ICカード"),
        ("電子マネー","電子マネー"),
    ]
    paymethod       = models.CharField(verbose_name="支払い方法", max_length=15, choices=paymethod_choice)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.paymethod

class Holiday(models.Model):
    # choices；事前に選択肢を用意し選ばせる
    # https://noauto-nolife.com/post/django-models-choices/
    holidays_choice = [
        ("月曜日","月曜日"),
        ("火曜日","火曜日"),
        ("水曜日","水曜日"),
        ("木曜日","木曜日"),
        ("金曜日","金曜日"),
        ("土曜日","土曜日"),
        ("日曜日","日曜日"),
    ]
    holiday         = models.CharField(verbose_name="定休日", choices=holidays_choice)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.holiday

class Restaurant(models.Model):
    category        = models.ManyToManyField(Category, verbose_name="カテゴリ")
    name            = models.CharField(verbose_name="店舗名", max_length=100)
    name_kana       = models.CharField(verbose_name="店舗名フリガナ", max_length=100)
    image           = models.ImageField(verbose_name="店舗画像", upload_to="nagoyameshi/restaurant/image/")
    introduction    = models.CharField(verbose_name="店舗紹介文", max_length=100)
    post_code_regex = RegexValidator(regex=r'^\d{3}-\d{4}$')
    # validators：追加のバリデーションの指定
    post_code       = models.CharField(verbose_name="郵便番号", max_length=8 , validators=[post_code_regex])
    address         = models.CharField(verbose_name="住所", max_length=100)
    holiday         =models.ManyToManyField(Holiday, verbose_name="定休日")
    # 携帯電話番号であれば11桁、固定回線の場合は10桁 混乱を招くためハイフンを除外する。
    tel_regex       = RegexValidator(regex=r'^\d{10,11}$')
    tel             = models.CharField(verbose_name="電話番号", max_length=11, validators=[tel_regex])
    email           = models.EmailField(verbose_name="メールアドレス",blank=True)
    paymethod       = models.ManyToManyField(Paymethod, verbose_name="支払い方法")
    # TrueもしくはFalse
    has_parking     = models.BooleanField(verbose_name="駐車場の有無")
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)


class Review(models.Model):
    user        = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)
    restaurant  = models.ForeignKey(Restaurant, verbose_name="店舗", on_delete=models.CASCADE)
    subject     = models.CharField(verbose_name="件名", max_length=100)
    content     = models.CharField(verbose_name="内容", max_length=1000)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)

    
class Reservation(models.Model):
    user            = models.ForeignKey(User, verbose_name="予約者", on_delete=models.CASCADE)
    restaurant      = models.ForeignKey(Restaurant, verbose_name="店舗", on_delete=models.CASCADE)
    scheduled_date  = models.DateTimeField(verbose_name="予約日")
    # 人数はマイナスにならないのでPostiveIntegerField
    headcount       = models.PositiveIntegerField(verbose_name="人数")
    # アレルギー、車椅子、盲導犬など
    note            = models.CharField(verbose_name="備考", max_length=100,blank=True)
    


# もしサイトの運営者情報を表示する場合、複数投稿できる中でどのようにして表示するかを考慮しておく
# ↑ created_at で最新のCompanyを取り出し、.first() で最新の1件を取り出す。
class Company(models.Model):
    name            = models.CharField(verbose_name="会社名", max_length=100)
    name_kana       = models.CharField(verbose_name="会社名フリガナ", max_length=100)
    ceo             = models.CharField(verbose_name="代表者名", max_length=30)
    founding_date   = models.DateField(verbose_name="設立日")
    capital         = models.PositiveIntegerField(verbose_name="資本金(万円)")
    activity        = models.CharField(verbose_name="事業内容", max_length=300)
    post_code_regex = RegexValidator(regex=r'^\d{3}-\d{4}$')
    post_code       = models.CharField(verbose_name="郵便番号", max_length=8 , validators=post_code_regex)
    # 携帯電話番号であれば11桁、固定回線の場合は10桁 混乱を招くためハイフンを除外
    tel_regex       = RegexValidator(regex=r'^\d{10,11}$')
    tel             = models.CharField(verbose_name="電話番号", max_length=11, validators=[tel_regex])
    email           = models.EmailField(verbose_name="メールアドレス")
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)
