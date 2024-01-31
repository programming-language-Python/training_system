from django.views.generic import CreateView


class EstablishingAccordanceCreateView(CreateView):
    pk_url_kwarg = 'testing_pk'

    def __init__(self):
        raise NotImplementedError
