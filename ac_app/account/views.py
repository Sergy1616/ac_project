from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, UpdateView, ListView
from django.shortcuts import get_object_or_404, redirect

from cart.forms import CartAddProductForm
from account.forms import (
    CustomPasswordResetForm,
    SignUpProfileForm,
    ProfileEditForm,
    CustomPasswordChangeForm,
    DeleteAccountForm
)
from account.models import Profile
from space.models import Comment, FavoriteStar
from shop.models import WishList
from cart.cart import Cart


class LoginProfileView(LoginView):
    template_name = "registration/login.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "account/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"


class SignUpProfileView(FormView):
    form_class = SignUpProfileForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_form'] = self.get_form()
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='account.authentication.EmailAuthBackend')
        return redirect('user_detail', username=user.username)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Failed to register your account.")
        return response


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'account/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.cleaned_data['remove_photo']:
            self.object.photo.delete()
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been updated.")
        referer_url = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer_url) if referer_url else response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Failed to update your profile.")
        return response


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change')
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully.")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Password change failed.")
        return response


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            form.save(request=request)
            messages.success(request, "We've emailed you instructions for setting your password.")
            return self.get(request, *args, **kwargs)
        else:
            return self.form_invalid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been set successfully.")
            return self.get(request, *args, **kwargs)
        else:
            return self.form_invalid(form)


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    form_class = DeleteAccountForm
    template_name = 'account/delete_account.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.POST.get('password')
        if user.check_password(password):
            if self.request.POST.get('confirm_delete'):
                return super().post(request, *args, **kwargs)
            else:
                messages.error(self.request, 'Please check the confirmation box to delete your account.')
                return super().get(request, *args, **kwargs)
        else:
            messages.error(self.request, 'Incorrect password. Account deletion failed.')
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        logout(self.request)
        return HttpResponseRedirect(success_url)


class UserCommentsView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'account/user_comments.html'
    context_object_name = 'user_comments'
    paginate_by = 8

    def get_queryset(self):
        return Comment.objects.select_related('news', 'author').filter(author=self.request.user)


class UserFavoriteStarsView(LoginRequiredMixin, ListView):
    model = FavoriteStar
    template_name = 'account/user_favorites.html'
    context_object_name = 'user_favorites'
    paginate_by = 8

    def get_queryset(self):
        return FavoriteStar.objects.select_related(
            'star__spectrum',
            'star__constellation').filter(user=self.request.user)


class UserWishListView(LoginRequiredMixin, DetailView):
    model = WishList
    template_name = 'account/user_wish_list.html'

    def get_object(self, queryset=None):
        wishlist, created = WishList.objects.prefetch_related(
            'products__images').get_or_create(user=self.request.user)
        return wishlist

    def get_queryset(self):
        queryset = WishList.objects.filter(user=self.request.user).select_related('user')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm(initial={'override': False})
        return context

    def post(self, request, *args, **kwargs):
        wishlist = self.get_object()
        products = wishlist.products.all()
        form = CartAddProductForm(request.POST)
        delete_wishlist = request.POST.get('delete_wishlist', False)

        if form.is_valid():
            valid_data = form.cleaned_data
            cart = Cart(request)
            for product in products:
                cart.add(
                    product_id=product.id,
                    quantity=valid_data['quantity'],
                    override_quantity=valid_data['override']
                    )
            if delete_wishlist:
                wishlist.delete()
            return redirect('cart_detail')

        return super().get_context_data(**kwargs)

