from django.urls import path
from . import views

app_name    = "nagoyameshi"
urlpatterns = [ 
    path("", views.index, name="index"),
    path("restaurant_list/", views.restaurant_list, name="restaurant_list"),
    path("restaurant_detail/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    path("company_detail/", views.company_detail, name="company_detail"),
]