所有工作均在这里，未对gem5做出改动
---
# 1.文件内容
## part1、part2前缀文件
都是照抄的gem5/configs/learning_gem5中的代码
我用的是part1_two_simple和part1_caches这两个文件，搭建的二级缓存系统

## workload 文件夹
写了重复访问小数组，顺序访问大数组与随机访问大数组，并且进行了编译。
编译后的文件，大数组中64后缀的对应数组是64*1024大小的，无后缀的是1024*1024大小的目前一运行就报错还没解决

## goal_and_result 文件夹
是任务目标，结果与进度追踪

## _pycache_ 文件夹
自动生成的

# 2.目录结构
文件和 gem5 放在同一个目录下：
```text
mydata/
├── gem5/
└── Cache_study/
```

# 3.问题
在大数组大小达到1024*1024，或者小数组重复运行100次的时候，系统就会报错。
报错：
      src/mem/packet.hh:807
      Assertion `flags.isSet(VALID_ADDR)' failed
我了解后说是指令取指令这里有问题，就是CPU的指令到L1 icache这一步，icache发现这个指令的地址无效，然后就卡住了

已经通过调大ICACHE的各种参数来解决，但具体什么样的参数对应多大的运算量还未计算）