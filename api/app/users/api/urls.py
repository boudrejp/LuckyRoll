from django.urls import path
from users.api.views import CurrentUserApiView


urlpatterns = [
    path("user/", CurrentUserApiView.as_view(), name="current-user")
]
