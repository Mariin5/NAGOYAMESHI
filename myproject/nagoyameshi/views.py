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
    def get(self, request, *args, **kwargs):
        context = {}
        print("IndexViewメソッド")
        print(request.GET)

        #カテゴリで検索した場合
        if "search" in request.GET:
            print(request.GET["search"])
            context["restaurant"]   = Restaurant.objects.filter(name__icontains=request.GET["search"])
            print( request.GET["search"].replace(" ","　").split("　") )
            

        #未検索時の表示（店舗を表示）
        else:
            context["restaurants"]  = Restaurant.objects.all()
        '''
        ifとelseの間に以下elifた追記可能？「カテゴリ」「店舗名」「エリア」など複数条件で検索できるようにするには？
        #カテゴリで検索した場合
        elif "search" in request.GET:
            print(request.GET["search"])
            context["categories"]   = Category.objects.filter(name__icontains=request.GET["search"])
            print( request.GET["search"].replace(" ","　").split("　") )

        #エリアで検索した場合
        elif "search" in request.GET:
            print(request.GET["search"])
            context["area"]         = Area.objects.filter(name__icontains=request.GET["search"])
            print( request.GET["search"].replace(" ","　").split("　") )
       '''
         # Categoryモデルを使って、Categoryの全データを取り出す。
        context["categories"]   = Category.objects.all()





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


