from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PushupForm100
from .models import PushUp
from random import sample

@login_required
def index(request):
    if not(request.user.id == 1 or request.user.email == "mgozdzik@duck.com"):
        return redirect("core:index")
    return render(request, "pushups/index.html")

@login_required
def genereate100(request):

    if request.method == "POST":
            form = PushupForm100(request.POST)
            if form.is_valid():
                choices = []
                for choice in PushUp.PUSHUP_CHOICES:
                    if form.cleaned_data.get(choice[0]):
                        choices.append(choice[0])
                
                total_reps = form.cleaned_data["total_reps"]
                num_sets = form.cleaned_data.get("num_sets")
                reps_in_set = form.cleaned_data.get("reps_in_set")

                if num_sets:
                    reps_per_set = total_reps // num_sets
                    remaining_reps = total_reps % num_sets
                else:
                    reps_per_set = reps_in_set
                    num_sets = total_reps // reps_in_set
                    remaining_reps = total_reps % reps_in_set

                if num_sets == 0:
                    pushup_plan = "Please enter a valid number of sets or reps in a set."
                elif num_sets == 1:
                    pushup_type = sample(choices, 1)[0]
                    pushup_plan = f"You have to make {total_reps} {PushUp.PUSHUP_CHOICES_DICT[pushup_type]} pushups."
                else:
                    set_choices = sample(choices, min(num_sets, len(choices)))
                    reps_per_choice = [reps_per_set for _ in range(len(set_choices))]
                    for i in range(remaining_reps):
                        reps_per_choice[i] += 1
                    plan = []
                    for choice, reps in zip(set_choices, reps_per_choice):
                        pushup_type = PushUp.PUSHUP_CHOICES_DICT[choice]
                        plan.append(f"You have to make {reps} {pushup_type} pushups.")
                    pushup_plan = "\n".join(plan)
    else:
        form = PushupForm100()
        pushup_plan = None
    return render(request, "pushups/pushup_100.html", {"form": form, "pushup_plan": pushup_plan})
