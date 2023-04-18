from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q

from accounts.models import CustomUser
from core.decorators import group_required

from .forms import QuoteSearchForm, QuoteForm
from .models import Quote

from notifications.models import Notification
from notifications.views import add_notification


def get_all_quotes(user):
    return Quote.objects.filter(Q(public=True, approved="AP") | Q(user=user)).all()


@group_required("quotes")
def index(request, quote_id=None):
    if quote_id:
        try:
            quote = Quote.objects.get(id=quote_id)
        except:
            return render(
                request,
                "core/index.html",
                {"error": f"Quote with id {quote_id} doesn't exist."},
            )
        form = QuoteSearchForm()
    else:
        if request.method == "POST":
            form = QuoteSearchForm(request.POST)
            if form.is_valid():
                quote = form.search(request.user, get_all_quotes)
        else:
            form = QuoteSearchForm()
            quote = get_all_quotes(request.user).order_by("?").first()

    context = {
        "form": form,
        "quote": quote,
    }
    return render(request, "quotes/index.html", context)


@group_required("quotes")
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            if quote.public == False:
                quote.approved = "AP"
                quote.save()
            elif quote.public == True:
                notification = Notification(
                    user=request.user,
                    title="Your new quote is waiting for approval.",
                    content=f"Your new quote ({quote.title}) is waiting for approval. We are going to inform you after next steps.",
                    link=f"/quotes/display-quote/{quote.id}",
                )
                add_notification(notification)

                for user in CustomUser.objects.filter(groups__name="approve quotes"):
                    notification = Notification(
                        user=user,
                        title="New quote is waiting for approval.",
                        content=f"New quote ({quote.title}) is waiting for approval.",
                        link=f"/quotes/admin/approve-quotes#{quote.id}",
                    )
                    add_notification(notification)

            return redirect(reverse("quotes:display_quote", args=[quote.id]))
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


@group_required("quotes")
def favorite_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    if request.user.favorite_quotes.filter(id=quote_id).exists():
        request.user.favorite_quotes.remove(quote)
    else:
        request.user.favorite_quotes.add(quote)
    return redirect(reverse("quotes:display_quote", args=[quote.id]))


@group_required("approve quotes")
def approve_quotes_panel(request):
    quotes_to_approve = Quote.objects.filter(approved="WT")

    return render(
        request,
        "quotes/approve_quotes_panel.html",
        {
            "quotes": quotes_to_approve,
        },
    )


@group_required("approve quotes")
def approve_quote_panel(request, quote_id):
    quote = Quote.objects.get(id=quote_id)

    return render(
        request,
        "quotes/approve_quote_details.html",
        {
            "quote": quote,
        },
    )


@group_required("approve quotes")
def approve_quote(request, quote_id, decision):
    quote = Quote.objects.get(id=quote_id)

    if decision == "Approve":
        quote.approved = "AP"
        title = "Your new quote has been approved."
        message = f"Your new quote ({quote.title}) has been approved. We think it's going to enrich our collection."
    elif decision == "Reject":
        quote.approved = "RJ"
        title = "Your new quote has been rejected."
        message = f"Your new quote ({quote.title}) has been rejected. It didn't match our standards."

    quote.save()

    notification = Notification(
        user=quote.user,
        title=title,
        content=message,
        link=f"/quotes/display-quote/{quote.id}",
    )
    add_notification(notification)

    return redirect(reverse("quotes:approve_quotes_panel"))


@group_required("quotes")
def update_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            temp_quote = form.save(commit=False)
            quote.user = request.user
            quote.title = temp_quote.title
            quote.author = temp_quote.author
            quote.language = temp_quote.language
            quote.public = temp_quote.public
            quote.content = temp_quote.content
            quote.approved = "WT"
            quote.save()
            if temp_quote.public == False:
                quote.approved = "AP"
                quote.save()
            elif temp_quote.public == True:
                notification = Notification(
                    user=request.user,
                    title="Your updated quote is waiting for approval.",
                    content=f"Your new quote ({quote.title}) is waiting for approval. We are going to inform you after next steps.",
                    link=f"/quotes/display-quote/{quote.id}",
                )
                add_notification(notification)

                for user in CustomUser.objects.filter(groups__name="approve quotes"):
                    notification = Notification(
                        user=user,
                        title="New quote is waiting for approval.",
                        content=f"New quote ({quote.title}) is waiting for approval.",
                        link=f"/quotes/admin/approve-quotes#{quote.id}",
                    )
                    add_notification(notification)

            return redirect(reverse("quotes:display_quote", args=[quote.id]))
    else:
        form = QuoteForm(instance=quote)
    return render(request, "quotes/add_quote.html", {"form": form, "quote": quote})


def daily_quote():
    quote = Quote.objects.order_by("?").first()
    newsletter_users = CustomUser.objects.filter(groups__name="quote newsletter")

    send_mail(
        subject="Quote Newsletter",
        message=f"Here's todays quote:\n{quote.title}\n@{quote.author}\n{quote.content}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email for user in newsletter_users],
        html_message=f"Here's todays quote:\n{quote.title}\n@{quote.author}\n{quote.content}",
    )
