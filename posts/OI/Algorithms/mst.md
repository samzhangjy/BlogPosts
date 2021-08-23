## 前言

最近刚学了最小生成树，于是想趁热打火，先来总结一下~

### 前置芝士

- 图、树的概念、遍历与存储
- 并查集

本文章所有代码均以`C++`编写。

## 最小生成树的概念

最小生成树（Minimum Spanning Tree, MST）是一种特殊的图。它具备朴素树的所有性质，但也是一张图中边权最小但经过每个节点的子树。

### 定义

> 一个有 $n$ 个结点的连通图的生成树是原图的极小连通子图，且包含原图中的所有 $n$ 个结点，并且有保持图连通的最少的边。最小生成树可以用`Kruskal`（克鲁斯卡尔）算法或`Prim`（普里姆）算法求出。[<sup>\[1\]</sup>](#refer-1)

### 大意

在一张连通图 $G$ 里，有 $n$ 个节点和 $m$ 条边，第 $i$ 条边的权值为 $w_i$ 。我们设图 $G$ 的最小生成树为 $T$ 。

那么，图 $G$ 的最小生成树 $T$ 必须具备以下条件：

- $T$ 必须包括 $G$ 的所有节点；
- $T$ 的边数必须等于 $n - 1$；
- $T$ 的边权和必须在所有生成树中最小；
- $T$ 必须为 $G$ 的子图。

假设我们有如下的连通图 $G$（左），那么它的最小生成树 $T$ 如图所示（右）。

![image.png](https://i.loli.net/2021/08/22/wOfjTEFkBdcz6sW.png)[<sup>\[2\]</sup>](#refer-2)

显然对于图 $G$，$T$ 的边权和在所有生成树中最小。我们称这样的树为图 $G$ 的 **最小生成树**（简称MST）。

## 算法

我们不妨来介绍两种较为常见的求最小生成树的算法。

在介绍算法之前，我们先来看这样一道题目：

![image.png](https://i.loli.net/2021/08/22/5lvUkLOfqRN7xu3.png)

题目链接：[洛谷P3366](https://www.luogu.com.cn/problem/P3366)。

题目很容易理解，即求出给定图的最小生成树边权和。那么，我们来看看这些算法吧！

### Kruskal

#### 基本思路

**Kruskal（克鲁斯卡尔）** 是一种贪心策略，类似图论中的Bellman-Ford算法。

简单来说，如果我们挑选了 $n-1$ 条较小边，那么显而易见，这 $n-1$ 条边的权值相加也会是一个较小值。按照这种思路，我们可以挑选 $n-1$ 条 $G$ 里面最小的边并将它们相连。

但是，你以为这就完了？怎么可能。

显然我们上面的做法有一个缺陷：它虽然保证了边权和最小，但是得出的却并不一定是一棵树。相反，它反而有可能得出来一个图（或森林）。我们需要解决这个问题。

显然，对于一条 $u \leftrightarrow v$ 的无向边，若点 $u$ 和点 $v$ 已经连通（直接或间接），那么我们就不再需要加入当前边了。

对于每次遍历，我们都会对当前边的所到达的节点进行一个排查：如果节点已经连通，则无需加边；否则连接两点。

这样一来，我们就剩下一个最重要的问题没解决了：如何判断两个点有没有连通？

我们可以使用并查集这个数据结构进行存储和判重。每次判断两点的连通性的时候，我们只需要查询他们的祖先是否相同即可。同理，对于每次连接操作，我们只需要进行并查集的合并操作来合并 $u,v$ 两点即可。

#### 参考代码

```cpp
#include <iostream>
#include <cstdio>
#include <algorithm>
using namespace std;
const int N = 2 * 1e5 + 10;

struct edge {  // 存边
    int u, v, w;
} e[N];
edge mst[5010];  // 最小生成树
int vtx[5010], k, ans, n, m;  // vtx并查集数组，k当前最小生成树节点数，ans边权和

bool cmp(edge a, edge b) {
    return a.w < b.w;  // 按照边权排序
}

int Find(int x) {  // 并查集查找操作
    if (vtx[x] == x) return x;
    return vtx[x] = Find(vtx[x]);
}

void Union(int u, int v) {  // 并查集合并操作
    int fu = Find(u), fv = Find(v);
    if (fu != fv) vtx[fv] = fu;
}

void kruskal() {  // Kruskal最小生成树
    for (int i = 0; i < m; i++) {  // 遍历所有边
        if (Find(e[i].u) != Find(e[i].v)) {  // 如果两点没有连接
            k++;  // MST边数++
            mst[k].u = e[i].u, mst[k].v = e[i].v, mst[k].w = e[i].w;  // 记录当前边
            ans += e[i].w;  // 总权重增加
            Union(e[i].u, e[i].v);  // 连接两点
        } 
    }
}

int main() {
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; i++) vtx[i] = i;  // 并查集初始化，祖先都是自己，即每个点都未连接
    for (int i = 0; i < m; i++) scanf("%d%d%d", &e[i].u, &e[i].v, &e[i].w);
    sort(e, e + m, cmp);  // 对边权进行排序
    kruskal();  // 获取MST
    if (k == n - 1) printf("%d\n", ans);  // 如果边数满足条件，输出总权值
    else printf("orz");  // 否则输出orz
    return 0;
}
```

### Prim

#### 基本思路

**Prim（普利姆）** 是Dijkstra的一个扩展。

Prim算法与Dijkstra算法唯一的区别在于：Prim算法所记录的距离并非从某个起点到终点的距离，而是当前的生成树到某个点的最短距离。

其余部分与Dijkstra算法一致。同样，Prim算法也可以使用堆进行优化，以提高效率。

#### 参考代码

待补充。

## 参考资料

<div id="refer-1"></div>

- [最小生成树_百度百科](https://baike.baidu.com/item/%E6%9C%80%E5%B0%8F%E7%94%9F%E6%88%90%E6%A0%91/5223845)

<div id="refer-2"></div>

- [最小生成树的两种方法（Kruskal算法和Prim算法）](https://blog.csdn.net/a2392008643/article/details/81781766)
