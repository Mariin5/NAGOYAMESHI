#調べること１：Choicesのモデルのつくりかた
#調べること２：１対多のモデルの作り方
#考えること１：他に必要なモデルがないかどうか
from django.db import models 

from django.utils import timezone 
from django.core.validators import RegexValidator,MinValueValidator,MaxValueValidator
import datetime
from django.core.exceptions import ValidationError
from django.db.models import Sum

# ユーザーモデルを読み込みする(1対多)
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    # 和食、洋食、中華、エスニック、メニューの種類
    category_choice =[
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
    category_name = models.CharField(verbose_name="カテゴリ名", max_length=15 ,choices=category_choice,unique=True)
    created_at  = models.DateTimeField(verbose_name="登録日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.category_name

class Area(models.Model):
    area_choice = [
            ('中心部', '中心部'),
            ('東部', '東部'),
            ('西部', '西部'),
            ('南部', '南部'),
            ('北部', '北部'),
            ('港', '港'),
        ]
    area        = models.CharField(verbose_name="エリア名", max_length=5, choices=area_choice,unique=True)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.area

class PayMethod(models.Model):
    paymethod_choice = [
        ("現金","現金"),
        ("クレジットカード","クレジットカード"),
        ("交通系ICカード","交通系ICカード"),
        ("電子マネー","電子マネー"),
    ]
    paymethod       = models.CharField(verbose_name="支払い方法", max_length=15, choices=paymethod_choice,unique=True)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.paymethod

class Holiday(models.Model):
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
    holiday         = models.CharField(verbose_name="定休日", max_length=5, choices=holidays_choice,unique=True,blank=True)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.holiday

class Restaurant(models.Model):
    category_name   = models.ManyToManyField(Category, verbose_name="カテゴリ")
    name            = models.CharField(verbose_name="店舗名", max_length=100)
    name_kana       = models.CharField(verbose_name="店舗名フリガナ", max_length=100)
    image           = models.ImageField(verbose_name="店舗画像", upload_to="nagoyameshi/restaurant/image/")
    introduction    = models.CharField(verbose_name="店舗紹介文", max_length=100)
    #PROTECT=関連するオブジェクトがあると削除できない
    area            = models.ForeignKey(Area,verbose_name="エリア",on_delete=models.PROTECT)
    post_code_regex = RegexValidator(regex=r'^\d{3}-\d{4}$')
    # validators：追加のバリデーションの指定
    post_code       = models.CharField(verbose_name="郵便番号", max_length=8 , validators=[post_code_regex])
    address         = models.CharField(verbose_name="住所", max_length=100)
    start_hour      = models.TimeField(verbose_name="営業開始時間",default=timezone.now)
    end_hour      = models.TimeField(verbose_name="営業終了時間",default=timezone.now)
    holiday         =models.ManyToManyField(Holiday, verbose_name="定休日")
    # 携帯電話番号であれば11桁、固定回線の場合は10桁 混乱を招くためハイフンを除外する。
    tel_regex       = RegexValidator(regex=r'^\d{10,11}$')
    tel             = models.CharField(verbose_name="電話番号", max_length=11, validators=[tel_regex])
    email           = models.EmailField(verbose_name="メールアドレス",blank=True)
    paymethod       = models.ManyToManyField(PayMethod, verbose_name="支払い方法")
    headcount       = models.PositiveIntegerField(verbose_name="最大予約可能人数",default=1) 
    # TrueもしくはFalse
    has_parking     = models.CharField(verbose_name="駐車場", max_length=100)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    MAX_STAR      = 5

    user        = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)
    restaurant  = models.ForeignKey(Restaurant, verbose_name="店舗", on_delete=models.CASCADE)
    star        = models.IntegerField(verbose_name="星",validators=[MinValueValidator(1),MaxValueValidator(MAX_STAR)],default=1)
    subject     = models.CharField(verbose_name="件名", max_length=100)
    content     = models.CharField(verbose_name="内容", max_length=1000)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)

    def star_icon(self):
        dic               = []
        dic["true_star"]  = self.star * ""
        dic["false_star"] = ( MAX_STAR - self.star) * ""

        return dic



class Favorite(models.Model):
    #同一ユーザーが複数回同じレストランをお気に入り登録できないように設定する（重複を防ぐ）
    class Meta:
        unique_together=("user","restaurant")

    user       = models.ForeignKey(User, verbose_name="登録者",on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, verbose_name="店舗",on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    


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
    post_code       = models.CharField(verbose_name="郵便番号", max_length=8 , validators=[post_code_regex])       
    # 携帯電話番号であれば11桁、固定回線の場合は10桁 混乱を招くためハイフンを除外
    tel_regex       = RegexValidator(regex=r'^\d{10,11}$')
    tel             = models.CharField(verbose_name="電話番号", max_length=11, validators=[tel_regex])
    email           = models.EmailField(verbose_name="メールアドレス")
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)


#予約締め切り日（24時間前)を超えていないかチェック
def scheduled_date_check(value):
    deadline = timezone.now() + datetime.timedelta(days=1)

    if deadline > value :
        raise ValidationError("予約可能日時を過ぎています")
    
    
class Reservation(models.Model):
    user            = models.ForeignKey(User, verbose_name="予約者", on_delete=models.CASCADE)
    restaurant      = models.ForeignKey(Restaurant, verbose_name="店舗", on_delete=models.CASCADE)
    scheduled_date  = models.DateTimeField(verbose_name="予約日",validators=[scheduled_date_check])
    # 人数はマイナスにならないのでPostiveIntegerField
    headcount       = models.PositiveIntegerField(verbose_name="人数")
    # アレルギー、車椅子、盲導犬など
    note            = models.CharField(verbose_name="備考", max_length=100,blank=True)

    #2つ以上のフィールドをバリデーションする場合
    def clean(self):
        super().clean()
    #予約人数確認
        restaurant = self.restaurant
        headcount  = self.headcount
        date       = self.scheduled_date 
    #希望予約日の予約人数状況確認
    #default=0 : 予約人数が0人だった場合に「0」と表示させる。この指定が無いとnoneになる
        result  = Reservation.objects.filter(scheduled_date__year=date.year,
                                             scheduled_date__month=date.month,
                                             scheduled_date__day=date.day,
                                             restaurant=restaurant).aggregate(Sum("headcount", default=0))
        print(result["headcount__sum"])
        if result["headcount__sum"] > restaurant.headcount:
            raise ValidationError("予約可能人数を超えています")
    
    #予約希望日が定休日でないかつ営業時間内であることを確認
    #最初に定休日の確認
        print( date.weekday() )

        holidays = [
            "月曜日",
            "火曜日",
            "水曜日",
            "木曜日",
            "金曜日",
            "土曜日",
            "日曜日",
        ]

        print(self.restaurant.holiday.filter(holiday=holidays[ date.weekday() ]))
        print(self.restaurant.holiday.filter(holiday=holidays[ date.weekday() ]).exists() )
        if self.restaurant.holiday.filter(holiday=holidays[ date.weekday() ]).exists():
            raise ValidationError("この予約希望日は定休日の為、予約できません")
        
    #営業時間内かどうか確認
        start = restaurant.start_hour
        end   = restaurant.end_hour

        print(start)
        print(end)
        print(type(end))

        scheduled_time = datetime.time(date.hour,date.minute)
        print(scheduled_time)

        if start > scheduled_time or scheduled_time > end:
            raise ValidationError("営業時間外の予約はできません")
