from market_data.models import AmfiMonthlyData
from django.db.models import Sum

LARGE_MIDCAP_BUCKET = [
    "Large Cap Fund",
    "Mid Cap Fund",
    "Large & Mid Cap Fund",
    "Flexi Cap Fund",
    "Focused Fund",
    "Value Fund/Contra Fund",
    "Dividend Yield Fund",
    "ELSS",
    "Sectoral/Thematic Funds",
]

def monthly_amfi_summary(month: str):
    qs = AmfiMonthlyData.objects.filter(month=month)

    small_cap = qs.filter(
        scheme_category="Small Cap Fund"
    ).aggregate(total=Sum("net_inflow"))["total"] or 0

    large_midcap = qs.filter(
        scheme_category__in=LARGE_MIDCAP_BUCKET
    ).aggregate(total=Sum("net_inflow"))["total"] or 0

    return {
        "month": month,
        "small_cap": round(small_cap, 2),
        "large_midcap": round(large_midcap, 2),
    }

def compare_two_months(month_a: str, month_b: str):
    a = monthly_amfi_summary(month_a)
    b = monthly_amfi_summary(month_b)

    return {
        "month_a": month_a,
        "month_b": month_b,
        "small_cap_change": round(b["small_cap"] - a["small_cap"], 2),
        "large_midcap_change": round(b["large_midcap"] - a["large_midcap"], 2),
    }
