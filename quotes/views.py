from django.shortcuts import render, redirect


def index(request):
    if not request.user.groups.filter(name="quotes").exists():
        return redirect("core:index")
    return render(request, "quotes/index.html")


# Random Quote

# Add Quote

# Todays Quote
# Newsletter
