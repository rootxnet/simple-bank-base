from decimal import Decimal


class Transaction:
    TRANSACTION_CREDIT = "CREDIT"
    TRANSACTION_DEBIT = "DEBIT"
    TRANSACTION_TYPES = (
        (TRANSACTION_CREDIT, "Credit (Deposit))"),
        (TRANSACTION_DEBIT, "Debit (Withdrawal)"),
    )

    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_DENIED = "DENIED"
    TRANSACTION_STATUSES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_DENIED, "Denied"),
    )


class Currency:
    USD = "USD"
    GBP = "GBP"
    EUR = "EUR"
    PLN = "PLN"

    CURRENCY_CHOICES = (
        (USD, "US Dollar"),
        (GBP, "British Pound"),
        (EUR, "Euro"),
        (PLN, "Polish Złoty"),
    )

    class Exchange:
        USD = Decimal(1)
        GBP = Decimal("1.2")
        EUR = Decimal("1.07")
        PLN = Decimal("0.23")
