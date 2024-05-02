from abstractions.abstract_models import AbstractSolvingTesting
from apps.testing.constants import APP_NAME


class SolvingTesting(AbstractSolvingTesting):
    class Meta:
        db_table = f'{APP_NAME}_solving-testing'
