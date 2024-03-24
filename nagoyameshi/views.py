#from msilib.schema import ListView
from django.shortcuts import render,redirect
from django.views import View
from django.shortcuts import redirect, get_object_or_404


# 未認証であればログインページにリダイレクトさせる。
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin


from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from .models import Category,Area,PayMethod,Holiday,Restaurant,Review,Reservation,Company,Favorite
from .forms import CategoryForm,AreaForm,PayMethodForm,HolidayForm,RestaurantForm,ReviewForm,ReservationForm,CompanyForm,FavoriteForm,RestaurantCategorySearchForm,YearMonthForm
import stripe
from django.urls import reverse_lazy
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


 

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        query   =Q()


        if "search" in request.GET:
            print(request.GET["search"])
            context["restaurants"]   = Restaurant.objects.filter(name__icontains=request.GET["search"])
            print( request.GET["search"].replace(" ","　").split("　") )
            
            #split = 文字分割、スペースも文字とみなす
            words =request.GET["search"].replace(" ","　").split("　")
            #nameをモデル名に変更すれば他条件での検索も可能になる
            for word in words:
                query &= Q(name__icontains=word)
        
        #restaurant内でフィルターをかけた結果をだす
        context["restaurants"] = Restaurant.objects.filter(query)

        #Categoryモデルを全て表示
        context["categories"]  = Category.objects.all()

        # render関数は指定したテンプレートのレンダリングをしている。
        # 第一引数はrequestオブジェクト、第2引数はテンプレート、第3引数はコンテキスト(DBなどから読み込みしたデータ(辞書型))
        return render(request, "nagoyameshi/index.html", context)

    def post(self, request, *args, **kwargs):
        # POSTメソッドを使用してリクエストが送られた場合、この部分の処理が実行される。
        pass



index   = IndexView.as_view()

class RestaurantListView(View):

    def get(self, request, *args, **kwargs):

        context = {}
        query   = Q()

        context["categories"] = Category.objects.all()

        if "search" in request.GET:
            words = request.GET["search"].replace(" ","　").split("　")
            for word in words:
                #AND検索：&=
                #OR検索 ：!=
                #OR検索で空文字を含むと全件が検索結果として表示されるため、空文字がない場合は検索条件を追加という定義をする（if word !="":）
                if word   != "": 
                    query &= Q( Q(name__icontains=word) | Q(area__area=word) | Q(category_name__category_name=word) )


        #TODO : ここにカテゴリでの検索にも対応させる。
        # RestaurantCategorySearchForm で実在するカテゴリのidかをチェックする。
        form    = RestaurantCategorySearchForm(request.GET)

        if form.is_valid():
            # このManyToManyFieldのオブジェクトは直接指定して検索はできない。
            print( form.cleaned_data["category_name"] )
            # そのため、request.GETからidをセット
            query &= Q(category_name=request.GET["category_name"])



        print(query)

        # TODO:カテゴリも含めて検索する。
        restaurants = Restaurant.objects.filter(query)
        #ページネーション
        #第一引数：オブジェクト、第二引数：1ページに表示するオブジェクト数
        paginator = Paginator(restaurants,6)

        if "page" in request.GET:
            restaurants = paginator.get_page(request.GET["page"])
        else:
            restaurants = paginator.get_page(1)

        #検索ワードを引き継いだままページ遷移できるようにする
        copied = request.GET.copy()

        #パラメータ
        print("?" + copied.urlencode())

        #前にページがある場合
        if restaurants.has_previous():
            copied["page"]                 = restaurants.previous_page_number()
            restaurants.previous_page_link = "?" + copied.urlencode()

            copied["page"]                 = 1
            restaurants.first_page_link = "?" + copied.urlencode()

        #次にページがある場合
        if restaurants.has_next():
            copied["page"]                 = restaurants.next_page_number()
            restaurants.next_page_link = "?" + copied.urlencode()

            copied["page"]                 = restaurants.paginator.num_pages
            restaurants.end_page_link = "?" + copied.urlencode()
        
        context["restaurants"]  = restaurants

        return render(request,"nagoyameshi/restaurant_list.html",context)

