from django.db.models import Sum
from market_data.models import AmfiMonthlyData


# ======================================================
# CONFIG
# ======================================================

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


# ======================================================
# 1️⃣ MONTHLY SUMMARY (Single Month KPIs)
# ======================================================

def monthly_amfi_summary(month: str):
    """
    Returns Small Cap and Large+Mid Cap summary for a given month
    Used for KPI cards and base analytics
    """

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


# ======================================================
# 2️⃣ MONTH-TO-MONTH COMPARISON
# ======================================================

def compare_two_months(month_a: str, month_b: str):
    """
    Compares two months and returns net change
    Used for MoM growth / decline indicators
    """

    if not AmfiMonthlyData.objects.filter(month=month_a).exists():
        return {"error": f"No data for {month_a}"}

    if not AmfiMonthlyData.objects.filter(month=month_b).exists():
        return {"error": f"No data for {month_b}"}

    a = monthly_amfi_summary(month_a)
    b = monthly_amfi_summary(month_b)

    return {
        "month_a": month_a,
        "month_b": month_b,
        "small_cap_change": round(b["small_cap"] - a["small_cap"], 2),
        "large_midcap_change": round(b["large_midcap"] - a["large_midcap"], 2),
    }


# ======================================================
# 3️⃣ YEAR-WISE PIVOT (Month × Category Matrix)
# ======================================================

def amfi_year_pivot(year: str):
    """
    Returns category-wise monthly matrix for a given year
    Used for pivot table UI
    """

    qs = AmfiMonthlyData.objects.filter(month__endswith=year)

    months = sorted(
        qs.values_list("month", flat=True).distinct()
    )

    categories = sorted(
        qs.values_list("scheme_category", flat=True).distinct()
    )

    matrix = {month: {} for month in months}

    for row in qs:
        matrix[row.month][row.scheme_category] = row.net_inflow

    return {
        "year": year,
        "months": months,
        "categories": categories,
        "matrix": matrix,
    }
