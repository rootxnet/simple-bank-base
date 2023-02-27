import uuid
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from contrib import enums
from contrib.enums import Currency
from contrib.models import BaseModel


class FinancialAccount(BaseModel):
    owner = models.OneToOneField("accounts.User", on_delete=models.CASCADE)

    balance = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal(0))

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner)

    def transaction_num(self):
        return self.transactions.all().count()

    def get_transactions_by_date_range(self, date_start=None, date_end=None):
        date_filters = {}
        if date_start:
            date_filters["transaction_time__gte"] = date_start
        if date_end:
            date_filters["transaction_time__lte"] = date_end
        return self.transactions.filter(**date_filters)

    def calculate_balance(self, date_start=None, date_end=None):
        txs = self.get_transactions_by_date_range(
            date_start=date_start, date_end=date_end
        ).filter(transaction_status=enums.Transaction.STATUS_APPROVED)

        total = Decimal(0)
        for a in txs.values("currency_code", "transaction_type").annotate(
            total=Sum("amount")
        ):
            total += (
                -1
                if a["transaction_type"] == enums.Transaction.TRANSACTION_DEBIT
                else 1
            ) * Transaction.amount_to_USD(a["total"], a["currency_code"])

        return total

    def recalculate_balance(self):
        self.balance = self.calculate_balance()
        self.save()


class Transaction(BaseModel):
    MAX_AMOUNT = Decimal("100000")

    account = models.ForeignKey(
        "transactions.FinancialAccount",
        null=True,
        related_name="transactions",
        on_delete=models.SET_NULL,
    )

    note = models.CharField(max_length=1000, blank=True)

    transaction_type = models.CharField(
        max_length=21, choices=enums.Transaction.TRANSACTION_TYPES
    )
    transaction_status = models.CharField(
        max_length=21,
        choices=enums.Transaction.TRANSACTION_STATUSES,
        default=enums.Transaction.STATUS_APPROVED,
    )
    transaction_time = models.DateTimeField()

    amount = models.DecimalField(
        validators=[MinValueValidator(Decimal("0.01")), MaxValueValidator(MAX_AMOUNT)],
        max_digits=16,
        decimal_places=2,
    )
    currency_code = models.CharField(
        max_length=4,
        choices=enums.Currency.CURRENCY_CHOICES,
        default=enums.Currency.USD,
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            "transaction_time",
        ]

    def __str__(self):
        return f"{self.id}-{self.transaction_type}-{self.amount}"

    # def save(self, *args, **kwargs):
    #     super().save(*args, *kwargs)
    #
    #     # this would normally be added to the queue via a post_approve (transaction status was changed to approved)
    #     # signal to be processed asynchronously
    #     self.account.recalculate_balance()

    @staticmethod
    def amount_to_USD(amount, source_currency_code):
        if rate := getattr(Currency.Exchange, source_currency_code):
            return amount * rate

        raise ValueError(f"Exchange rate for {source_currency_code} does not exist.")

    @property
    def amount_USD(self):
        if self.currency_code == Currency.USD:
            return self.amount

        return self.amount_to_USD(
            amount=self.amount, source_currency_code=self.currency_code
        )


@receiver(post_save, sender=Transaction)
def transaction_saved(sender, instance: Transaction, created, **kwargs):
    if instance.transaction_status == enums.Transaction.STATUS_APPROVED:
        instance.account.recalculate_balance()