restaurant_list = RestaurantListView.as_view()

        
class RestaurantDetailView(View):

    def get(self, request, pk, *args, **kwargs):

        context = {}
        context["restaurant"]   = Restaurant.objects.filter(id=pk).first()
        #レストランのIDとレビューが紐づいているためfilter(restaurant=pk)
        context["reviews"]  = Review.objects.filter(restaurant=pk).order_by("-created_at")



        return render(request, "nagoyameshi/restaurant_detail.html", context)
    
    def post(self, request, pk,*args, **kwargs):
        #request.POSTにはstar subject contentしか入ってないため、name,restaurantがバリデーションエラーになる
        copied          = request.POST.copy()

        copied["user"]  = request.user
        copied["restaurant"]  = pk
        form    = ReviewForm(copied)

        
        if form.is_valid():
            print('レビュー投稿が完了しました')
            form.save()
        else:
            print(form.errors)
        return redirect("nagoyameshi:restaurant_detail", pk)


restaurant_detail   = RestaurantDetailView.as_view()

class CategoryDetailView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}
        context["category"]   = Category.objects.filter(id=pk).first()
        context["restaurant"]   = Restaurant.objects.filter(id=pk).first()

        return render(request, "nagoyameshi/category_detail.html", context)

category_detail   = CategoryDetailView.as_view()

#お気に入り登録



def company_detail(request):
    companies = Company.objects.all()
    context   = {'companies':companies,}
    return render(request,"nagoyameshi/company_detail.html",context)

def terms_of_service(request):
    return render(request,"nagoyameshi/terms_of_service.html")

def contact(request):
    return render(request,"nagoyameshi/contact.html")

def premium_contents(request):
    return render(request,"nagoyameshi/premium_contents.html")

def membership(request):
    return render(request,"nagoyameshi/membership.html")


stripe.api_key  = settings.STRIPE_API_KEY


class CheckoutView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        checkout_session =stripe.checkout.Session.create(
            line_items=[
                {
                    'price':settings.STRIPE_PRICE_ID,
                    'quantity':1,
                },
            ],
            payment_method_types=['card'],
            mode='subscription',
            success_url=request.build_absolute_uri(reverse_lazy("nagoyameshi:success")) + f'?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=request.build_absolute_uri(reverse_lazy("nagoyameshi:index")),
        )

        print( checkout_session["id"] )

        return redirect(checkout_session.url)

checkout    = CheckoutView.as_view()

class SuccessView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        if "session_id" not in request.GET:
            print("セッションIDがありません。")
            return redirect("nagoyameshi:index")
        try:
            checkout_session_id = request.GET['session_id']
            checkout_session    = stripe.checkout.Session.retrieve(checkout_session_id)
        except:
            print( "このセッションIDは無効です。")
            return redirect("nagoyameshi:index")
        print(checkout_session)

        if checkout_session["payment_status"] != "paid":
            print("未払い")
            return redirect("nagoyameshi:index")
        print("支払い済み")


        request.user.customer   = checkout_session["customer"]
        request.user.save()

        print("有料会員登録しました！")

        return redirect("nagoyameshi:index")

success     = SuccessView.as_view()

class PortalView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        if not request.user.customer:
            print( "有料会員登録されていません")
            return redirect("nagoyameshi:index")

        portalSession   = stripe.billing_portal.Session.create(
            customer    = request.user.customer,
            return_url  = request.build_absolute_uri(reverse_lazy("nagoyameshi:index")),
        )

        return redirect(portalSession.url)

portal      = PortalView.as_view()


