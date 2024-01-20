from typing import Mapping


class URLMixin(object):
    APP_NAME: str

    def get_testing_list_url_data(self) -> dict[str, str]:
        return {'testing_list_url': self.get_testing_list_url()}

    def get_testing_list_url(self) -> str:
        return self.APP_NAME + ':testing_list'

    def get_testing_create_url_data(self) -> dict[str, str]:
        return {'testing_create_url': self.get_testing_create_url()}

    def get_testing_create_url(self) -> str:
        return self.APP_NAME + ':testing_create'

    def get_testing_detail_url_button_data(self) -> Mapping:
        return {
            'testing_update_url': self.get_testing_update_url(),
            'testing_delete_url': self.get_testing_delete_url(),
            'add_task_form_url': self.get_add_task_form_url()
        }

    def get_testing_update_url_data(self) -> dict[str, str]:
        return {'testing_update_url': self.get_testing_update_url()}

    def get_testing_update_url(self) -> str:
        return self.APP_NAME + ':testing_update'

    def get_testing_delete_url_data(self) -> dict[str, str]:
        return {'testing_delete_url': self.get_testing_delete_url()}

    def get_testing_delete_url(self) -> str:
        return self.APP_NAME + ':testing_delete'

    def get_add_task_form_url(self) -> str:
        return self.APP_NAME + ':add_task_form'
