from django.contrib import admin
from .models import AmfiMonthlyData


@admin.register(AmfiMonthlyData)
class AmfiMonthlyDataAdmin(admin.ModelAdmin):
    list_display = (
        "scheme_category",
        "month",
        "net_inflow",
        "created_at",
    )
    list_filter = ("month",)
    search_fields = ("scheme_category",)
