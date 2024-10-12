from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractAnswerOptionWithCheckbox
from apps.testing.constants import APP_NAME
from apps.testing.models.tasks import Sequencing


class SequencingAnswerOption(AbstractAnswerOptionWithCheckbox):
    sequencing = models.ForeignKey(
        Sequencing,
        on_delete=models.CASCADE,
        related_name='sequencing_answer_option_set',
        verbose_name='Установление последовательности'
    )

    class Meta(AbstractAnswerOptionWithCheckbox.Meta):
        db_table = f'{APP_NAME}_sequencing-answer-option'
