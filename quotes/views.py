from django.shortcuts import render, redirect
from core.decorators import group_required
from django.core.mail import send_mail
from .models import Quote
from accounts.models import CustomUser
from django.conf import settings
from .forms import QuoteForm


def get_random_quote():
    quote = Quote.objects.order_by("?").first()
    return quote


def daily_quote():
    quote = get_random_quote()
    newsletter_users = CustomUser.objects.filter(quote_newsletter=True).all()

    send_mail(
        subject="Quote Newsletter",
        message=f"Here's todays quote:\n{quote.title}\n@{quote.author}\n{quote.content}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email for user in newsletter_users],
        html_message=f"Here's todays quote:\n{quote.title}\n@{quote.author}\n{quote.content}",
    )


@group_required("quotes")
def index(request):
    random_quote = get_random_quote()
    return render(request, "quotes/index.html", {
        "quote": random_quote,
        "random": True,
    })


@group_required("quotes")
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect(f"/quotes/display-quote/{quote.id}")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {
        "form": form
    })


@group_required("quotes")
def display_quote(request, quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
    except:
        return render(request, "core/index.html", {
            "error": f"Quote with id {quote_id} doesn't exist."
        })

    return render(request, "quotes/index.html", {
        "quote": quote,
    })
