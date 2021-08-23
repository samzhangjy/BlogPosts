# 括号匹配 题解

## <img src="https://www.zhihu.com/equation?tex=Description" alt="Description" class="ee_img tr_noresize" eeimg="1">

给定一个长度为<img src="https://www.zhihu.com/equation?tex=n" alt="n" class="ee_img tr_noresize" eeimg="1">的，由若干个`{`和`}`组成的括号串<img src="https://www.zhihu.com/equation?tex=s" alt="s" class="ee_img tr_noresize" eeimg="1">，并给定一个整数<img src="https://www.zhihu.com/equation?tex=p" alt="p" class="ee_img tr_noresize" eeimg="1">，求与<img src="https://www.zhihu.com/equation?tex=s_p" alt="s_p" class="ee_img tr_noresize" eeimg="1">匹配的另一个左 / 右括号<img src="https://www.zhihu.com/equation?tex=s_k" alt="s_k" class="ee_img tr_noresize" eeimg="1">的位置<img src="https://www.zhihu.com/equation?tex=k" alt="k" class="ee_img tr_noresize" eeimg="1">。

## <img src="https://www.zhihu.com/equation?tex=Algorithm" alt="Algorithm" class="ee_img tr_noresize" eeimg="1">

一眼看上去，欸，这不是栈的板子题吗？只不过从判断括号串合不合法变成了找到与一个括号匹配的另一个括号罢了。于是，我们先来讲一下未经更改的板子题：洛谷[P1739](https://www.luogu.com.cn/problem/P1739)。

### <img src="https://www.zhihu.com/equation?tex=Prerequisites" alt="Prerequisites" class="ee_img tr_noresize" eeimg="1">

- 栈

### 原版括号匹配

题目内容我就不在此阐述了，大致意思就是让你去判断一个表达式里面的所有括号能不能匹配上并且合法（只包括小括号）。

我们可以用`栈`来达到这一点。

假设我们有这个括号序列：<img src="https://www.zhihu.com/equation?tex=(())" alt="(())" class="ee_img tr_noresize" eeimg="1">。很明显，它是合法的。但是，让程序也明白这一点，我们需要更详细的解释。

如果要使括号序列<img src="https://www.zhihu.com/equation?tex=s" alt="s" class="ee_img tr_noresize" eeimg="1">内的所有括号匹配，肯定左括号的数量跟右括号的数量要相等。但是，例如<img src="https://www.zhihu.com/equation?tex=)()(" alt=")()(" class="ee_img tr_noresize" eeimg="1">这样的括号序列当然也不行。怎么办呢？这时候就需要用到`栈`了。

首先，我们输入一个括号<img src="https://www.zhihu.com/equation?tex=p" alt="p" class="ee_img tr_noresize" eeimg="1">。如果它是左括号，那么我们直接把它压入栈；否则，它就是右括号。我们需要对右括号进行如下判断：

1. 若栈顶为空，则代表这个括号不匹配，致使整个序列不合法。我们可以直接输出`NO`并结束程序；
2. 若栈顶非空且栈顶为`(`，那么这是一对匹配的括号，可以弹出栈顶并继续循环；
3. 因为右括号从未入栈，所以不存在栈顶为右括号的情况。

于是，我们就可以判断括号是否匹配……了？

不，其实不行。在循环结束后，我们还需要判断当前栈顶是否为空。栈空才代表括号匹配完毕，否则就有多余的左括号。

现在，我们做完了这道板子题。代码就不放了，大家应该可以根据文字描述写出代码。

### 步入正题

好了，现在我们该回过头来看看这道题了。现在看上去，这道题是不是特别板子了呢？

我们还是需要一个栈来维护我们的括号序列。

跟上道题一样，我们要把碰到的左括号都压入栈。这时候，当要匹配的括号（<img src="https://www.zhihu.com/equation?tex=s_k" alt="s_k" class="ee_img tr_noresize" eeimg="1">）是左括号的时候，问题就变得相当简单了。我们只需要在遇到第<img src="https://www.zhihu.com/equation?tex=p" alt="p" class="ee_img tr_noresize" eeimg="1">个括号的时候输出与之匹配的左括号的位置即可。

但是，这里还有一个小问题：如何记录括号位置？

我使用的是结构体来存储：

```cpp
struct brace {
    char c;  // 括号本身的字符（左大括号或右大括号）
    int id;  // 括号的位置
};
```

问题就迎刃而解了。

然后，我们可以来看看下一个问题：如何匹配右括号？其实也同样简单。在每次输入的是右括号的时候，我们都判断与之匹配的与之匹配的左括号id是否为<img src="https://www.zhihu.com/equation?tex=p" alt="p" class="ee_img tr_noresize" eeimg="1">即可。

但是，还有最后一个问题：怎么判断该匹配的括号是左括号还是右括号？

因为题目给定的括号串是合法的，所以左括号只可能在与之匹配的右括号前面。所以，每次遇到左括号的时候，我们都判断它的id是否等于<img src="https://www.zhihu.com/equation?tex=p" alt="p" class="ee_img tr_noresize" eeimg="1">，若等于则打上标记，代表我们要匹配的是右括号；反之，则是要匹配左括号。

## <img src="https://www.zhihu.com/equation?tex=Code" alt="Code" class="ee_img tr_noresize" eeimg="1">

在这里，为了方便，我使用了STL的`stack`。细节详见注释。

```cpp
#include <iostream>
#include <stack>
using namespace std;

int n, p;
struct brace {
    char c;
    int id;
};
stack <brace> s;  // 要维护的括号栈

int main() {
    char ch;  // 每次要读入的括号字符
    bool flag = 0;  // 标记，0为要匹配左括号，1要匹配右括号
    cin >> n >> p;
    for (int i = 1; i <= n; i++) {  // 输入括号并在线分析
        cin >> ch;
        brace cur; cur.c = ch, cur.id = i;  // 当前括号
        if (ch == '{') {  // 如果当前是左括号
            s.push(cur);  // 压入栈
            if (i == p) flag = 1;  // 并判断id是不是p，若是则打上标记
        } else if (s.top().c == '{') {  // 否则
            brace top = s.top();  // 栈顶
            if (!flag && i == p) {  // 如果要匹配的是左括号并且当前位置是p
                cout << top.id << endl;  // 输出与之匹配的栈顶id
                return 0;
            } else if (top.id == p) {  // 否则要匹配右括号并需要判断当前栈顶id是不是p
                cout << i << endl;  // 输出与栈顶匹配的当前括号的位置
                return 0;
            }
            s.pop();  // 匹配完毕，弹出栈顶
        }
    }
    return 0;
}
```

Thank you for reading!
