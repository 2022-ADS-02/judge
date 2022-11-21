import os.path, subprocess
from subprocess import STDOUT, PIPE


def judge_java(java_file, sample_data):
    compile_java(java_file)
    for idx in range(len(sample_data)):
        # java 에서 println 을 쓰면 개행이 되기 때문에 rstrip() 으로 개행 삭제
        print("input : ", sample_data[idx]["input"])
        print("output : ", sample_data[idx]["output"])

        submit = execute_java(java_file, sample_data[idx]["input"]).rstrip().replace("\r", "")
        print('submit : ', submit)
        answer = sample_data[idx]["output"].rstrip().replace("\r", "")
        if answer != submit:
            print("틀렸습니다!")
            return False

    print("맞았습니다!")
    return True


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


def judge_python(python_file, sample_data):
    for idx in range(len(sample_data)):
        print("input:", sample_data[idx]["input"])
        print("output:", sample_data[idx]["output"])
        submit = execute_python(python_file, sample_data[idx]["input"]).rstrip().replace("\r", "")
        print("submit:", submit)
        answer = sample_data[idx]["output"].rstrip().replace("\r", "")

        if answer != submit:
            print("틀렸습니다!")
            return False

    print("맞았습니다!")
    return True


def write_file(fileName, fileString, ext):
    text_file = open(fileName + "." + ext, "w")
    n = text_file.write(fileString)
    text_file.close()


def judge_file(fileString, language, sample_data):
    if language == "Java":
        write_file("Main", fileString, "java")
        return judge_java("Main.java", sample_data)
    elif language == "Python":
        write_file("test", fileString, "py")
        return judge_python("test.py", sample_data)
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

sample = [
    {
        "input": "1\n2\n3\n4\n5\n",
        "output": "1\n2\n3\n4\n5\n"
    },
    {
        "input": "1\n2\n3\n4\n5\n",
        "output": "1\n2\n3\n4\n5\n"
    }
]
example_data_java = {
    "language": "Java",
    "code": '''
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.StringTokenizer;

public class Main {
    static class Node implements Comparable<Node>{
        int idx;
        int age;
        String name;

        public Node(int idx, int age, String name) {
            this.idx = idx;
            this.age = age;
            this.name = name;
        }

        @Override
        public int compareTo(Node o) {
            if (this.age == o.age) {
                return this.idx - o.idx;
            }
            return this.age - o.age;
        }
    }


    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());

        ArrayList<Node> list = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            st = new StringTokenizer(br.readLine());
            int age = Integer.parseInt(st.nextToken());
            String name = st.nextToken();
            list.add(new Node(i, age, name));
        }

        Collections.sort(list);

        for (int i = 0; i < n; i++) {
            Node cur = list.get(i);
            System.out.println(cur.age + " " + cur.name);
        }
    }
}
    ''',
    "samples_text": [
        {
            "input": "3\n21 JunKyu\n21 Dohyun\n20 Sunyoung",
            "output": "20 Sunyoung\n21 JunKyu\n21 Dohyun"
        },
    ]
}

example_data_python = {
    "language": "Python",
    "code": '''import sys

sys.setrecursionlimit(10 ** 8)

N = int(input())
parent = [*map(int, input().split())]
Remove = int(input())

childs = [[] for _ in range(N)]

rootNode = 0
rootNodeComplete = False
for idx in range(len(parent)):
    if parent[idx] == -1 and not rootNodeComplete:
        rootNode = idx
        rootNodeComplete = True
        continue
    childs[parent[idx]].append(idx)

for idx in range(len(childs)):
    if Remove in childs[idx]:
        childs[idx].remove(Remove)


def search(idx):
    sum = 0
    if len(childs[idx]) == 0:
        return 1
    else:
        for i in range(len(childs[idx])):
            sum += search(childs[idx][i])
        return sum

if Remove == rootNode:
    print(0)
else:
    print(search(rootNode))
exit(0)
''',
    "samples_text": [
        {
            "input": "5\n-1 0 0 1 1\n2",
            "output": "2"
        },
        {
            "input": "5\n-1 0 0 1 1\n1",
            "output": "1"
        },
        {
            "input": "5\n-1 0 0 1 1\n0",
            "output": "0"
        }
    ]
}

# Sample Data Code
# example_data_java & example_data_python

# judge_file(example_data_python["code"], example_data_python["language"], example_data_python["samples_text"])

# judge_file(example_data_java["code"], example_data_java["language"], example_data_java["samples_text"])
