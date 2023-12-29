from django.urls import reverse

from abstractions.abstract_models.abstract_testing import AbstractTesting
from apps.testing_by_code.constants import APP_NAME


class Testing(AbstractTesting):
    def get_absolute_url(self):
        return reverse(APP_NAME + ':testing_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
