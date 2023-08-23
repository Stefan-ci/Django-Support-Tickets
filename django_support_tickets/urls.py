from django.urls import path
from django_support_tickets import views

app_name = "django-support-tickets"

urlpatterns = [
    path("my/", views.user_tickets_list_view, name="user-tickets-list"),
    path("my/create/", views.user_create_new_ticket_view, name="user-tickets-create"),
    path("my/detail/<str:slug>-get<int:pk>/", views.user_tickets_detail_view, name="user-tickets-detail"),
]

urlpatterns += [
    path("resolved/<str:slug>-get<int:pk>/", views.user_mark_ticket_as_resolved_view, name="user-mark-ticket-as-resolved"),
    path("close/<str:slug>-get<int:pk>/", views.user_mark_ticket_as_closed_view, name="user-mark-ticket-as-closed"),
    path("rate/<str:slug>-get<int:pk>/", views.user_rate_ticket_view, name="user-rate-ticket"),
]
