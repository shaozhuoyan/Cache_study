建议边做项目的同时学习git使用，c++基础语法，基本的cpu知识。（一定是边做边学，不要学完了在做项目）

## 一个小项目

learning 中的 cache：

1、先把官方 SimpleCache 跑起来

2、做一个非常小的 Cache 实验，自己写一个几十行的 C/C++ workload，例如顺序访问数组、重复访问小数组、随机访问大数组，然后改变 Cache Size，观察性能参数的变化。

3、修改这个cache，比如把它的替换算法从random改成fifo。

（借助ai学习，但是一开始建议自己也要手敲一遍）

## gem5

gem5项目地址：https://github.com/gem5/gem5 ,在仓库中configs下有learning gem5文件夹

learning gem5官方教程：https://www.gem5.org/documentation/learning_gem5/introduction/



理解在gem5中建模的方法之后，深入理解gem5：https://dingfen.github.io/2022/02/24/2022-2-24-gem5-1/

这里有一些gem5一些列的博客：https://zybzzz.github.io/ybsite/notes/sim/gem5/arch.html



## cpu arch

目前这个小项目是做cache，可以先去找资料了解cache，cpu

之后如果真的要做这个，可以通过一些书去系统的了解。从 单核顺序 到 单核乱序 到 多核。然后软件（编译），硬件（cpu gpgpu）都是有很多内容，后面会推荐一些书。目前先不细说。