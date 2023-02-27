from django.urls import path

from .views.user import CurrentUserView

app_name = "accounts"

account_details = CurrentUserView.as_view(actions={"get": "retrieve"})

urlpatterns = [
    path(r"current_user/", account_details, name="current-user"),
]
