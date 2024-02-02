from msilib.schema import ListView
from django.shortcuts import render,redirect
# TODO:この先は、TemplateViewやListViewなどではなく、Viewを継承したビュークラスを使いましょう(ビューの処理をより高度にできる)
from django.views import View
from django.shortcuts import redirect, get_object_or_404


# 未認証であればログインページにリダイレクトさせる。
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from .models import Category,Area,PayMethod,Holiday,Restaurant,Review,Reservation,Company,Favorite
from .forms import CategoryForm,AreaForm,PayMethodForm,HolidayForm,RestaurantForm,ReviewForm,ReservationForm,CompanyForm,FavoriteForm

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

        return render(request, "nagoyameshi/restaurant_detail.html", context)

restaurant_detail   = RestaurantDetailView.as_view()

class CategoryDetailView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}
        context["category"]   = Category.objects.filter(id=pk).first()
        context["restaurant"]   = Restaurant.objects.filter(id=pk).first()

        return render(request, "nagoyameshi/category_detail.html", context)
    

category_detail   = CategoryDetailView.as_view()

#お気に入り登録
class FavoriteView(LoginRequiredMixin, View):

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
class FavoriteDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk,  *args, **kwargs):

        favorite    = Favorite.objects.filter(id=pk, user=request.user).first()
        favorite.delete()

        return redirect("nagoyameshi:favorite")

favorite_delete = FavoriteDeleteView.as_view()


def company_detail(request):
    companies = Company.objects.all()
    context   = {'companies':companies,}
    return render(request,"nagoyameshi/company_detail.html",context)

def terms_of_service(request):
    return render(request,"nagoyameshi/terms_of_service.html")

def contact(request):
    return render(request,"nagoyameshi/contact.html")




