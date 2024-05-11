from abstractions.abstract_models import AbstractSolvingTesting
from apps.testing.constants import APP_NAME


class SolvingTesting(AbstractSolvingTesting):
    class Meta(AbstractSolvingTesting.Meta):
        db_table = f'{APP_NAME}_solving-testing'
