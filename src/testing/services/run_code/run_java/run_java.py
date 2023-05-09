import subprocess
import time
import os

from testing.utils.utils import write_to_file


class RunJava:
    def __init__(self, code: str, is_body: bool = False):
        self.is_body = is_body
        self.class_name = f"MyClass_{int(time.time())}"
        if is_body:
            self.java_file = f"{self.class_name}.java"
            self.code_java = f'''
            public class {self.class_name} {'{'}
                public static void main(String[] args) {'{'}
                    {code}
                {'}'}
            {'}'}'''
        else:
            pass
            # code.replace("Main", self.class_name)
            # code.replace("Example", )

    def execute(self) -> str:
        if self.is_body:
            name = self.java_file
            text = self.code_java
        else:
            name = self.java_file
            text = self.code_java
        write_to_file(name, text)
        return self.compile()

    def compile(self) -> str:
        # Компилируем файл
        compilation_process = subprocess.Popen(["javac", self.java_file],
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
        compilation_output, compilation_error = compilation_process.communicate()
        # Проверяем наличие ошибок компиляции
        if compilation_error:
            print("Ошибка компиляции:", compilation_error.decode())
        else:
            return self.run_compiled_file()

    def run_compiled_file(self) -> str:
        # Запускаем скомпилированный файл
        execution_process = subprocess.Popen(["java", self.class_name],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
        execution_output, execution_error = execution_process.communicate()
        os.remove(self.java_file)
        os.remove(self.class_name + '.class')
        return execution_output.decode()


if __name__ == "__main__":
    run_java = RunJava("System.out.println(15);", True)
    print(run_java.execute())
