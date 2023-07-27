from django.db.models import Manager
from django.forms import Form

from testing.models import Setting
from testing.services.filter_setting import FilterSetting
from user.models import User


class SettingService:
    user: User
    setting: Manager[Setting]
    setting_form: Manager[Form]

    def __init__(self, user: User, setting_form) -> None:
        self.user = user
        self.setting_form = setting_form

    def set(self) -> None:
        filtered_setting = self.filter()
        if filtered_setting.exists():
            self.setting = self._set_for_user(filtered_setting)
        else:
            self.add()

    def _set_for_user(self, filtered_setting: Manager[FilterSetting]) -> Manager[Setting]:
        filtered_setting = filtered_setting.filter(users=self.user)
        if filtered_setting.exists():
            return filtered_setting.first()
        return self.setting.users.add(self.user)

    def filter(self) -> Manager[FilterSetting]:
        filter_setting = FilterSetting(self.setting_form)
        filtered_setting = filter_setting.execute()
        self.setting = filtered_setting.first()
        return filtered_setting

    def add(self) -> None:
        self.setting = self.setting_form.save(commit=False)
        self.setting.pk = None
        self.setting.save()
        self.setting_form.save_m2m()
        self.setting.users.add(self.user)

    @staticmethod
    def update(task: Manager, setting: Manager) -> Manager:
        task.setting = setting
        task.save(update_fields=['setting'])
        return task

    def get(self):
        return self.setting

    def get_pk(self):
        return self.setting.pk

    def get_form(self):
        return self.setting_form
