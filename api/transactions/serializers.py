from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from accounts.serializers.user import UserSerializer
from transactions.models import FinancialAccount, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class FinancialAccountSummarySerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = FinancialAccount
        fields = "__all__"
