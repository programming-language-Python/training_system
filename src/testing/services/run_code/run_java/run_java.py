import subprocess
import time
import os

from testing.exceptions import CompilationError
from testing.utils.utils import write_to_file


class RunJava:
    code: str
    class_name_main: str
    class_name_example: str | None
    file: str

    def __init__(self, code: str):
        self.code = code
        self.set()

    def set(self):
        is_class_example = 'class Example' in self.code
        if is_class_example:
            self.class_name_example = f'Example_{int(time.time())}'
            self.code = self.code.replace('Example', self.class_name_example)
        else:
            self.class_name_example = None

        is_class_main = 'class Main' in self.code
        if is_class_main:
            self.class_name_main = f'Main_{int(time.time())}'
            self.code = self.code.replace('Main', self.class_name_main)
        else:
            self.class_name_main = f'Main_{int(time.time())}'
            self.code = f'''
                        public class {self.class_name_main} {'{'}
                            public static void main(String[] args) {'{'}
                                {self.code}
                            {'}'}
                        {'}'}'''
        self.file = f'{self.class_name_main}.java'

    def execute(self) -> str:
        name = self.file
        text = self.code
        write_to_file(name, text)
        return self.compile()

    def compile(self) -> str:
        # Компилируем файл
        compilation_process = subprocess.Popen(['javac', self.file],
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
        compilation_output, compilation_error = compilation_process.communicate()
        # Проверяем наличие ошибок компиляции
        if compilation_error:
            error_text = f'Компилируемый код написан с ошибкой.\n' \
                         f'Содержимое ошибки:\n{compilation_error.decode()}'
            raise CompilationError(error_text)
        else:
            return self.run_compiled_file()

    def run_compiled_file(self) -> str:
        # Запускаем скомпилированный файл
        execution_process = subprocess.Popen(['java', self.class_name_main],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
        execution_output, execution_error = execution_process.communicate()
        if execution_error:
            print('Ошибка выполнения:', execution_error.decode())
        else:
            self.remove_compiled_files()
            return execution_output.decode()

    def remove_compiled_files(self):
        os.remove(self.file)
        os.remove(self.class_name_main + '.class')
        if self.class_name_example:
            os.remove(self.class_name_example + '.class')


if __name__ == '__main__':
    # java_code = f'''class Example {'{'}
    #     int Z;
    # {'}'}
    # public class Main {'{'}
    #     public static void main(String[] args) {'{'}
    #
    #     Example w = new Example();
    #     Example j = w;
    #
    #     System.out.println(w.Z + " " + j.Z);
    #
    #     {'}'}
    # {'}'}
    # '''
    java_code = f'''
    public class Main {'{'}
        public static void main(String[] args) {'{'}
        System.out.println(1 + " " + 5);
        {'}'}
    {'}'}
    '''
    run_java = RunJava(java_code)
    print(run_java.execute())
