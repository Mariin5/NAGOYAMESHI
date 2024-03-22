
# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/== #

from django.contrib import admin
from .models import Category,Area,PayMethod,Holiday,Restaurant,Review,Reservation,Company
from django.utils.html import format_html


class CategoryAdmin(admin.ModelAdmin):
    list_display	= [ "id", 
                        "category_name", 
                        "created_at", 
                        "updated_at" ]

class AreaAdmin(admin.ModelAdmin):
    list_display	= [ "id", 
                        "area", 
                        "created_at", 
                        "updated_at" ]

class PayMethodAdmin(admin.ModelAdmin):
    list_display	= [ "id" ,
                        "paymethod" ]

class HolidayAdmin(admin.ModelAdmin):
    list_display	= [ "id" , 
                        "holiday" ]

class RestaurantAdmin(admin.ModelAdmin):
    list_display    = [ "id", 
                       "name", 
                       "name_kana", 
                       "image", 
                       "introduction", 
                       "area", 
                       "post_code", 
                       "format_holiday", 
                       "tel", 
                       "email", 
                       "format_paymethod", 
                       "has_parking", 
                       "created_at", 
                       "updated_at", 
                       "format_category" ]
    filter_horizontal   = [ "category_name", "paymethod","holiday" ]

    def format_category(self, obj):
        content  = ""

        for category in obj.category_name.all():
            content += category.category_name + "," 
        return format_html('{}', content)

    def format_paymethod(self, obj):
        content  = ""

        for paymethod in obj.paymethod.all():
            content += paymethod.paymethod + ","
        return format_html('{}', content)


    def format_holiday(self, obj):
        content = ""

        for holiday in obj.holiday.all():
            content += holiday.holiday
        return format_html('{}', content)

class ReviewAdmin(admin.ModelAdmin):
    list_display	= [ "id", 
                        "user", 
                        "restaurant", 
                        "subject", 
                        "content", 
                        "created_at" ]

class ReservationAdmin(admin.ModelAdmin):
    list_display	= [ "id", 
                        "user", 
                        "restaurant", 
                        "scheduled_date", 
                        "headcount", 
                        "note" ]

class CompanyAdmin(admin.ModelAdmin):
    list_display	= [ "id", 
                        "name", 
                        "name_kana", 
                        "ceo", 
                        "founding_date", 
                        "capital", 
                        "activity", 
                        "post_code",  
                        "tel", 
                        "email", 
                        "created_at", 
                        "updated_at" ]


admin.site.register(Category,CategoryAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(PayMethod,PayMethodAdmin)
admin.site.register(Holiday,HolidayAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Company,CompanyAdmin)
