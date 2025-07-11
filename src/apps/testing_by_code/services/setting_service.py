from django.db.models import QuerySet

from apps.testing_by_code.forms import SettingForm
from apps.testing_by_code.models import Setting, Task
from apps.testing_by_code.services.filter_setting import FilterSetting


class SettingService:
    setting: Setting
    setting_form: SettingForm

    def __init__(self, setting_form: SettingForm) -> None:
        self.setting_form = setting_form

    def set(self) -> None:
        filtered_setting = self.filter()
        if filtered_setting.exists():
            self.setting = filtered_setting.first()
        else:
            self.add()

    def filter(self) -> QuerySet[Setting]:
        filter_setting = FilterSetting(self.setting_form)
        filtered_setting = filter_setting.execute()
        self.setting = filtered_setting.first()
        return filtered_setting

    def add(self) -> None:
        self.setting = self.setting_form.save(commit=False)
        self.setting.pk = None
        self.setting.save()
        self.setting_form.save_m2m()

    @staticmethod
    def update(task: Task, setting: Setting) -> Task:
        task.setting = setting
        task.save(update_fields=['setting'])
        return task

    def get(self):
        return self.setting

    def get_form(self):
        return self.setting_form
