from django.urls import path
from . import views

handler500 = views.my_customized_server_error
app_name    = "nagoyameshi"
urlpatterns = [ 
    path("", views.index, name="index"),
    path("account_delete/", views.account_delete , name="account_delete"),
    path("category_detail/<int:pk>/", views.category_detail, name="category_detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("company_detail/", views.company_detail, name="company_detail"),
    path('contact/',views.contact,name='contact'),
    path('favorite/',views.favorite,name="favorite"),
    path('favorite_delete/<int:pk>/',views.favorite_delete,name="favorite_delete"),
    path("membership/", views.membership, name="membership"),
    path('past_reservation/',views.past_reservation,name="past_reservation"),
    path("portal/", views.portal, name="portal"),
    path("premium/", views.premium, name="premium"),
    path('premium_contents/',views.premium_contents,name="premium_contents"),
    path("profit/", views.profit, name="profit"),
    path('reservation/',views.reservation,name="reservation"),
    path('reservation_delete/<int:pk>/',views.reservation_delete,name="reservation_delete"),
    path("restaurant_list/", views.restaurant_list, name="restaurant_list"),
    path("restaurant_detail/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    path("success/", views.success, name="success"),
    path('terms_of_service/',views.terms_of_service,name="terms_of_service"),

]
    