class PremiumView(View):
    def get(self, request, *args, **kwargs):
        

        try:
            subscriptions = stripe.Subscription.list(customer=request.user.customer)
        except:
            print("このカスタマーIDは無効です。")
            return redirect("nagoyameshi:index")
        

        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")

                return render(request, "nagoyameshi/premium.html")
            else:
                print("サブスクリプションが無効です。")

        return redirect("nagoyameshi:index")

premium     = PremiumView.as_view()

#ログイン状態とサブスク状態を一気にチェック
class PremiumMemberMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):

        if not request.user.is_authenticated:
            #return redirect("login")と同じ
            return self.handle_no_permission()

        #カスタマーIDの確認
        try:
            subscriptions = stripe.Subscription.list(customer=request.user.customer)
        except:
            print("このカスタマーIDは無効です。")
            request.user.customer = ""
            request.user.save()
            return redirect("nagoyameshi:index")

    #サブスクの確認
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です")
                return super().dispatch(request,*args,**kwargs)
            else:
                print("サブスクリプションが無効です。再度登録をお願いします。")
            request.user.customer = ""
            request.user.save()
            return redirect("nagoyameshi:index")
        
class FavoriteView(PremiumMemberMixin,View):

    def get(self, request, *args, **kwargs):

        context                 = {}
        context["favorites"]    = Favorite.objects.filter(user=request.user).order_by("-created_at")

        return render(request, "nagoyameshi/favorite.html", context)

    def post(self, request, *args, **kwargs):
        copied          = request.POST.copy()

        # お気に入り登録したユーザー情報
        copied["user"]  = request.user
        form    = FavoriteForm(copied)

        
        if form.is_valid():
            form.save()

        return redirect("nagoyameshi:favorite")

favorite        = FavoriteView.as_view()

# お気に入り削除
class FavoriteDeleteView(PremiumMemberMixin, View):
    def post(self, request, pk,  *args, **kwargs):

        favorite    = Favorite.objects.filter(id=pk, user=request.user).first()
        favorite.delete()

        return redirect("nagoyameshi:favorite")

favorite_delete = FavoriteDeleteView.as_view()
        
class ReservationView(PremiumMemberMixin,View):
        def get(self, request, *args, **kwargs):
            context = {}

        #現在時刻より未来の予約のみ表示
        #__gte : Greater Than or Equal
        # 過去の予約を出す場合は　__lte：Less Than or Equal
        # https://noauto-nolife.com/post/django-filter-method/
            context["reservations"] = Reservation.objects.filter(user=request.user, scheduled_date__gte=timezone.now()).order_by("scheduled_date")
            return render(request, "nagoyameshi/reservation.html", context)

        def post(self, request, *args, **kwargs):
            copied          = request.POST.copy()
            copied["user"]  = request.user
            form    = ReservationForm(copied)

            if form.is_valid():
                print("予約が完了しました")
                form.save()

                def get(self, request, *args, **kwargs):

                    subject = "NAGOYAMESHI：予約完了"
                    message = "NAGOYAMESHIのご利用ありがとうございます。予約が完了しました。予約詳細はマイページよりご確認ください。"

                    from_email = nagoyameshi@test.com
                    recipient_list = [ "nagoyameshi@testl.com" ]
                    send_mail(subject, message, from_email, recipient_list)

                return redirect("nagoyameshi:reservation")

            else:
                print("予約に失敗しました。営業時間と予約可能人数をご確認の上、再度予約をお願いします")
                print(form.errors)
            return redirect("nagoyameshi:restaurant_detail")

reservation  = ReservationView.as_view()

