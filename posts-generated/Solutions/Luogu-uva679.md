# 这篇博客已经弃坑
## 前言

就是一堆没有用的话qwq，不想看可以不看

啊我好激动……这是这个蒟蒻的第<img src="https://www.zhihu.com/equation?tex=1" alt="1" class="ee_img tr_noresize" eeimg="1">篇题解！望管理员大大通过~

这道题其实做了很久……后来发现其实变量写倒了……来记录一下吧qwq

~~（高情商解读上面的那句话：我只会写这道题的题解）~~

好了，废话不多说 ~~（说的挺多的啊）~~，直接进入题解。

## <img src="https://www.zhihu.com/equation?tex=Description" alt="Description" class="ee_img tr_noresize" eeimg="1">

首先，我们看向题目。

> 许多的小球一个一个的从一棵满二叉树上掉下来组成一个新满二叉树，在一个时间单位内，一个正在下降的球第一个访问的是非叶子节点。然后继续下降时，或者走右子树，或者走左子树，直到访问到叶子节点。决定球运动方向的是每个节点的布尔值。最初，所有的节点都是`false`，当访问到一个节点时，如果这个节点是`false`，则这个球把它变成`true`，然后从左子树走，继续它的旅程。如果节点是`true`，则球也会改变它为`false`，而接下来从右子树走。满二叉树的标记方法如下图。因为所有的节点最初为`false`，所以第一个球将会访问节点<img src="https://www.zhihu.com/equation?tex=1" alt="1" class="ee_img tr_noresize" eeimg="1">，节点<img src="https://www.zhihu.com/equation?tex=2" alt="2" class="ee_img tr_noresize" eeimg="1">和节点<img src="https://www.zhihu.com/equation?tex=4" alt="4" class="ee_img tr_noresize" eeimg="1">，转变节点的布尔值后在在节点<img src="https://www.zhihu.com/equation?tex=8" alt="8" class="ee_img tr_noresize" eeimg="1">停止。第二个球将会访问节点 <img src="https://www.zhihu.com/equation?tex=1" alt="1" class="ee_img tr_noresize" eeimg="1">、<img src="https://www.zhihu.com/equation?tex=3" alt="3" class="ee_img tr_noresize" eeimg="1">、<img src="https://www.zhihu.com/equation?tex=6" alt="6" class="ee_img tr_noresize" eeimg="1">，在节点<img src="https://www.zhihu.com/equation?tex=12" alt="12" class="ee_img tr_noresize" eeimg="1">停止。明显地，第三个球在它停止之前，会访问节点 1、2、5，在节点 10 停止。现在你的任务是，给定新满二叉树的深度<img src="https://www.zhihu.com/equation?tex=D" alt="D" class="ee_img tr_noresize" eeimg="1">和下落的小球的编号<img src="https://www.zhihu.com/equation?tex=I" alt="I" class="ee_img tr_noresize" eeimg="1">，可以假定<img src="https://www.zhihu.com/equation?tex=I" alt="I" class="ee_img tr_noresize" eeimg="1">不超过给定的新满二叉树的叶子数，写一个程序求小球停止时的叶子序号<img src="https://www.zhihu.com/equation?tex=P" alt="P" class="ee_img tr_noresize" eeimg="1">。

（题目翻译感觉排版有点乱……所以我更改了部分排版）

换成<img src="https://www.zhihu.com/equation?tex=OIer" alt="OIer" class="ee_img tr_noresize" eeimg="1">能听懂的话就是，下面这样（如果不严谨还请纠正QwQ）。

给定一棵深度为<img src="https://www.zhihu.com/equation?tex=D" alt="D" class="ee_img tr_noresize" eeimg="1">的满二叉树，现要求沿节点从上到下遍历该树<img src="https://www.zhihu.com/equation?tex=I" alt="I" class="ee_img tr_noresize" eeimg="1">次，求第<img src="https://www.zhihu.com/equation?tex=I" alt="I" class="ee_img tr_noresize" eeimg="1">次遍历的终点节点编号。对于每次遍历，都会把经过的结点的值取反。具体地，我们规定，若当前节点的值为<img src="https://www.zhihu.com/equation?tex=0" alt="0" class="ee_img tr_noresize" eeimg="1">，则将该节点的值设为<img src="https://www.zhihu.com/equation?tex=1" alt="1" class="ee_img tr_noresize" eeimg="1">，并继续沿该节点的左子树遍历；若当前节点的值为<img src="https://www.zhihu.com/equation?tex=1" alt="1" class="ee_img tr_noresize" eeimg="1">，则将该节点的值设为<img src="https://www.zhihu.com/equation?tex=0" alt="0" class="ee_img tr_noresize" eeimg="1">，并沿其右子树继续遍历。特别地，初始时各个节点的值都为<img src="https://www.zhihu.com/equation?tex=0" alt="0" class="ee_img tr_noresize" eeimg="1">。

## <img src="https://www.zhihu.com/equation?tex=Algorithm" alt="Algorithm" class="ee_img tr_noresize" eeimg="1">

显而易见，我们可以对这个问题进行暴力模拟。但是，这显然不是最优解法。由于这个方法各位大佬的题解都很详细了，就不再阐述了。我们来讨论一下更优解。（不知道是不是最优解qwq）

经过枚举观察，我们可以发现：当当前节点遍历次数<img src="https://www.zhihu.com/equation?tex=I" alt="I" class="ee_img tr_noresize" eeimg="1">为奇数时，会向左子树遍历；当<img src="https://www.zhihu.com/equation?tex=I" alt="I" class="ee_img tr_noresize" eeimg="1">为偶数时，会遍历右子树。（有点懒，图就不画了，各位神犇可以去自己动手画一画）

对于每次节点访问，我们都需要求出当前节点遍历过多少次。我们可以发现，每个节点的当前访问次数与当前节点最后一次访问该节点的球的序号有关。并且，当前节点访问次数<img src="https://www.zhihu.com/equation?tex=I_i" alt="I_i" class="ee_img tr_noresize" eeimg="1">有如下规律：

- 若<img src="https://www.zhihu.com/equation?tex=I_{i-1} \pmod{2} = 1" alt="I_{i-1} \pmod{2} = 1" class="ee_img tr_noresize" eeimg="1">，则<img src="https://www.zhihu.com/equation?tex=I_i = \lceil\frac{I_{i-1}}{2}\rceil+1" alt="I_i = \lceil\frac{I_{i-1}}{2}\rceil+1" class="ee_img tr_noresize" eeimg="1">；
- 若<img src="https://www.zhihu.com/equation?tex=I_{i-1} \pmod{2} = 0" alt="I_{i-1} \pmod{2} = 0" class="ee_img tr_noresize" eeimg="1">，则<img src="https://www.zhihu.com/equation?tex=I_i = \frac{I_{i-1}}{2}" alt="I_i = \frac{I_{i-1}}{2}" class="ee_img tr_noresize" eeimg="1">。

为什么奇数的时候要加一呢？

是因为
