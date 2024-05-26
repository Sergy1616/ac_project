class NavigationMixin:
    navigate_on_field = None
    extra_filters = {}
    sort_order = 'asc'

    def get_next_item(self):
        if self.navigate_on_field is None:
            return None
        field_name = self.navigate_on_field
        current_value = getattr(self.object, field_name)
        model = self.model
        if self.sort_order == 'asc':
            filters = {**self.extra_filters, **{f'{field_name}__gt': current_value}}
            next_item = model.objects.filter(**filters).order_by(field_name).first()
        else:
            filters = {**self.extra_filters, **{f'{field_name}__lt': current_value}}
            next_item = model.objects.filter(**filters).order_by(f'-{field_name}').first()
        return next_item

    def get_prev_item(self):
        if self.navigate_on_field is None:
            return None
        field_name = self.navigate_on_field
        current_value = getattr(self.object, field_name)
        model = self.model
        if self.sort_order == 'asc':
            filters = {**self.extra_filters, **{f'{field_name}__lt': current_value}}
            prev_item = model.objects.filter(**filters).order_by(f'-{field_name}').first()
        else:
            filters = {**self.extra_filters, **{f'{field_name}__gt': current_value}}
            prev_item = model.objects.filter(**filters).order_by(field_name).first()
        return prev_item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_item'] = self.get_next_item()
        context['prev_item'] = self.get_prev_item()
        return context
