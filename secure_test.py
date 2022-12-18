import ctypes
import os
import resource
import signal
import platform
import subprocess
import sys
import time
import execute


def fib(n):
    if (n <= 1): return 1
    return fib(n - 1) + fib(n - 2)


class user_regs_struct(ctypes.Structure):
    _fields = [
        ("r15", ctypes.c_ulonglong),
        ("r14", ctypes.c_ulonglong),
        ("r13", ctypes.c_ulonglong),
        ("r12", ctypes.c_ulonglong),
        ("rbp", ctypes.c_ulonglong),
        ("rbx", ctypes.c_ulonglong),
        ("r11", ctypes.c_ulonglong),
        ("r10", ctypes.c_ulonglong),
        ("r9", ctypes.c_ulonglong),
    ]


def set_resource_limit(time_limit, memory_limit):
    time_limit = time_limit  # second
    memory_limit = memory_limit * 1024 * 1024  # mb to byte

    print(memory_limit)
    resource.setrlimit(resource.RLIMIT_CPU, (time_limit, time_limit + 1))

    #resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    # m1 mac 의 경우, memory_limit 을 정상적으로 못 읽어오는듯..! 도커에서 리눅스 환경에선 돌아감.
    # 윗 줄 주석 하고 테스트 해야할 듯

    resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024, 64 * 1024))  # 64 KB


def execute_secure(fileString, language, sample_data):
    child = os.fork()
    if child == 0:
        set_resource_limit(5, 256)
        answer = execute.judge_file(fileString, language, sample_data)

    else:
        answer = True
        while True:
            _, status, rusage = os.wait4(child, 0)
            _status = status
            _rusage = rusage

            if os.WIFEXITED(status):
                answer = False
                break
            if os.WIFSTOPPED(status):
                if os.WSTOPSIG(status) == signal.SIGXCPU:
                    print('time limit exceed')
                    os.kill(child, signal.SIGXCPU)
                    answer= False
                    break
                elif os.WSTOPSIG(status) == signal.SIGSEGV:
                    print('memory limit exceed')
                    os.kill(child, signal.SIGSEGV)
                    answer= False
                    break
                elif os.WSTOPSIG(status) == signal.SIGXFSZ:
                    print('output limit exceed')
                    os.kill(child, signal.SIGXFSZ)
                    answer= False
                    break

            if os.WIFSIGNALED(status):
                print("runtime error :", status)
                answer= False
                break

    return answer

            # regs = user_regs_struct()
            # ptrace(12, child, None, ctypes.byref(regs))

            # syscallcount[regs.orig.rax] += 1

            # ptrace(24, child, None, None)


example_data_python = {
    "language": "Python",
    "code": '''
import sys

a = 0
while True:
    a = a + 1
    
sys.setrecursionlimit(10 ** 8)

N, M = list(map(int, input().split()))

arr = [[] for i in range(N)]
visit = [-1 for i in range(N)]
visitIndex = [[i] for i in range(N)]
rel = [list(map(int, input().split())) for _ in range(M)]

for idx in range(len(rel)):
    _sender = rel[idx][0] - 1
    _receiver = rel[idx][1] - 1
    arr[_receiver].append(_sender)
    visitIndex[_sender].append(_receiver)


def search(idx):
    if visit[idx] > -1:
        return visit[idx]

    sum = len(arr[idx])
    for number in arr[idx]:
        if number in visitIndex[idx]:
            continue
        sum += search(number)
    visit[idx] = sum
    return sum


max = [0]
for idx in range(len(visit)):

    new = search(idx)
    if idx == 0:
        continue
    if visit[max[len(max) - 1]] < new:
        max = [idx]
    elif visit[max[len(max) - 1]] == new:
        max.append(idx)

for n in range(len(max)):
    max[n] += 1
print(*max)

''',
    "samples_text": [
        {
            "input": "5 4\n3 1\n3 2\n4 3\n5 3\n",
            "output": "1 2"
        },
    ]
}

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
    public static void main(String[] args) {
		int input = 800000000; // 8개 출력
		
		for (int i = 1; i <= input; i++) {
			System.out.println(fibo(i));
		}
	}

	public static int fibo(int n) {
		if (n <= 1)
			return n;
		else 
            return fibo(n-2) + fibo(n-1);
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

# judge_file(example_data_java["code"], example_data_java["language"], example_data_java["samples_text"])
# execute_secure(example_data_python["code"], example_data_python["language"], example_data_python["samples_text"])
