# 这里稍微解释一下Cache的原理：是CPU与memory之间的一个小而快的存储，如果CPU像读取一个字节1000，Cache会读取这个字节周围的一整块内容地址1000~1063，64B，这一整块叫数据块（Block） = Cache Line。
# Cache内部不是一整块区域，被划分成Set，一个Set里面都能放几个block。一个set里边有way叫做位置,way=1就是直接映射Cache，way=2就是二路组相联。
# 例如BlockA来了，先确定set，确定以后way0，way1都可以取去，如果只有一路，那再来BlockB的时候就只能把A替换掉了

# CPU给Cache一个地址。例如：1010101111000011...Cache需要知道：这个地址的数据在哪里。所以把地址分三部分：| Tag | Index | Offset |，Index决定：去哪个Set。
# Offset表示：Block里面的位置。比如：Cache Line：64 Bytes。CPU访问：1010。那么Offset告诉：它是Block里面第10个字节。Tag用来确认：是不是我要的数据。不同Memory地址可能映射到同一个Set。所以需要Tag验证。

# mhrcs解释：CPU访问Cache：如果数据在Cache：叫：hit（命中）直接返回。如果不在：叫：miss（缺失）需要去Memory取：
# 那如果Cache正在等待Memory返回的时候，又来了新的请求怎么办？CPU连续访问：ABCD，结果：A miss、B miss、C miss、D miss 如果Cache只能等A：那么：B、C、D全部堵住。所以Cache里面需要一个“小表”：记录：哪些数据正在等待Memory返回。这个东西叫：MSHR全称：Miss Status Holding Register中文：缺失状态保持寄存器。

# tgts_per_mshr解释：一个Memory Block可能被多个请求需要。例如：CPU：第一次访问：A发现miss：但是Memory还没回来。这时候：CPU又访问A。怎么办？难道再去Memory请求一次？不需要。因为：已经有人在取A了。所以：第二个请求可以挂在这个MSHR下面。

# def __init__解释：Python规定：如果一个类里面有：def __init__(self):    那么当：对象名 = 类名()时：    Python自动调用它。
# 如果：一个类里面有：def __init__(self):    那么当：对象名 = 类名()时：，相当于self就等价于对象名


import m5
from m5.objects import *    #位于src/python/m5

m5.util.addToPath("../gem5/configs")   #这一句是为了让python找到common，这里是给python加了一个额外的搜索路径。这个新搜索路径是根据你写代码的文件夹在哪来找到的。接下里的文件引入就有两个搜索路径了，可以在代码文件夹下，也可以在新加的搜索路径下
from common import SimpleOpts    #位于configs/common,common是方便写gem5配置脚本提供的“工具箱”，SimpleOpts作用是允许你在运行 gem5 时，通过命令行修改配置参数，而不用直接改 Python 文件

class L1Cache(Cache):   #定义一个新的类，L1 Cache是类的名字，它继承 gem5 已经提供好的 Cache 模型。Cache位于gem5/src/mem/cache/
    """Simple L1 Cache with default values"""        #docstring（文档字符串）给这个类写的说明文字。这种特殊注释会python运行的时候被显示出来


    assoc = 2                          #代表Cache的组织方式，这个是二路组相联
    tag_latency = 4    #2                #tag查找延迟：需要两个cache周期，周期就是这个模块对应的时钟周期
    data_latency = 4      #2             #data查找延迟（也就是根据offset把数据提取出来这步），确定数据位置以后2个周期
    response_latency = 4  #2             #数据准备好以后返回CPU的时间
    mshrs = 8            #4               #所以这里就代表这个MSHR这个表最多同时记录四个未完成的请求
    tgts_per_mshr = 64   #20                 #一个miss记录最多支持20个等待者
    replacement_policy = FIFORP()                  #具体的代码在gem5/src/mem/cache/replacement_policies/ReplacementPolicies.py 命名格式参照这个文件
    def __init__(self, options=None):  #options=None表示：可以接受外部参数。
        super().__init__()             #因为我的类是class L1Cache(Cache): 是继承的Cache，所以L1Cache有：父类Cache的东西。创建L1Cache时：必须先初始化父类。而super（）就表示调用父类，即为super().__init__() 就可以表示为Cache.__init__()
        pass                           #函数里边什么都没有的时候就需要加pass，但是这里显然有一行，所以这里的pass没有意义

    def connectBus(self, bus):         #定义一个函数，把Cache连接到bus
        """Connect this cache to a memory-side bus"""   
        self.mem_side = bus.cpu_side_ports        #port被封装在Cache里边了，Cache与CPU是一个整体，Cache和mem是通过bus连接的，所以Cache的mem_side连接的就是bus端的cpu_side接口

    def connectCPU(self, cpu):         #L1Cache这个父类不知道怎么连接CPU，它不知道自己是什么Cache。L1 Instruction Cache 需要：cpu.icache_port，L1 Data Cache需要：cpu.dcache_port。所以让子类决定。
        """Connect this cache's port to a CPU-side port
        This must be defined in a subclass"""
        raise NotImplementedError         #程序运行过程中，如果遇到：raise XXXPython会：停止当前函数执行，报出一个错误，告诉用户：“这里出问题了”。NotImplementedError：这是一个错误异常类型，这个报错表示函数还没有具体实现，无法直接使用


class L1ICache(L1Cache):                #子类继承父类的默认参数（default values）
    """Simple L1 instruction cache with default values"""

    # Set the default size
    size = "64KiB"  #"16KiB"                    #设置默认大小，icache与dcache通常不一样

    SimpleOpts.add_option(           #调用SimpleOpts，允许用户运行时修改L1iCache的大小
        "--l1i_size", help=f"L1 instruction cache size. Default: {size}"       #--l1i_size表示命令行中提供的一个参数的名称，属于可选参数，可以赋值的，help是对这个选项写说明，f"是用来打印的。整体命令就是：我增加一个命令行参数叫--l1i_size，它用于修改L1指令缓存大小。
    )

    def __init__(self, opts=None):
        super().__init__(opts)
        if not opts or not opts.l1i_size:    #not opts表示没有传入参数，参数就是函数（）里面的东西。例如调用函数的时候cache = L1ICache()，就是没有opt，如果是cache = L1ICache(my_options)，那么就是有参数
            return                           #退出函数，不返回值，直接结束初始化。执行cache=L1ICache()这个过程叫做初始化。大体的流程是，cache=L1ICache()调用一个函数，然后初始化父类，因为opts=None，所以执行return，结束程序，默认size是16kb
        self.size = opts.l1i_size

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU icache port"""
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    """Simple L1 data cache with default values"""

    # Set the default size
    size = "16KiB"

    SimpleOpts.add_option(
        "--l1d_size", help=f"L1 data cache size. Default: {size}"
    )

    def __init__(self, opts=None):
        super().__init__(opts)
        if not opts or not opts.l1d_size:
            return
        self.size = opts.l1d_size

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU dcache port"""
        self.cpu_side = cpu.dcache_port 


class L2Cache(Cache):
    """Simple L2 Cache with default values"""

    # Default parameters
    size = "64KiB"     #"256KiB"
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    replacement_policy = FIFORP()
     
    SimpleOpts.add_option("--l2_size", help=f"L2 cache size. Default: {size}")

    def __init__(self, opts=None):
        super().__init__()
        if not opts or not opts.l2_size:
            return
        self.size = opts.l2_size

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports   #这里连接的是L1Cache的bus的mem端

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports


