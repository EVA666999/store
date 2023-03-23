from .models import Basket


def baskets(request):
    user = request.user
    baskets = Basket.objects.filter(user=user) if user.is_authenticated else []
    return {"baskets": baskets}
