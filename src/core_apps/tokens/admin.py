from django.contrib import admin

from .models import Token, TokenPrice


class TokenPriceInline(admin.TabularInline):
    model = TokenPrice
    extra = 1


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = (TokenPriceInline,)


@admin.register(TokenPrice)
class TokenPriceAdmin(admin.ModelAdmin):
    list_display = ("token", "date", "price")
    list_filter = ("token", "date")
    search_fields = ("token__name", "date")
    ordering = ("-date",)
    raw_id_fields = ("token",)
    date_hierarchy = "date"
