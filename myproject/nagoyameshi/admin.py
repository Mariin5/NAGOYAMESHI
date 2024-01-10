
# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/== #

from django.contrib import admin
from .models import Category,Area,PayMethod,Holiday,Restaurant,Review,Reservation,Company


from django.utils.html import format_html


class CategoryAdmin(admin.ModelAdmin):
    list_display	= [ "id", "category_name", "created_at", "updated_at" ]

class AreaAdmin(admin.ModelAdmin):
    list_display	= [ "id", "area", "created_at", "updated_at" ]

class PayMethodAdmin(admin.ModelAdmin):
    list_display	= [ "id" ,"format_paymethod" ]

    def format_paymethod(self, obj):
        content = ""

        for paymethod in obj.paymethod.all():
            content += paymethod.name

        return format_html('{}', content)

class HolidayAdmin(admin.ModelAdmin):
    list_display	= [ "id" , "format_holiday" ]

    def format_holiday(self, obj):
        content = ""

        for holiday in obj.holiday.all():
            content += holiday.name

        return format_html('{}', content)

class RestaurantAdmin(admin.ModelAdmin):
    list_display	= [ "id", "name", "name_kana", "image", "introduction", "format_area", "post_code", "format_holiday", "tel", "email", "format_paymethod", "has_parking", "created_at", "updated_at"]
    
    def format_category(self, obj):
        content  = ""

        for category_name in obj.category.all():
            content += category_name.caytegory + ","
        return format_html('{}', content)
        

    def format_paymethod(self, obj):

        content  = ""

        for paymethod in obj.paymethod.all():
            content += paymethod.name + ","

        return format_html('{}', content)


    def format_holiday(self, obj):
        content = ""

        for holiday in obj.holiday.all():
            content += holiday.name

        return format_html('{}', content)
    
    def format_area(self, obj):
        content = ""

        for area in obj.area.all():
            content += area.name

        return format_html('{}', content)


    # categoryはManyToMany、list_displayにManyToManyは入れることはできない。



class ReviewAdmin(admin.ModelAdmin):
    list_display	= [ "id", "user", "restaurant", "subject", "content", "created_at" ]

class ReservationAdmin(admin.ModelAdmin):
    list_display	= [ "id", "user", "restaurant", "scheduled_date", "headcount", "note" ]

class CompanyAdmin(admin.ModelAdmin):
    list_display	= [ "id", "name", "name_kana", "ceo", "founding_date", "capital", "activity", "post_code", "tel", "email", "created_at", "updated_at" ]


admin.site.register(Category,CategoryAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(PayMethod,PayMethodAdmin)
admin.site.register(Holiday,HolidayAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Company,CompanyAdmin)