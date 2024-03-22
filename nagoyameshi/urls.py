from django.urls import path
from . import views

#ABC順
app_name    = "nagoyameshi"
urlpatterns = [ 
    #TOP
    path("", views.index, name="index"),
    #アカウント削除
    path("account_delete/", views.account_delete , name="account_delete"),
    #カテゴリ別ページ
    path("category_detail/<int:pk>/", views.category_detail, name="category_detail"),
    #有料会員サブスク決済ページ(Stripe)に遷移
    path("checkout/", views.checkout, name="checkout"),
    #会社概要
    path("company_detail/", views.company_detail, name="company_detail"),
    #問合せ
    path('contact/',views.contact,name='contact'),
    #有料会員のみ：お気に入り店舗管理
    path('favorite/',views.favorite,name="favorite"),
    #有料会員のみ：お気に入り店舗削除
    path('favorite_delete/<int:pk>/',views.favorite_delete,name="favorite_delete"),
    #会員情報管理
    path("membership/", views.membership, name="membership"),
    #有料会員登録しているかどうか確認
    path("portal/", views.portal, name="portal"),
    #有料会員のみ：有料会員かどうか表示
    path("premium/", views.premium, name="premium"),
    #無料会員向け：有料会員特典紹介
    path('premium_contents/',views.premium_contents,name="premium_contents"),
    #管理者のみ：売上管理
    path("profit/", views.profit, name="profit"),
    #有料会員のみ：予約管理
    path('reservation/',views.reservation,name="reservation"),
    #有料会員のみ：予約取り消し
    path('reservation_delete/<int:pk>/',views.reservation_delete,name="reservation_delete"),
    #店舗一覧
    path("restaurant_list/", views.restaurant_list, name="restaurant_list"),
    #店舗詳細
    path("restaurant_detail/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    #サブスク決済完了
    path("success/", views.success, name="success"),
    #利用規約
    path('terms_of_service/',views.terms_of_service,name="terms_of_service"),

]

