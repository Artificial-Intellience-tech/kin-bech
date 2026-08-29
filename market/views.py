from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SellRequest, SellImage
from .forms import SellRequestForm


def marketplace_list(request):
    sell_requests = SellRequest.objects.select_related("seller").order_by("-created_at")
    return render(
        request,
        "marketplace/marketplace.html",
        {"sell_requests": sell_requests},
    )


@login_required
def create_sell_request(request):
    if request.method == "POST":
        form = SellRequestForm(request.POST, request.FILES)
        if form.is_valid():
            sell_request = form.save(commit=False)
            sell_request.seller = request.user
            sell_request.save()

            # Handle multiple uploaded images
            for img in request.FILES.getlist("images"):
                SellImage.objects.create(sell_request=sell_request, image=img)

            return redirect("market:marketplace")
    else:
        form = SellRequestForm()

    return render(
        request,
        "marketplace/create_sell_request.html",
        {"form": form},
    )


@login_required
def delete_sell_request(request, pk):
    item = get_object_or_404(SellRequest, pk=pk)
    if item.seller != request.user:
        return redirect("market:marketplace")

    item.delete()
    # Redirect to the logged-in user's profile
    return redirect("profile", user_id=request.user.id)