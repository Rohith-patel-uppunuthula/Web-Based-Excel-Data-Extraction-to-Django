from django.http import JsonResponse
from market_data.services.amfi_analytics import monthly_amfi_summary

def amfi_monthly_summary_api(request):
    month = request.GET.get("month")
    if not month:
        return JsonResponse(
            {"error": "month query param is required"},
            status=400
        )

    data = monthly_amfi_summary(month)
    return JsonResponse(data)


from market_data.services.amfi_analytics import compare_two_months

def amfi_compare_api(request):
    month_a = request.GET.get("from")
    month_b = request.GET.get("to")

    if not month_a or not month_b:
        return JsonResponse(
            {"error": "from and to query params are required"},
            status=400
        )

    data = compare_two_months(month_a, month_b)
    return JsonResponse(data)
