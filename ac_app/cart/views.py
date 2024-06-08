from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .cart import Cart
from .forms import CartAddProductForm


class CartDetailView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)

        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id, *args, **kwargs):
        cart = Cart(request)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            valid_data = form.cleaned_data
            cart.add(product_id=product_id, quantity=valid_data['quantity'], override_quantity=valid_data['override'])
            total_unique = cart.total_unique_items()
            return JsonResponse({
                'result': 'success',
                'message': 'Product successfully added to the cart',
                'total_unique': total_unique
            })
        return JsonResponse({"result": "error"}, status=400)


class CartRemoveView(View):
    def post(self, request, product_id, *args, **kwargs):
        cart = Cart(request)
        cart.remove(product_id)
        return JsonResponse({'result': 'success'})
