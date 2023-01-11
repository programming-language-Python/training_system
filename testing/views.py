from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, UpdateView

from config import settings
from testing.forms import TestingForm, TaskSettingForm
from testing.models import Testing, TaskSetting
from testing.services import redirect_not_is_teacher


# Create your views here.
class TestingList(ListView):
    model = Testing

    def get_queryset(self):
        return Testing.objects.select_related('user').filter(user=self.request.user)


class UpdateTesting(LoginRequiredMixin, UpdateView):
    model = Testing
    fields = '__all__'
    template_name_suffix = '_update'


#
# @require_POST
# def add_testing(request, product_model, product_id):
#     # Берём модель в которой находится товар
#     Product = apps.get_model('app', product_model)
#     product = Product.objects.get(id=product_id)
#     cart = Cart(request)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         if cd['update']:
#             cart.update(product, cd['quantity'], product.price)
#         else:
#             cart.add(Product, product, product.price, cd['quantity'])
#     return redirect('cart:cart_detail')

@login_required
def add_testing(request):
    redirect_not_is_teacher(request)

    testing_form = TestingForm()
    task_setting_form = TaskSettingForm()

    if request.method == 'POST':
        testing_form = TestingForm(request.POST)
        task_setting_form = TaskSettingForm(request.POST)
        print(testing_form.is_valid(), '\n', task_setting_form.is_valid())
        is_valid = testing_form.is_valid() and task_setting_form.is_valid()
        if is_valid:
            # print(form.cleaned_data)
            # news = News.objects.create(**form.cleaned_data)
            # testing = form.save()
            # return redirect(testing)
            # is_teacher = User.objects.get(pk=request.user.pk)
            print('test: ', task_setting_form.cleaned_data['title'])
        else:
            return render(request, 'inc/task_setting/_form.html', context={
                'form': task_setting_form
            })
    context = {
        'testing_form': testing_form,
        'number_of_forms': 0
    }
    return render(request, 'testing/add_testing.html', context)


def create_task_setting_form(request, number_of_forms):
    if number_of_forms != 0:
        settings.number_of_forms += 1
    form = TaskSettingForm()
    context = {
        'form': form,
        'number_of_forms': settings.number_of_forms
    }
    return render(request, 'inc/task_setting/_form.html', context)
