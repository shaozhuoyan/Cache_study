#运行命令
#cd /mnt/mydata/gem5
#./build/X86/gem5.opt /mnt/mydata/Cache_study/part1_two_level.py
#更改运行程序与大小
#./build/X86/gem5.opt /mnt/mydata/Cache_study/part1_two_level.py /mnt/mydata/Cache_study/workload/reuse_small_array
#./build/X86/gem5.opt /mnt/mydata/Cache_study/part1_two_level.py --l1d_size 4KiB /mnt/mydata/Cache_study/workload/reuse_small_array

#./build/X86/gem5.opt /mnt/mydata/Cache_study/part1_two_level.py --l1d_size 4KiB /mnt/mydata/Cache_study/workload/random_large_array64
#./build/X86/gem5.opt /mnt/mydata/Cache_study/part1_two_level.py --l1d_size 4KiB /mnt/mydata/Cache_study/workload/sequential_large_array64

import m5
from m5.objects import *          #位于src/python/m5
m5.util.addToPath("../gem5/configs")  #因为part1_caches就用到了common，所以最好把addToPath移到前边来，但是影响不大
from part1_caches import *
from common import SimpleOpts


#这里加载workload提前了
thispath = os.path.dirname(os.path.realpath(__file__)) #(__file__)表示当前文件路径，os.path.realpath指的是获取绝对路径，os.path.dirname取目录，总体为：获取当前simple.py文件所在的文件夹的路径
default_binary = os.path.join(             #用于拼接路径，保存的是可执行文件的路径
    thispath,                   #当前文件的文件夹路径
    "../",                #往上返回三级目录
    "gem5/tests/test-progs/hello/bin/x86/linux/hello",  #转到如下新目录，这就是模拟系统要运行的软件
)

SimpleOpts.add_option("binary", nargs="?", default=default_binary)   #binary同样也是命令名字，属于位置参数；nargs：number of arguments表示这个参数需要几个值，这里是个？表示这个参数可写可不写
#这句话相当于告诉CPU要运行的是什么程序，如果不写，那么就是默认的default_binary，如果写了那就是你写的那个程序
args = SimpleOpts.parse_args()       #相当于args是一个参数的集合，然后里边有很多参数的名字，比如说binary或者是--l1i_size，这个有名字的参数都有自己对应的值。args就负责保存这些

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing" 
system.mem_ranges = [AddrRange("512MiB")]

system.cpu = X86TimingSimpleCPU()
system.cpu.icache = L1ICache(args)
system.cpu.dcache = L1DCache(args)
system.cpu.icache.connectCPU(system.cpu)  #放到前边的函数里，self就是system.cpu.icache，cpu就是system.cpu
system.cpu.dcache.connectCPU(system.cpu)
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache = L2Cache(args)
system.l2cache.connectCPUSideBus(system.l2bus)

system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(args.binary)

process = Process()
process.cmd = [args.binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")