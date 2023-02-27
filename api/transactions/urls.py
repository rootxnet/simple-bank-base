from django.urls import path

from .views import FinancialAccountSummaryView, TransactionView

app_name = "transactions"

transactions = TransactionView.as_view(actions={"get": "list"})
transaction_details = TransactionView.as_view(actions={"get": "retrieve"})
account_summary = FinancialAccountSummaryView.as_view(actions={"get": "retrieve"})

urlpatterns = [
    path(r"account/<str:account_pk>/", account_summary, name="account_summary"),
    path(r"account/<str:account_pk>/transactions/", transactions, name="transactions"),
    path(
        r"account/<str:account_pk>/transactions/<str:transaction_pk>/",
        transaction_details,
        name="transaction_details",
    ),
]
