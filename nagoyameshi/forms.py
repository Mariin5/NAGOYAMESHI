# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #

from django import forms
from .models import Category,Area,PayMethod,Holiday,Restaurant,Review,Reservation,Company,Favorite
from django.core.validators import MinValueValidator,MaxValueValidator

class CategoryForm(forms.ModelForm):
    class Meta:
        model	= Category
        fields	= [ "category_name" ]

class AreaForm(forms.ModelForm):
    class Meta:
        model	= Area
        fields	= [ "area" ]

class PayMethodForm(forms.ModelForm):
    class Meta:
        model	= PayMethod
        fields	= [ "paymethod" ]

class HolidayForm(forms.ModelForm):
    class Meta:
        model	= Holiday
        fields	= [ "holiday" ]

class RestaurantForm(forms.ModelForm):
    class Meta:
        model	= Restaurant
        fields	= [ "category_name", 
                  "name", 
                  "name_kana", 
                  "image", 
                  "introduction", 
                  "post_code", 
                  "address", 
                  "start_hour", 
                  "end_hour",
                  "holiday", 
                  "tel", 
                  "email", 
                  "paymethod", 
                  "headcount",
                  "has_parking" ]

class ReviewForm(forms.ModelForm):
    class Meta:
        model	= Review
        fields	= [ "star",
                  "user", 
                  "restaurant", 
                  "subject", 
                  "content" ]

class ReservationForm(forms.ModelForm):
    class Meta:
        model	= Reservation
        fields	= [ "user", 
                  "restaurant", 
                  "scheduled_date", 
                  "headcount", 
                  "note" ]

class CompanyForm(forms.ModelForm):
    class Meta:
        model	= Company
        fields	= [ "name", 
                  "name_kana", 
                  "ceo", 
                  "founding_date", 
                  "capital", 
                  "activity", 
                  "post_code", 
                  "tel", 
                  "email" ]


class FavoriteForm(forms.ModelForm):
    class Meta:
        model   = Favorite
        fields  = [ "user", 
                   "restaurant" ]

class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
        model   = Restaurant
        fields  = [ "name" ]   

class RestaurantCategorySearchForm(forms.ModelForm):
    class Meta:
        model   = Restaurant
        fields  = [ "category_name" ]

class YearMonthForm(forms.Form):
    year  = forms.IntegerField()
    month = forms.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)])