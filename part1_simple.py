#照抄part1，逐句了解,这里x86和arm与riscv实际上都一样，只是后边两个不需要把中断通过bus连接CPU和memory
#运行命令：
#cd /mnt/mydata/gem5
#./build/X86/gem5.opt /mnt/mydata/Cache_study/part1_simple_test.py

import m5 #m5是gem5编译以后生成的一套python模块，位于src/python/m5
from m5.objects import * #m5.objects里边是gem5里边所有模拟硬件对象，相当于把所有硬件模型导进来了

#创建一个空的系统
system = System() 
#设置系统时钟域与电压域（1GHz就是每秒10亿次时钟周期）
system.clk_domain = SrcClockDomain() 
system.clk_domain.clock = "1GHz" #不同模块不同时钟域，这里设系统的运行速度为1GHz，指的是如果子模块没有特别设定，那就默认为1GHz
system.clk_domain.voltage_domain = VoltageDomain() #频率与电压有关，高频对应高电压，相当于给时钟域对应一个电压域
#设置系统参数
system.mem_mode = "timing" #设置的是memory访问模型，timing表示的是带时间延迟的内存访问模型
system.mem_ranges = [AddrRange("512MiB")] #设置的是memory空间，划定内存范围是512MB，但是还没有创建内存模型

#创建一个简单的CPU
system.cpu = X86TimingSimpleCPU()     
#创建membus（CPU不能直接连memory，需要bus做数据传输，把CPU的命令传给memctrl）
system.membus = SystemXBar()  #XBar相当于一个系统互联结构，相当于一个支架，给系统各个硬件连接好
#CPU连接bus
system.cpu.icache_port = system.membus.cpu_side_ports #icache存程序指令
system.cpu.dcache_port = system.membus.cpu_side_ports #dcache存数据
#创建中断控制器
system.cpu.createInterruptController()
#仅X86需要，将中断通过bus连接cpu与memory
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

#创建一个内存控制器（CPU不可以直连memory，用接收到CPU命令以后，memctrl根据命令找DRAM里的内容）
system.mem_ctrl = MemCtrl()
#创建DRAM，DDR3是内存类型，1600是数据传输速度，8x8是芯片组织形式
system.mem_ctrl.dram = DDR3_1600_8x8()

system.mem_ctrl.dram.range = system.mem_ranges[0] #右边是前边划定的512MB范围，这句话是把前边划定的512MB分配给DDR3内存
system.mem_ctrl.port = system.membus.mem_side_ports #连接memory controller和bus，把内存控制器连接在总线的内存侧接口
system.system_port = system.membus.cpu_side_ports #让整个系统通过bus访问内存

#加载workload
thispath = os.path.dirname(os.path.realpath(__file__)) #(__file__)表示当前文件路径，os.path.realpath指的是获取绝对路径，os.path.dirname取目录，总体为：获取当前simple.py文件所在的文件夹的路径
binary = os.path.join(             #用于拼接路径，保存的是可执行文件的路径
    thispath,                   #当前文件的文件夹路径
    "../",                #往上返回三级目录
    "gem5/tests/test-progs/hello/bin/x86/linux/hello",  #转到如下新目录，这就是模拟系统要运行的软件
)
#根据我要运行的这个程序，创建合适的系统调用模拟环境。
system.workload = SEWorkload.init_compatible(binary)   #上边要运行的hello就是workload，SE就是系统调用模拟，也就是说用gem5模拟CPU运行一个程序，还有一个叫FS（Full System）模式，就是像真的启动电脑运行。

#创建一个准备运行hello程序的模拟进程
process = Process()
process.cmd = [binary] #告诉process这个进程要运行什么
system.cpu.workload = process  #把程序交给CPU
system.cpu.createThreads()   #给CPU准备运行程序需要的状态

root = Root(full_system = False, system = system) #false表示不用FS模式，用的是SE模式，root是根节点，gem5的所有模拟对象最后都要挂在跟对象下边
m5.instantiate()  #实例化，根据配置把所有硬件真正的建立起来

print(f"Beginning simulation!")
exit_event = m5.simulate()        #真正开始运行
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")  #输出结束原因，tick是模拟时间的意思，是时间的单位，getCause获取推出愿意




