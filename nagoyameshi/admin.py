from django.contrib import admin

# Register your models here.
# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/== #

from django.contrib import admin
from .models import Category,Area,Paymethod,Holiday,Restaurant,Review,Reservation,Company

class CategoryAdmin(admin.ModelAdmin):
    list_display	= [ "id", "category", "created_at", "updated_at" ]

class AreaAdmin(admin.ModelAdmin):
    list_display	= [ "id", "area", "created_at", "updated_at" ]

class PaymethodAdmin(admin.ModelAdmin):
    list_display	= [ "id", "paymethod", "created_at", "updated_at" ]

class HolidayAdmin(admin.ModelAdmin):
    list_display	= [ "id", "holiday", "created_at", "updated_at" ]

class RestaurantAdmin(admin.ModelAdmin):
    list_display	= [ "id", "category", "name", "name_kana", "image", "introduction", "post_code", "address", "holiday", "tel", "email", "paymethod", "has_parking", "created_at", "updated_at" ]

class ReviewAdmin(admin.ModelAdmin):
    list_display	= [ "id", "user", "restaurant", "subject", "content", "created_at" ]

class ReservationAdmin(admin.ModelAdmin):
    list_display	= [ "id", "user", "restaurant", "scheduled_date", "headcount", "note" ]

class CompanyAdmin(admin.ModelAdmin):
    list_display	= [ "id", "name", "name_kana", "ceo", "founding_date", "capital", "activity", "post_code", "tel", "email", "created_at", "updated_at" ]


admin.site.register(Category,CategoryAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(Paymethod,PaymethodAdmin)
admin.site.register(Holiday,HolidayAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Company,CompanyAdmin)
