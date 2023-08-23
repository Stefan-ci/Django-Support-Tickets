import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


_NEW = 1
_OPEN = 2
_CLOSED = 3
_RESOLVED = 4


TICKET_STATUS_CHOICES = [
    (_NEW, _("Nouveau")),
    (_OPEN, _("Ouvert")),
    (_CLOSED, _("Fermé")),
    (_RESOLVED, _("Résolu")),
]

RATING_STARS_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]


class Ticket(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Creator"))
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Assignee"), null=True, blank=True, related_name="assigned_tickets")
    subject = models.CharField(max_length=255, verbose_name=_("Subject"))
    slug = models.SlugField(max_length=500, verbose_name=_("Slug"), null=True, blank=True)
    status = models.SmallIntegerField(verbose_name=_("Status"), choices=TICKET_STATUS_CHOICES, default=1)
    description = models.TextField(verbose_name=_("More details"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created on"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is deleted"))
    attachment = models.FileField(upload_to="tickets/main/attachments/%Y/%m/", null=True, blank=True, verbose_name=_("Attachment"))
    rating_stars = models.SmallIntegerField(verbose_name=_("Review"), choices=RATING_STARS_CHOICES, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True, unique=False, verbose_name="UUID")
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Updated on"))
    
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        ordering = ["-date", "subject", "status", "rating_stars"]
    
    def __str__(self) -> str:
        return f"{self.subject} :: {self.pk}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject)
        super(Ticket, self).save(*args, **kwargs)
        
    def active_comments(self):
        return self.ticketcomment_set.filter(is_deleted=False, is_active=True)
    
    def get_latest_comment(self):
        return self.ticketcomment_set.filter(is_deleted=False, is_active=True).latest("date")
    
    def rating_stars_range(self):
        return range(0, self.rating_stars)

    def is_answered(self):
        try:
            latest = self.get_latest_comment()
        except Ticket.DoesNotExist:
            return False
        return latest.author != self.creator



class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, verbose_name=_("Ticket"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Author"))
    comment = models.TextField(verbose_name=_("Comment"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is deleted"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    attachment = models.FileField(upload_to="tickets/comments/attachments/%Y/%m/", null=True, blank=True, verbose_name=_("Attachment"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created on"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Updated on"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-date", "ticket", "author", "is_active"]
    
    def __str__(self) -> str:
        return f"Comment on {self.ticket.subject}"
