from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.TextInput(attrs={'class': 'edit-input'}))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
