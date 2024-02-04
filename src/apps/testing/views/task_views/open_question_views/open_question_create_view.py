from django.views.generic import CreateView


class OpenQuestionCreateView(CreateView):
    def __init__(self):
        raise NotImplementedError
    # model =
    # form_class = ClosedQuestionForm
    # template_name = 'testing/task/closed_question_create_or_update.html'
    # pk_url_kwarg = 'testing_pk'
