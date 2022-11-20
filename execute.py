import os.path, subprocess
from subprocess import STDOUT, PIPE


def judge_java(java_file, param, ans):
    for idx in range(len(ans)):
        # java 에서 println 을 쓰면 개행이 되기 때문에 rstrip() 으로 개행 삭제
        submit = execute_java(java_file, param[idx]).rstrip()

        answer = ans[idx]
        print(submit, answer)
        if answer != submit:
            print("틀렸습니다!")
            return -1

    print("맞았습니다!")
    return 1


def compile_java(java_file):
    subprocess.check_call(['javac', java_file])


def execute_java(java_file, param):
    java_class, ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    param = str(param).encode('utf-8')
    stdout, stderr = proc.communicate(param)
    submit = stdout.decode('utf-8')
    return submit


def execute_python(python_file, param):
    cmd = ['python', python_file]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    param = str(param).encode('utf-8')
    stdout, stderr = proc.communicate(param)
    submit = stdout.decode('utf-8')
    return submit


def judge_python(python_file, param, ans):
    for idx in range(len(ans)):
        submit = execute_python(python_file, param[idx]).rstrip()

        answer = ans[idx]

        if answer != submit:
            print("틀렸습니다!")
            return -1

    print("맞았습니다!")
    return 1


def write_file(fileName, fileString, ext):
    text_file = open(fileName + "." + ext, "w")
    n = text_file.write(fileString)
    text_file.close()


def divide_ext(fileString, language, in_, out_):
    if language == "java":
        write_file("Main", fileString, language)
        judge_java("Main.java", in_, out_)
    elif language == "python":
        write_file("test", fileString, language)
        judge_python("test.py", in_, out_)
    else:
        return "error"



files = """import java.util.*;
class Main {
    public static void main(String args[]) {
        Scanner t=new Scanner(System.in);
        String str=t.nextLine();
        System.out.println(str);
    }
}"""

user_answer = ["1", "2", "3", "4", "4"]
real_answer = ["1", "2", "3", "4", "4"]

divide_ext(files, 'java', user_answer, real_answer)

