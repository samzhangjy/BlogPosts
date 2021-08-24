## 前言

蒟蒻的第一篇题解，好激动 qwq

## Description

题目很简单，就是有 $N$ 头大象想要站在一个总承重量为 $W$ 的蜘蛛网上（好神奇 qwq）。其中，第 $i$ 头大象的重量是 $w_i$ 。求最多蜘蛛网上能站多少头大象。

其实就是把数组升序排序，并统计累加即可。

## Solution

算法方面，这个蒟蒻刚学到堆，便想用小根堆解决这个问题。

我们使用优先队列建立一个小根堆，然后在小根堆中进行排序（C++ 的 `priority_queue` 会自动进行堆的 up 和 down 操作）。

然后我们在没有累加到 $W$ 的时候一直累加堆顶并弹出堆顶即可。

## Code

```cpp
#include <iostream>
#include <queue>
using namespace std;

priority_queue <int, vector <int>, greater<int> > q;  // 小根堆
int n, m, w, tmp;  // n是测试点数量，m有几头象，w蜘蛛网总承重量

int main() {
    cin >> n;
    while (n--) {  // 方便
        int ans = 0, cnt = 0;  // ans最终数量，cnt累加器
        cin >> m >> w;
        for (int i = 0; i < m; i++) {
            cin >> tmp;
            q.push(tmp);  // 每次输入都直接入队
        }
        while (!q.empty() && cnt + q.top() <= w) {  // 堆非空并且蜘蛛网还能装
            cnt += q.top(), ans++;  // 计数器累加
            q.pop();  // 弹出堆顶
        }
        while (!q.empty()) q.pop();  // 清空堆，为下一次排序做准备
        cout << ans << endl;  // 输出ans
    }
    return 0;  // 完美结束
}
```

QwQ，欢迎各位 dalao 指出错误！
