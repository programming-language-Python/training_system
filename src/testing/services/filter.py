from testing.models import TaskSetup


def filter_many_to_many_relationship(items_model, obj_to_filter=None, **kwargs):
    """Фильтрует связь многим ко многим"""
    items = items_model.objects.all()
    filter_field = kwargs['filter_field']
    items_form = kwargs['form'].cleaned_data.get(filter_field)
    selected_items = items.intersection(items_form)
    not_selected_items = items.difference(items_form)
    # print('items', items)
    # print('filter_field', filter_field)
    # print('items_form', items_form)
    # print('selected_items', selected_items)
    # print('not_selected_items', not_selected_items)

    if not obj_to_filter:
        obj_to_filter = TaskSetup.objects
    for selected_item in selected_items:
        # print(f'obj_to_filter.filter({filter_field}__title="{selected_item.title}")')
        obj_to_filter = eval(f'obj_to_filter.filter({filter_field}__title="{selected_item.title}")')

    for not_selected_item in not_selected_items:
        # print(f'obj_to_filter.exclude({filter_field}__title="{not_selected_item.title}")')
        obj_to_filter = eval(f'obj_to_filter.exclude({filter_field}__title="{not_selected_item.title}")')
    # print('obj_to_filter', obj_to_filter)
    return obj_to_filter
