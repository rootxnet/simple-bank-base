from decimal import Decimal

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import User
from contrib import enums
from transactions.models import FinancialAccount, Transaction


@override_settings()
class TestTransactions(TestCase):
    """Test transactions."""

    def setUp(self):
        """
        Setup all required data, generate auth data.
        """
        self.client = APIClient()

        self.user = User.objects.create(username="test_user")
        self.user.set_password("123qwe")
        self.user.save()

        self.financial_account = FinancialAccount.objects.create(
            owner=self.user,
        )

        auth_token_response = self.client.post(
            path=reverse("token_obtain_pair"),
            data={"username": "test_user", "password": "123qwe"},
            format="json",
        )

        self.auth_token = auth_token_response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)

    def test_initial_deposit(self):
        self.assertEqual(self.financial_account.balance, Decimal(0))

        transaction_deposit = Transaction.objects.create(
            account=self.financial_account,
            note="Initial deposit",
            transaction_type=enums.Transaction.TRANSACTION_CREDIT,
            transaction_status=enums.Transaction.STATUS_PENDING,
            transaction_time=timezone.now(),
            amount=10000,
            currency_code=enums.Currency.USD,
        )
        # status is PENDING
        self.assertEqual(self.financial_account.balance, Decimal(0))

        transaction_deposit.transaction_status = enums.Transaction.STATUS_APPROVED
        transaction_deposit.save()
        self.assertEqual(self.financial_account.balance, Decimal(10000))

        # simulate request, it should contain only the original cleared transfer transaction
        response = self.client.get(
            reverse(
                "transactions:transactions",
                kwargs={"account_pk": self.financial_account.pk},
            ),
        ).json()
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["id"], str(transaction_deposit.id))

    def test_mixed_transaction_types(self):
        self.assertEqual(self.financial_account.balance, Decimal(0))

        transaction_deposit1 = Transaction.objects.create(
            account=self.financial_account,
            note="Some deposit",
            transaction_type=enums.Transaction.TRANSACTION_CREDIT,
            transaction_status=enums.Transaction.STATUS_APPROVED,
            transaction_time=timezone.now(),
            amount=200,
            currency_code=enums.Currency.USD,
        )

        transaction_withdrawal1 = Transaction.objects.create(
            account=self.financial_account,
            note="Some withdrawal",
            transaction_type=enums.Transaction.TRANSACTION_DEBIT,
            transaction_status=enums.Transaction.STATUS_APPROVED,
            transaction_time=timezone.now(),
            amount=150,
            currency_code=enums.Currency.USD,
        )

        self.assertEqual(self.financial_account.balance, Decimal(50))

        # simulate request, it should contain only the original cleared transfer transaction
        response = self.client.get(
            reverse(
                "transactions:transactions",
                kwargs={"account_pk": self.financial_account.pk},
            ),
        ).json()
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["id"], str(transaction_deposit1.id))
        self.assertEqual(response[1]["id"], str(transaction_withdrawal1.id))

    def test_mixed_currency_transactions(self):
        transaction_deposit1_PLN = Transaction.objects.create(
            account=self.financial_account,
            note="PLN Deposit",
            transaction_type=enums.Transaction.TRANSACTION_CREDIT,
            transaction_status=enums.Transaction.STATUS_APPROVED,
            transaction_time=timezone.now(),
            amount=1000,
            currency_code=enums.Currency.PLN,
        )

        transaction_deposit2_GBP = Transaction.objects.create(
            account=self.financial_account,
            note="GBP Deposit",
            transaction_type=enums.Transaction.TRANSACTION_CREDIT,
            transaction_status=enums.Transaction.STATUS_APPROVED,
            transaction_time=timezone.now(),
            amount=1000,
            currency_code=enums.Currency.GBP,
        )

        transaction_deposit3_USD = Transaction.objects.create(
            account=self.financial_account,
            note="USD Deposit",
            transaction_type=enums.Transaction.TRANSACTION_CREDIT,
            transaction_status=enums.Transaction.STATUS_APPROVED,
            transaction_time=timezone.now(),
            amount=1000,
            currency_code=enums.Currency.USD,
        )

        # calculate total balance using exchange rates
        balance = Decimal(
            enums.Currency.Exchange.PLN * 1000
            + enums.Currency.Exchange.GBP * 1000
            + enums.Currency.Exchange.USD * 1000
        )

        self.assertEqual(self.financial_account.balance, balance)

        response = self.client.get(
            reverse(
                "transactions:transactions",
                kwargs={"account_pk": self.financial_account.pk},
            ),
        ).json()
        self.assertEqual(len(response), 3)
        self.assertEqual(response[0]["id"], str(transaction_deposit1_PLN.id))
        self.assertEqual(response[1]["id"], str(transaction_deposit2_GBP.id))
        self.assertEqual(response[2]["id"], str(transaction_deposit3_USD.id))

        response = self.client.get(
            reverse(
                "transactions:account_summary",
                kwargs={"account_pk": self.financial_account.pk},
            ),
        ).json()
        self.assertEqual(response["balance"], balance)
