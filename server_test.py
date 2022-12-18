import requests

params = {
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

url = 'http://127.0.0.1:9001/judge'
response = requests.post(url=url, json=params)
#response = requests.post(url=url, json=example_data_java)
print(response.json())
