from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class AbstractFieldDescription(models.Model):
    description = CKEditor5Field(verbose_name='Описание')

    class Meta:
        abstract = True
