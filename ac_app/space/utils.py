from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView


class PaginatedListView(ListView):
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.GET.get('ajax') == 'true':
            page = request.GET.get('page', 1)
            paginator = Paginator(self.object_list, self.paginate_by)
            try:
                objects = paginator.page(page)
            except PageNotAnInteger:
                objects = paginator.page(1)
            except EmptyPage:
                return HttpResponse('')

            context = {self.context_object_name: objects}
            return render(request, self.get_ajax_template_name(), context)

        return super().get(request, *args, **kwargs)

    def get_ajax_template_name(self):
        raise NotImplementedError("Define 'get_ajax_template_name' method with appropriate template name.")


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
