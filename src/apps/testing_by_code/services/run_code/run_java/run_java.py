import re
import subprocess
import os
import time

from apps.testing_by_code.exceptions import CodeExecutionError


class RunJava:
    code: str
    file: str

    def __init__(self, code: str):
        is_class_example = 'class Example' in code
        if is_class_example:
            class_name_example = f'Example_{int(time.time())}'
            code = code.replace('Example', class_name_example)

        is_class_main = 'class Main' in code
        class_name_main = f'Main_{int(time.time())}'
        if is_class_main:
            code = code.replace('Main', class_name_main)
        else:
            code = f'''
                    public class {class_name_main} {'{'}
                        public static void main(String[] args) {'{'}
                            {code}
                        {'}'}
                    {'}'}'''
        self.code = code
        current_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        self.file = f'{current_dir}/{class_name_main}.java'

    def execute(self) -> str:
        name = self.file
        text = self.code
        with open(name, 'w') as file:
            file.write(text)
        return self._run_file()

    def _run_file(self) -> str:
        execution_process = subprocess.Popen(['java', self.file],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
        execution_output, execution_error = execution_process.communicate()
        if execution_error:
            message = f'Код написан с ошибкой. Ошибка выполнения кода: {execution_error.decode()}'
            raise CodeExecutionError(message)
        else:
            os.remove(self.file)
            correct_answer = execution_output.decode()
            return re.sub(r'[\r\n]', '', correct_answer)
