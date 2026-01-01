from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import AmfiMonthlyData


# =========================
# YEAR FILTER
# =========================
class YearFilter(SimpleListFilter):
    title = "Year"
    parameter_name = "year"

    def lookups(self, request, model_admin):
        years = (
            AmfiMonthlyData.objects
            .values_list("month", flat=True)
            .distinct()
        )
        year_set = sorted({m.split()[-1] for m in years})
        return [(y, y) for y in year_set]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(month__endswith=self.value())
        return queryset


# =========================
# MONTH FILTER (Year-dependent, calendar ordered)
# =========================
class MonthFilter(SimpleListFilter):
    title = "Month"
    parameter_name = "month_name"

    MONTH_ORDER = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    def lookups(self, request, model_admin):
        year = request.GET.get("year")
        if not year:
            return []

        months = (
            AmfiMonthlyData.objects
            .filter(month__endswith=year)
            .values_list("month", flat=True)
            .distinct()
        )

        month_set = {m.split()[0] for m in months}
        ordered_months = [m for m in self.MONTH_ORDER if m in month_set]
        return [(m, m) for m in ordered_months]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(month__startswith=self.value())
        return queryset


# =========================
# ADMIN
# =========================
@admin.register(AmfiMonthlyData)
class AmfiMonthlyDataAdmin(admin.ModelAdmin):
    list_display = (
        "scheme_category",
        "month",
        "net_inflow",
    )

    list_filter = (
        YearFilter,   # 👈 select Year first
        MonthFilter,  # 👈 then Month appears
    )

    search_fields = ("scheme_category",)
    ordering = ("month", "scheme_category")
    list_per_page = 50
