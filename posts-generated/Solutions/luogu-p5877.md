## 前言

~~蒟蒻来水题解啦~~

## Description

给定一个 <img src="https://www.zhihu.com/equation?tex=N * N" alt="N * N" class="ee_img tr_noresize" eeimg="1"> 的矩阵中的 <img src="https://www.zhihu.com/equation?tex=M" alt="M" class="ee_img tr_noresize" eeimg="1"> 个点，求这些点中的连通块数量。

## Solution

~~正常人~~看到这道题的第一反应应该是广搜吧。但是，很明显使用 BFS 会超时：我们需要求 <img src="https://www.zhihu.com/equation?tex=M" alt="M" class="ee_img tr_noresize" eeimg="1"> 次连通块的数量。

那么怎么办呢？~~凉拌蒟蒻！~~ 我们可以使用 **二维并查集** 进行统计。

为什么我们可以使用并查集呢？我们可以把一个连通块想象成一个树，新加进来（或与其相邻的）的节点都是它的子节点。那么，这棵树的根就是这个连通块在并查集里的祖先。

那还剩下一个问题。二维并查集这么搞？

其实我们不需要真正创建一个二维的并查集。我们可以把这个矩阵进行压缩，使其成为一个我们~~喜闻乐见~~熟悉的一维并查集。

那么，对于一个点 <img src="https://www.zhihu.com/equation?tex=(x, y)" alt="(x, y)" class="ee_img tr_noresize" eeimg="1"> ，它在并查集数组中的下标应该是 <img src="https://www.zhihu.com/equation?tex=x \times N + y" alt="x \times N + y" class="ee_img tr_noresize" eeimg="1"> 。

然后，对于每个新添加的节点，我们都会检测它上、下、左、右四个方位有没有相同颜色的节点。如果有，那么继续判断该节点是否跟当前节点为同一个祖先。如果不是，那么我们将它们合并，使其祖先同一。

## Code

下面，让大家来看看这个蒟蒻~~难看的~~代码啦~

```cpp
#include <iostream>
#include <cstdio>
using namespace std;
const int N = 510, M = N * N;  // M是最多的矩阵的点数

int n, m, father[M], a[N][N], ans;  // father数组存储每个节点祖先，a数组用于存储每个节点的颜色，ans变量为当前连通块的数量
int dx[] = {0, 0 ,1, -1}, dy[] = {1, -1, 0, 0};  // 类似BFS，上下左右四个点的偏移量

int Find(int x) {  // 查询祖先
    if (father[x] == x) return x;  // 如果祖先是自己，返回
    return father[x] = Find(father[x]);  // 否则递归查找
}

void Union(int u, int v) {  // 合并节点
    int fu = Find(u), fv = Find(v);  // 获取祖先
    if (fu != fv) father[fu] = fv, ans--;  // 如果祖先不同，那么合并，并且连通块数量 - 1
}

int main() {
    scanf("%d%d", &n, &m);
    for (int i = 1; i < M; i++) father[i] = i;  // 初始化并查集，每个节点的祖先都是自己（即默认有M个连通块）
    for (int i = 1; i <= m; i++) {
        int c, x, y;
        scanf("%d%d%d", &c, &x, &y);
        a[x][y] = c + 1, ans++;  // c + 1是因为C++默认数组初始是0，与默认值区分开
        for (int i = 0; i < 4; i++) {  // 循环4个方位
            int nx = x + dx[i], ny = y + dy[i];  // 当前新的节点坐标
            if (a[nx][ny] != a[x][y]) continue;  // 如果不是同一个颜色那就没必要合并了
            Union(nx * n + ny, x * n + y);  // 合并节点，判断祖先的操作在Union函数里
        }
        printf("%d\n", ans);  // 输出当前连通块数量
    }
    return 0;  // 完美结束！
}
```