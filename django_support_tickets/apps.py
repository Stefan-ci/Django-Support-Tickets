from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DjangoSupportTicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_support_tickets'
    verbose_name = _("Support Tickets")
