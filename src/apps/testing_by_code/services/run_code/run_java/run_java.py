import re
import subprocess
import os
import time


class RunJava:
    code: str
    file: str

    def __init__(self, code: str):
        self.code = code
        self.set()

    def set(self):
        is_class_example = 'class Example' in self.code
        if is_class_example:
            class_name_example = f'Example_{int(time.time())}'
            self.code = self.code.replace('Example', class_name_example)

        is_class_main = 'class Main' in self.code
        if is_class_main:
            class_name_main = f'Main_{int(time.time())}'
            self.code = self.code.replace('Main', class_name_main)
        else:
            class_name_main = f'Main_{int(time.time())}'
            self.code = f'''
                        public class {class_name_main} {'{'}
                            public static void main(String[] args) {'{'}
                                {self.code}
                            {'}'}
                        {'}'}'''
        current_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        self.file = f'{current_dir}/{class_name_main}.java'

    def execute(self) -> str:
        name = self.file
        text = self.code
        with open(name, 'w') as file:
            file.write(text)
        return self.run_file()

    def run_file(self) -> str:
        execution_process = subprocess.Popen(['java', self.file],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
        execution_output, execution_error = execution_process.communicate()
        if execution_error:
            print('Ошибка выполнения:', execution_error.decode())
        else:
            os.remove(self.file)
            return re.sub(r'[\s\r\n]', '', execution_output.decode())
