from django.contrib import admin
from .models import Phones, Ratings


class PhonesAdmin(admin.ModelAdmin):
    pass


class RatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Phones, PhonesAdmin)
admin.site.register(Ratings, RatingAdmin)
