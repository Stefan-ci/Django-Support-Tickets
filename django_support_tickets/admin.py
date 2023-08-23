from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from  django_support_tickets.models import Ticket, TicketComment
from django.template.defaultfilters import date as _date, time as _time


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 1
    classes = ["collapse"]
    fields = ["author", "attachment", "comment"]
    readonly_fields = ["date"]
    can_delete = False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["initial"] = request.user
        return super(TicketCommentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ["ticket", "author", "is_active", "date"]
    list_filter = ["is_active", "date"]
    search_fields = ["ticket__subject", "ticket__status", "ticket__rating_stars", "ticket__creator__username", 
        "ticket__creator__email", "ticket__creator__first_name", "ticket__creator__last_name", "ticket__assignee__username", 
        "ticket__assignee__email", "ticket__assignee__first_name", "ticket__assignee__last_name", 
        "ticket__description", "ticket__is_deleted", "ticket__uuid", "comment", "author__email", "author__username",
        "author__first_name", "author__last_name"]
    date_hierarchy = "date"
    
    
    fieldsets = [
        (_("Author"), {
            "fields": ["author"]
        }),
        
        (_("Ticket"), {
            "fields": ["ticket"]
        }),
        
        (_("Commemt"), {
            "fields": ["attachment", "comment"]
        })
    ]


class TicketAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["subject"]
    }
    list_display = ["subject", "status", "creator", "assignee", "latest_activity", "date"]
    list_filter = ["status", "rating_stars", "date"]
    search_fields = ["subject", "status", "creator", "assignee", "rating_stars", "date", "creator__username", "creator__email",
        "creator__first_name", "creator__last_name", "assignee__username", "assignee__email", "assignee__first_name",
        "assignee__last_name", "description", "is_deleted", "uuid"]
    inlines = [TicketCommentInline]
    date_hierarchy = "date"
    

    def latest_activity(self, obj):
        latest = obj.get_latest_comment()
        return "%s %s - %s" % (_date(latest.date), _time(latest.date), latest.author)
    latest_activity.short_description = _("Last activities")
    
    
    fieldsets = [
        (_("Creator & Assignee"), {
            "fields": ["creator", "assignee"]
        }),
        
        (_("Ticket"), {
            "fields": ["subject", "attachment", "status", "rating_stars", "description"]
        }),
                
        (_("Metadata"), {
            "fields": ["slug", "uuid"]
        }),
    ]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment, TicketCommentAdmin)
