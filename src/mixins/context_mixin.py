from typing import Mapping


class ContextMixin:
    APP_NAME: str

    def get_testing_list_data(self, is_teacher: bool) -> dict[str, str]:
        context = {
            'testing_list_url': f'{self.APP_NAME}:testing_list'
        }
        if is_teacher:
            text = 'Настроить тестирование'
            context |= {
                'testing_create_url': f'{self.APP_NAME}:testing_create'
            }
        else:
            text = 'Пройти тест'
        context['text'] = text
        return context

    def get_testing_detail_data(self, is_solving_testing: bool) -> dict[str, str]:
        return {
            'is_solving_testing': is_solving_testing,
            'testing_update_url': f'{self.APP_NAME}:testing_update',
            'testing_delete_url': f'{self.APP_NAME}:testing_delete'
        }
