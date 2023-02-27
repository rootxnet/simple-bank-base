from django.contrib import admin

from transactions.models import FinancialAccount, Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "note",
        "transaction_type",
        "transaction_status",
        "amount",
        "currency_code",
        "transaction_time",
    )
    list_filter = (
        "account",
        "transaction_type",
        "transaction_status",
        "currency_code",
        "transaction_time",
    )

    search_fields = ("note", "amount")


class FinancialAccountAdmin(admin.ModelAdmin):
    list_display = ("owner", "balance", "transaction_num")


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(FinancialAccount, FinancialAccountAdmin)
