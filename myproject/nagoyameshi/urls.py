from django.urls import path
from . import views

app_name    = "nagoyameshi"
urlpatterns = [ 
    path("", views.index, name="index"),
    path("restaurant_list/", views.restaurant_list, name="restaurant_list"),
    path("restaurant_detail/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    path("category_detail/<int:pk>/", views.category_detail, name="category_detail"),
    path("company_detail/", views.company_detail, name="company_detail"),
    path('contact/',views.contact,name='contact'),
    path('terms_of_service/',views.terms_of_service,name='terms_of_service'),
    path('favorite/',views.favorite,name='favorite'),
    path('reservation/',views.reservation,name='reservation'),
    path('favorite_delete/<int:pk>/',views.favorite_delete,name='favorite_delete'),
    path("", views.index, name="index"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.success, name="success"),
    path("portal/", views.portal, name="portal"),
    path("premium/", views.premium, name="premium"),
    path('premium_contents/',views.premium_contents,name='premium_contents'),
    path("membership/", views.membership, name="membership"),
]
    
