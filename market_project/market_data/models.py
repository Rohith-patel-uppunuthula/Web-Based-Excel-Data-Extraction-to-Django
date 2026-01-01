from django.db import models


class AmfiMonthlyData(models.Model):
    month = models.CharField(
        max_length=20,
        help_text="Reporting month, e.g. November 2025"
    )

    scheme_category = models.CharField(
        max_length=200,
        help_text="Scheme category like Large Cap, Mid Cap, Small Cap"
    )

    net_inflow = models.FloatField(
        null=True,
        blank=True,
        help_text="Net inflow/outflow value for the month (INR Crores)"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "AMFI Monthly Data"
        verbose_name_plural = "AMFI Monthly Data"
        unique_together = ("month", "scheme_category")
        indexes = [
            models.Index(fields=["month"]),
            models.Index(fields=["scheme_category"]),
        ]

    def __str__(self):
        return f"{self.scheme_category} | {self.month}"
