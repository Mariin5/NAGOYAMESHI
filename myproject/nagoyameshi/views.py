from django.shortcuts import render,redirect
# TODO:この先は、TemplateViewやListViewなどではなく、Viewを継承したビュークラスを使いましょう(ビューの処理をより高度にできる)
from django.views import View


# 未認証であればログインページにリダイレクトさせる。
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Category,Area,PayMethod,Holiday,Restaurant,Review,Reservation,Company
from .forms import CategoryForm,AreaForm,PayMethodForm,HolidayForm,RestaurantForm,ReviewForm,ReservationForm,CompanyForm

class IndexView(View):
    # リクエストメソッドごとの処理を書く。
    # リクエストメソッド(リクエストの種類。getメソッド と postメソッドがある。getメソッドを使って読み込み・検索。postメソッドを使って投稿・書き込み)
    # requestはリクエストオブジェクト、*argsと**kwargsは溢れた引数を受け取ることができる。エラー対策。
    # https://noauto-nolife.com/post/django-args-kwargs/
    def get(self, request, *args, **kwargs):

        context = {}

        # Categoryモデルを使って、Categoryの全データを取り出す。
        context["categories"]   = Category.objects.all()





        # render関数は指定したテンプレートのレンダリングをしている。
        # 第一引数はrequestオブジェクト、第2引数はテンプレート、第3引数はコンテキスト(DBなどから読み込みしたデータ(辞書型))
        return render(request, "nagoyameshi/index.html", context)

index   = IndexView.as_view()

class RestaurantListView(View):

    def get(self, request, *args, **kwargs):

        context = {}
        context["categories"]   = Category.objects.all()

        """
        restaurants = Restaurant.objects.all()

        paginator   = Paginator(restaurants,6)

        if "page" in request.GET:
            context["restaurants"] = paginator.get_page(request.GET["page"])
        else:
            context["restaurants"] = paginator.get_page(1)
        """


        # Restaurantのidが1のデータを取り出す
        #context["restaurants"]  = Restaurant.objects.filter(id=1)

        # nameがtestのデータを取り出す。
        #context["restaurants"]  = Restaurant.objects.filter(name="test")

        # name="test" では 完全一致。testを含む検索をする 
        # __icontains : 大文字と小文字を区別しない
        # __contains : 大文字と小文字を区別する。
        context["restaurants"]  = Restaurant.objects.filter(name__icontains="test")

        # ↓『test ああああ』を含むのであって、『test』と『ああああ』を含むという意味ではない。
        context["restaurants"]  = Restaurant.objects.filter(name__icontains="test ああああ")

        # クエリビルダを使うことになる。.filter()に格納する検索条件を詳細に指定できる。


        return render(request, "nagoyameshi/restaurant_list.html", context)

restaurant_list   = RestaurantListView.as_view()


class RestaurantDetailView(View):

    def get(self, request, pk, *args, **kwargs):

        context = {}
        context["restaurant"]   = Restaurant.objects.filter(id=pk).first()

        return render(request, "nagoyameshi/restaurant_detail.html", context)
        
    #TODO: このPOSTメソッドでレビューを受け付ける？

restaurant_detail   = RestaurantDetailView.as_view()


