from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django_support_tickets.forms import TicketCommentForm, TicketForm
from django_support_tickets.models import Ticket, TicketComment, _NEW, _OPEN, _CLOSED, _RESOLVED


@login_required(login_url="accounts:login")
def user_tickets_list_view(request):
    tickets = Ticket.objects.filter(creator=request.user).order_by("-date")
    
    paginator = Paginator(tickets, 10)
    page = request.GET.get("page")
    tickets_obj = paginator.get_page(page)

    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    context = {
        "tickets": tickets_obj,
        "NEW_STATUS": _NEW,
        "OPEN_STATUS": _OPEN,
        "CLOSED_STATUS": _CLOSED,
        "RESOLVED_STATUS": _RESOLVED,
    }

    template_name = "django_support_tickets/user_tickets_list.html"
    return render(request, template_name, context)



@login_required(login_url="accounts:login")
def user_tickets_detail_view(request, slug, pk):
    try:
        ticket = Ticket.objects.get(slug=slug, pk=pk, is_deleted=False, creator=request.user)
    except Ticket.DoesNotExist:
        ticket = None
        messages.error(request, _("Ticket not found !"))
        raise Http404
    
    comment_form = TicketCommentForm
    
    if request.method == "POST":
        if ticket.status == _CLOSED or ticket.status == _RESOLVED:
            messages.error(request, _("This ticket has been already closed or resolved !"))
            return redirect(request.META.get("HTTP_REFERER"))
        
        comment_form = TicketCommentForm(data=request.POST, files=request.FILES) or None
        if comment_form.is_valid():
            cleaned_data = comment_form.cleaned_data
            comment = TicketComment.objects.create(
                ticket=ticket,
                author=request.user,
                comment=cleaned_data["comment"],
                attachment=cleaned_data["attachment"]
            )
            messages.success(request, _("Ticket commented successfully!"))
            return redirect(request.META.get("HTTP_REFERER"))
        
        else:  # if not form.is_valid()
            errors = comment_form.errors.as_data()
            for error in errors:
                msg = "".join(errors[error][0])
                messages.error(request, _(f"{error.capitalize()}: {msg}"))
            return redirect(".")
    
    else: # request.method != "POST"
        comment_form = TicketCommentForm()
    
    context = {
        "ticket": ticket,
        "comment_form": comment_form,
        "NEW_STATUS": _NEW,
        "OPEN_STATUS": _OPEN,
        "CLOSED_STATUS": _CLOSED,
        "RESOLVED_STATUS": _RESOLVED,
    }
    template_name = "django_support_tickets/user_tickets_detail.html"
    return render(request, template_name, context)




@login_required(login_url="accounts:login")
def user_create_new_ticket_view(request):
    form = TicketForm
    
    if request.method == "POST":
        form = TicketForm(data=request.POST, files=request.FILES) or None
        if form.is_valid():
            cleaned_data = form.cleaned_data
            ticket = Ticket(
                creator=request.user,
                subject=cleaned_data["subject"],
                description=cleaned_data["description"],
                attachment=cleaned_data["attachment"],
                status=_NEW
            )
            
            ticket.save()
            
            messages.success(request, _("Ticket created successfully. Our help center will reach as soon as possible."))
            return redirect(ticket.user_ticket_detail_absolute_url())
        
        else:  # if not form.is_valid()
            errors = form.errors.as_data()
            for error in errors:
                msg = "".join(errors[error][0])
                messages.error(request, _(f"{error.capitalize()}: {msg}"))
            return redirect(".")
    
    else: # request.method != "POST"
        form = TicketForm()
    
    context = {
        "form": form,
        "NEW_STATUS": _NEW,
        "OPEN_STATUS": _OPEN,
        "CLOSED_STATUS": _CLOSED,
        "RESOLVED_STATUS": _RESOLVED,
    }
    template_name = "django_support_tickets/user_create_new_ticket.html"
    return render(request, template_name, context)









@login_required(login_url="accounts:login")
@require_POST
def user_mark_ticket_as_closed_view(request, slug, pk):
    try:
        ticket = Ticket.objects.get(slug=slug, pk=pk, is_deleted=False, creator=request.user)
    except Ticket.DoesNotExist:
        ticket = None
        messages.error(request, _("Ticket not found!"))
        raise Http404
    
    ticket.status = _CLOSED
    ticket.save()
    messages.success(request, _("Ticket closed successfully!"))
    return redirect(request.META.get("HTTP_REFERER"))





@login_required(login_url="accounts:login")
@require_POST
def user_mark_ticket_as_resolved_view(request, slug, pk):
    try:
        ticket = Ticket.objects.get(slug=slug, pk=pk, is_deleted=False, creator=request.user)
    except Ticket.DoesNotExist:
        ticket = None
        messages.error(request, _("Ticket not found!"))
        raise Http404
    
    ticket.status = _RESOLVED
    ticket.save()
    messages.success(request, _(f"Ticket #{ticket.pk} has been marked as resolved successfully!"))
    return redirect(request.META.get("HTTP_REFERER"))




@login_required(login_url="accounts:login")
@require_POST
def user_rate_ticket_view(request, slug, pk):
    try:
        ticket = Ticket.objects.get(slug=slug, pk=pk, is_deleted=False, creator=request.user)
    except Ticket.DoesNotExist:
        ticket = None
        messages.error(request, _("Ticket not found!"))
        raise Http404
    
    ticket.rating_stars = int(request.POST["rating_stars"] or 5)
    ticket.save()
    messages.success(request, _(f"Thank you for rating this discussion (Ticket #{ticket.pk})"))
    return redirect(request.META.get("HTTP_REFERER"))
