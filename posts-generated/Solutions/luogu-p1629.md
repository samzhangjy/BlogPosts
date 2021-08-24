# 邮递员送信 题解

[原题](https://www.luogu.com.cn/problem/P1629)

## Description

给定一个图，求正向最短路与反向最短路。

## Partial Score

首先，乍一看这个题目，咦？这不是多源最短路吗？Floyd直接 <img src="https://www.zhihu.com/equation?tex=O(n^3)" alt="O(n^3)" class="ee_img tr_noresize" eeimg="1"> 怼呗！于是，就有了下面这个<img src="https://www.zhihu.com/equation?tex=40pts" alt="40pts" class="ee_img tr_noresize" eeimg="1">的Floyd代码：

```cpp
#include <iostream>
#include <memory.h>
using namespace std;
const int N = 1010;

int g[N][N], n, m, u, v, w, ans = 0;

void floyd() {  // Floyd多源最短路
    for (int k = 1; k <= n; k++) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                g[i][j] = min(g[i][j], g[i][k] + g[k][j]);
            }
        }
    }
}

int main() {
    memset(g, 0x3f, sizeof(g));
    cin >> n >> m;
    for (int i = 1; i <= n; i++) g[i][i] = 0;  // 初始化
    for (int i = 1; i <= m; i++) {
        cin >> u >> v >> w;
        g[u][v] = min(g[u][v], w);  // 判重边
    }
    floyd();
    for (int i = 2; i <= n; i++) {
        ans += g[1][i] + g[i][1];  // 模拟累加
    }
    cout << ans << endl;
    return 0;
}
```

当然，这个方法是不可行的。对于<img src="https://www.zhihu.com/equation?tex=100\%" alt="100\%" class="ee_img tr_noresize" eeimg="1">的数据，<img src="https://www.zhihu.com/equation?tex=n \leq 10^3" alt="n \leq 10^3" class="ee_img tr_noresize" eeimg="1">，<img src="https://www.zhihu.com/equation?tex=m \leq 10^5" alt="m \leq 10^5" class="ee_img tr_noresize" eeimg="1">！我们需要一个更优的算法。

## Solution

于是 - 我们的救星：Dijkstra来了！

为什么我们能够使用Dijkstra呢？Dijkstra不是只能处理单源最短路嘛？其实，我们可以将这个题目转换成单源最短路。

题目说，我们必须到达一个点后再返回起点。我们的权重也就等于从起点到点<img src="https://www.zhihu.com/equation?tex=x" alt="x" class="ee_img tr_noresize" eeimg="1">的权重 + 从点<img src="https://www.zhihu.com/equation?tex=x" alt="x" class="ee_img tr_noresize" eeimg="1">再回到起点的权重。那么，根据加法交换律，我们可以先计算从起点到各个目的地的权重，然后再计算从各个目的地到起点的权重！

可能看到这，又有人会问了：各个目的地到起点的总权重不还是多源最短路吗？别急，我这就讲。

既然我们需要计算从各个目的地到起点的权重，也就是“多对一”，那为什么我们不能也做成“一对多”呢？这样就可以使用Dijkstra了。

我们当然可以。把每条边反过来就好啦！原来是从 <img src="https://www.zhihu.com/equation?tex=u_i \rarr v_i" alt="u_i \rarr v_i" class="ee_img tr_noresize" eeimg="1"> 的一条边，经过我们的反向建边之后，就可以很容易的变为 <img src="https://www.zhihu.com/equation?tex=v_i \rarr u_i" alt="v_i \rarr u_i" class="ee_img tr_noresize" eeimg="1"> 。这样，我们从起点开始跑Dijkstra就可以轻松获得从各个目的地到达起点的总权重了！

那么问题来了：怎么反向建边呢？

其实很简单。我们可以先把每条边记录在数组里：`u[], v[], w[]`，然后先正向建边，跑一遍Dijkstra。跑完之后，我们再根据数组建立 <img src="https://www.zhihu.com/equation?tex=v_i \rarr u_i" alt="v_i \rarr u_i" class="ee_img tr_noresize" eeimg="1"> 这条边就很容易啦！

下面我来简单说说几个坑点。

### 避坑指北

1. 最大的坑点就是可能有同学忽略了重边的存在。每次进行加边的操作时，都判断邻接表中有没有存储这条边。如果有，那么就取 <img src="https://www.zhihu.com/equation?tex=min(w_i, k)" alt="min(w_i, k)" class="ee_img tr_noresize" eeimg="1"> 。其中， <img src="https://www.zhihu.com/equation?tex=w_i" alt="w_i" class="ee_img tr_noresize" eeimg="1"> 为已经存储的权重，<img src="https://www.zhihu.com/equation?tex=k" alt="k" class="ee_img tr_noresize" eeimg="1">为新的权重。如果没有的话，正常存储即可；
2. 因为我们需要进行两次Dijkstra，所以我们也需要两次的数组初始化以及队列的清空；
3. 本题是稀疏图，使用堆优化的Dijkstra更佳；
4. 每次进行累加权重操作的时候都要从 <img src="https://www.zhihu.com/equation?tex=i = 2" alt="i = 2" class="ee_img tr_noresize" eeimg="1"> 开始，因为目的地分别是 <img src="https://www.zhihu.com/equation?tex=2 \sim n" alt="2 \sim n" class="ee_img tr_noresize" eeimg="1"> ， <img src="https://www.zhihu.com/equation?tex=1" alt="1" class="ee_img tr_noresize" eeimg="1"> 为起点。

## Code

下面封嘴放代码啦。

```cpp
#include <iostream>
#include <cstdio>
#include <algorithm>
#include <memory.h>
#include <queue>
using namespace std;
const int N = 1e3 + 10, M = 1e5 + 10;

int h[N], w[M], vtx[M], nxt[M], idx = 0;  // w存的是权重（花费时间）
int dis[N], vis[N], u[M], v[M], z[M];  // u -> v，权重为z
int n, m, ans;  // ans存储最终累加结果

struct edge {  // 存边的结构体
    int u, v, w;

    friend bool operator < (edge x, edge y) {  // 优先队列比较函数
        return x.w > y.w;
    }
};

priority_queue <edge> q;  // 优先队列（小根堆）

void addEdge(int a, int b, int c) {  // 插入一条边有向带权边 a -> b，权值为c
    int p = h[a], flag = 0;
    while (p != -1) {
        if (vtx[p] == b) {
            flag = 1, w[p] = min(w[p], c);
        }
        p = nxt[p];
    }
    if (flag == 0) {  // 判重
        vtx[idx] = b, nxt[idx] = h[a], w[idx] = c, h[a] = idx++;
    }
}

void dijkstra(int u) {  // 堆优化Dijkstra模板
    dis[u] = 0;
    edge tEdge;
    tEdge.u = u, tEdge.v = u, tEdge.w = 0;
    q.push(tEdge);
    while (!q.empty()) {
        tEdge = q.top();
        q.pop();
        int tmp = tEdge.v;
        if (vis[tmp]) continue;
        vis[tmp] = 1;
        int p = h[tmp];
        while (p != -1) {
            if (!vis[vtx[p]]) {
                if (dis[tmp] + w[p] < dis[vtx[p]]) {
                    dis[vtx[p]] = dis[tmp] + w[p];
                    tEdge.u = tmp, tEdge.v = vtx[p], tEdge.w = dis[tmp] + w[p];
                    q.push(tEdge);
                }
            }
            p = nxt[p];
        }
    }
}

void initialize() {  // 初始化各种数组
    memset(h, -1, sizeof(h));
    memset(vtx, 0, sizeof(vtx));
    memset(nxt, 0, sizeof(nxt));
    memset(w, 0, sizeof(w));
    idx = 0;
    for (int i = 1; i <= n; i++) dis[i] = (2 << 30) - 1;
    memset(vis, 0, sizeof(vis));  // vis数组第二次遍历的时候也要清空
    while (!q.empty()) q.pop();  // 注意：因为要跑两遍Dijkstra，所以记得清空队列
}

void flip() {  // 反转邻接表
    for (int i = 1; i <= m; i++) {
        addEdge(v[i], u[i], z[i]);  // 添加边 v[i] -> u[i]（反向）
    }
}

int main() {
    scanf("%d%d", &n, &m);
    initialize();  // 初始化
    for (int i = 1; i <= m; i++) {  // 读入m条边
        scanf("%d%d%d", &u[i], &v[i], &z[i]);  // 先存下来，一会建立反图的时候还要用
        addEdge(u[i], v[i], z[i]);  // 添加正向边 u[i] -> v[i]
    }
    dijkstra(1);  // 跑一遍正向的Dijkstra
    for (int i = 2; i <= n; i++) ans += dis[i];  // 因为目的地是2 ~ n，所以都要经过，累加即可
    initialize();  // 再为反向图初始化
    flip();  // 反转图
    dijkstra(1);  // 跑一遍反向的Dijkstra
    for (int i = 2; i <= n; i++) ans += dis[i];  // 接着累加回邮局的路程
    printf("%d\n", ans);
    return 0;  // 完美结束！
}
```

## 写在最后

其实这道题是我们老师的一道考试试题，考场上只写出来了Floyd，得了40分。其实也想出来了正解做法，但是处于某些奇奇怪怪的原因一直有bug。转天早上重写了一遍竟然好了。。
