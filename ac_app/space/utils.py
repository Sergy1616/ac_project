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

    def get_adjacent_item(self, direction):
        """
        General method to get the next or previous item.
        """
        if self.navigate_on_field is None:
            return None
        field_name = self.navigate_on_field
        current_value = getattr(self.object, field_name)
        model = self.model

        if self.sort_order == 'asc':
            if direction == 'next':
                filters = {**self.extra_filters, **{f'{field_name}__gt': current_value}}
                order_by_field = field_name
            elif direction == 'prev':
                filters = {**self.extra_filters, **{f'{field_name}__lt': current_value}}
                order_by_field = f'-{field_name}'
        else:
            if direction == 'next':
                filters = {**self.extra_filters, **{f'{field_name}__lt': current_value}}
                order_by_field = f'-{field_name}'
            elif direction == 'prev':
                filters = {**self.extra_filters, **{f'{field_name}__gt': current_value}}
                order_by_field = field_name

        return model.objects.filter(**filters).order_by(order_by_field).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_item'] = self.get_adjacent_item('next')
        context['prev_item'] = self.get_adjacent_item('prev')
        return context