# 予約の削除(キャンセル)をするビュー
class ReservationDeleteView(PremiumMemberMixin,View):
    def post(self, request, pk,  *args, **kwargs):

        reservation = Reservation.objects.filter(id=pk, user=request.user).first()

        # TODO: ここで削除する前に、予約キャンセル可能かを調べる。
    
        now         = datetime.datetime.now()

        # 予約のキャンセルは前日の23時59分までに行う。
        # 予約した日から、前日の23時59分のDateTimeオブジェクトを作る。
        dt          = reservation.scheduled_date - datetime.timedelta(days=1)
        deadline    = datetime.datetime( year=dt.year , month=dt.month, day=dt.day, hour=23, minute=59)

        print(deadline)

        if now < deadline:
            print("予約キャンセル")
        else:
            print("予約キャンセルできません。")


        return redirect("nagoyameshi:reservation")

reservation_delete  = ReservationDeleteView.as_view()



class AccountDeleteView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):

        request.user.is_active = False
        request.user.save() 
        return redirect("nagoyameshi:index")
account_delete      = AccountDeleteView.as_view()


class ProfitView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return redirect("nagoyameshi:index")
        
        context = {}

        form = YearMonthForm(request.GET)

        #期間指定
        if form.is_valid():
            select_date = datetime.date(year=form.cleaned_data["year"],month=form.cleaned_data["month"],day=1)
        else:
            select_date             = datetime.date.today()

        first_day       = datetime.date(year=select_date.year, month=select_date.month, day=1)

        #12月の次は一年増やす、それ以外は増やさない
        if select_date.month == 12:
            last_day    = datetime.date(year=select_date.year+1, month=1, day=1) - datetime.timedelta(days=1)
        else:
            last_day    = datetime.date(year=select_date.year, month=select_date.month+1, day=1) - datetime.timedelta(days=1)
        
        print(first_day)
        print(last_day)

        context["first_day"]    = first_day
        context["last_day"]     = last_day

        #UNIXタイムスタンプ：https://wa3.i-3-i.info/word18475.html
        #Stripeから売上実績を引きだすためにUNIXタイムスタンプが必要
        #int：整数にする

        first_time = int( datetime.datetime.combine(first_day, datetime.datetime.min.time() ).timestamp())
        last_time  = int( datetime.datetime.combine(last_day, datetime.datetime.min.time() ).timestamp())

        print(first_time)
        print(last_time)

        #取得したい期間設定：選択期間の時間00::~23:59まで
        created = {"gte":first_time,"lte":last_time}

        all_charges = []
        has_more = True
        starting_after = None

        while has_more:
            charges = stripe.Charge.list(limit=100, created=created, starting_after=starting_after)

            has_more =charges.has_more
            if has_more:
                starting_after = charges.data[-1].id

            all_charges.extend(charges.data)
        
        print(len(all_charges))

        total_sales = 0
        for charge in all_charges:
            total_sales += charge["amount"]

        print(total_sales)

        context["total_sales"] = total_sales
            
        today   = datetime.date.today()
        context["year"]             = [ y for y in range( today.year, today.year-11, -1) ]
        context["month"]            = [ m for m in range(1, 13) ]
        context["select_date"]      = select_date



    
        # ======総会員数、有料会員数、無料会員数、店舗総数、総予約数を出力する。=============== 

        context["all_user"]     = User.objects.count()
        context["premium_user"] = User.objects.exclude(customer=None).count()
        context["normal_user"]  = User.objects.filter(customer=None).count()

        
        context["restaurant"]   = Restaurant.objects.count()
        context["reservation"]  = Reservation.objects.count()


        return render(request, "nagoyameshi/profit.html", context)

profit  = ProfitView.as_view()

'''
class ReviewView(PremiumMemberMixin,View):
    def post(self, request, pk,*args, **kwargs):
        #request.POSTにはstar subject contentしか入ってないため、name,restaurantがバリデーションエラーになる
        copied          = request.POST.copy()

        copied["user"]  = request.user
        copied["restaurant"]  = pk
        form    = ReviewForm(request.POST)

        
        if form.is_valid():
            print('レビュー投稿が完了しました')
            form.save()
        else:
            print(form.errors)
        return redirect("nagoyameshi:restaurant_detail", pk)
review   = ReviewView.as_view()
'''



