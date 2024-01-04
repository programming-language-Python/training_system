from mixins import URLMixin


class ContextMixin(URLMixin):
    def get_testing_list_data(self, is_teacher: bool) -> dict[str, str]:
        context = self.get_testing_list_url_data()
        if is_teacher:
            text = 'Настроить тестирование'
            context |= self.get_testing_create_url_data()
        else:
            text = 'Пройти тест'
        context['text'] = text
        return context
