from django.shortcuts import render
from core.decorators import group_required
from django.core.mail import send_mail
from .models import Quote
from accounts.models import CustomUser
from django.conf import settings

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
            html_message = f"Here's todays quote:\n{quote.title}\n@{quote.author}\n{quote.content}",
        )

@group_required("quotes")
def index(request):
    random_quote = get_random_quote()
    return render(request, "quotes/index.html", {
        "random_quote": random_quote,
    })
