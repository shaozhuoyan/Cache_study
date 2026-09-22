# 1.学习日志
---
## 9.14
- 理论学习：
    - 学习计算机体系结构 1/35
- 实际工作：
    - 安装了 docker
    - 配置了 gem5 的开发环境
    - 克隆了 gem5 源码

决定明天还是先做了再说，没找到太好的针对一个模块的精讲视频

## 9.15
- 理论学习：
    - 通过AI简单了解了 CPU 与 Cache 
- 实际工作：
    - 构建 gem5
    - 尝试创建配置脚本

## 9.17
- 理论学习：
- 实际工作：
    - 照抄并学习part1的simple与cache代码

## 9.18
- 理论学习
- 实际工作：
    - 照抄并学习了part1的two_level与part2的simple_cache
    - 对Cache进行size参数修改并看了性能指标
    - **一碰到大数组就会导致程序报错，取指令后icache得不到有效地址**
      ```
      反复出现：
      TimingSimpleCPU::sendFetch()
      TimingSimpleCPU::fetch()
      TimingSimpleCPU::completeIfetch()
      报错：
      src/mem/packet.hh:807
      Assertion `flags.isSet(VALID_ADDR)' failed
      ```

## 9.21
- 理论学习
    - ```
      如何观察Cache的性能指标
      1.config.ini文件，表示用了什么配置，
      size
      assoc
      tag_latency
      data_latency
      response_latency
      mshrs
      都是Cache的参数
      2.stats.txt文件，表示运行结果，
      overallHits           命中次数
      overallMisses         缺失次数
      overallMissRate       缺失率
      overallAccesses       总访问次数
      overallMissLatency    缺失总延迟
      simTicks              模拟总时间
      simInsts              模拟执行的命令数
      ```
    - 
- 实际工作：
    - 解决报错ing但是未解决 （有点太过于依赖ai了）
   
## 9.22
- 理论学习
    - 查找文件中特定指标命令：
    - grep -E "simTicks|dcache.overallMissRate|dcache.overallAccesses|dcache.overallMissLatency" m5out/stats.txt
    - 实验发现以下问题
        - 1.发现两种替换算法下，对于顺序大数组的访问中16KiB和8KiB的模拟总时间完全相同：顺序访问模式下，Cache 容量缩小到一定程度以后，性能瓶颈可能不再由容量决定，而由访问模式和硬件预取/空间局部性决定。
        - 2.为什么FIFO比LUT的性能普遍要差一些：因为FIFO只根据数据进入Cache的时间进行替换，无法感知数据的访问频率；而LRU会优先保留最近被访问的数据，能够更好地利用程序的时间局部性，因此减少Cache缺失。
        - 2.1可是我觉得无论是随机，还是顺序，都是跟取用频率无关的，尤其是顺序，我访问了第一个，接下来就不会再访问第一个了，所以LUR是完全没有用的呀，但是此时LUR依旧是比FIFO好：！！因为除了数组以外，还有栈、printf相关数据等小数据以及指令缓存，所以LUR还是能够比FIFO发挥更多的作用
- 实际工作
    - 解决了问题，把一级指令缓存的参数调大了似乎就行了
    - 做完了实验


PS:还有两个方向没有解决：一个是出的问题，一个是二级cache的影响，我们只分析了一级的
     



# 2.常用命令
--- 
| 代码 | 含义 |
|:---:|:---:|
|`nproc`|   #CPU线程数
|`lscpu`|  #CPU核心数
|`free -h`|#查看内存
|`mkdir xxx`|  #创建文件夹
|`touch xxx.py`|  #创建文件
|`rm xxx.py`|   #删除文件
|`cd`|      #进入目录
|`cd ..`|   #返回上级
|`ls`|      #查看文件夹目录
|`cat`|     #查看文件内容
|`git describe`|  #查看gem5版本
|`./ 文件名`|   #表示运行当前文件夹下的程序
|`file 文件名`|  #检查这个文件是不是一个合法的Linux程序
