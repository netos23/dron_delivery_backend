from django.urls import path

from .views import EmailPart1View, EmailPart2View

urlpatterns = [
    path("part1", EmailPart1View.as_view(), name="email-part1"),
    path("part2", EmailPart2View.as_view(), name="email-part2"),
]
