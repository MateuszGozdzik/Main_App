from django.shortcuts import render
from core.decorators import group_required
from .models import Quote

@group_required("quotes")
def index(request):
    random_quote = Quote.objects.order_by("?").first()
    # random_quote_content = random_quote.html

    return render(request, "quotes/index.html", {
        "random_quote": random_quote,
    })



# Add Quote

# Todays Quote
# Newsletter
