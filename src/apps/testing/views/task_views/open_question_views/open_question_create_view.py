from django.views.generic import CreateView


class OpenQuestionCreateView(CreateView):
    pk_url_kwarg = 'testing_pk'

    def __init__(self):
        raise NotImplementedError
