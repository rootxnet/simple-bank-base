from rest_framework import mixins, permissions, viewsets

from transactions.models import FinancialAccount, Transaction
from transactions.serializers import (FinancialAccountSummarySerializer,
                                      TransactionSerializer)


# Create your views here.
class TransactionView(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(account__pk=self.kwargs.get("account_pk"))


class FinancialAccountSummaryView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = FinancialAccountSummarySerializer
    queryset = FinancialAccount.objects.all()
    lookup_field = "account_pk"

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs.get(self.lookup_field))
