from django.urls import reverse_lazy
from django.views import View

from apps.testing_by_code.models import SolvingTesting


class SolvingTestingView(View):
    model = SolvingTesting

    def post(self, request):
        post_method = request.POST
        solving_testing_pk = post_method.get('solving_testing_pk')
        user_answers = post_method.getlist('answer')
        solving_testing = self.model.objects.get(pk=solving_testing_pk)
        solving_testing.complete(user_answers)
        return reverse_lazy('user:home', pk=request.user.pk)
