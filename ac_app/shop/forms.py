from django import forms


class ProductSortForm(forms.Form):
    sort = forms.ChoiceField(
        choices=(('date_desc', 'New Arrivals'),
                 ('price_desc', 'Price: High to Low'),
                 ('price_asc', 'Price: Low to High'),
                 ('name_asc', 'Name: (A-Z)'),
                 ('name_desc', 'Name: (Z-A)')), required=False)
