from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q

from accounts.models import CustomUser
from core.decorators import group_required

from .forms import QuoteFiltersForm, QuoteForm
from .models import Quote

from random import choice


def index(request):
    return display_quote(request)


@group_required("quotes")
def display_quote(request, quote_id=None, params: dict = None):
    if quote_id:
        try:
            quote = Quote.objects.get(id=quote_id)
        except:
            return render(
                request,
                "core/index.html",
                {"error": f"Quote with id {quote_id} doesn't exist."},
            )
    elif params:
        filter_query = Q()
        for param_name, param_value in params.items():
            if param_value:
                filter_query &= Q(**{param_name: param_value})

        matching_quotes = Quote.objects.filter(filter_query)

        if matching_quotes:
            quote = choice(matching_quotes)
    else:
        quote = Quote.objects.order_by("?").first()

    return render(
        request,
        "quotes/index.html",
        {
            "quote": quote,
            "quote_is_favorite": request.user.favorite_quotes.filter(
                id=quote.id
            ).exists(),
        },
    )


@group_required("quotes")
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect(reverse("quotes:display_quote", args=[quote.id]))
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


@login_required
def favorite_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    if request.user.favorite_quotes.filter(id=quote_id).exists():
        request.user.favorite_quotes.remove(quote)
    else:
        request.user.favorite_quotes.add(quote)
    return redirect(reverse("quotes:display_quote", args=[quote.id]))


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
