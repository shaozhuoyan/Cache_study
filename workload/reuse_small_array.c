//编译命令 
//cd /mnt/mydata/Cache_study/workload
//gcc -static reuse_small_array.c -o reuse_small_array    SE模式，所以用静态更稳定

#include <stdio.h>

//重复访问小数组
int main ()
{
    int size = 2048;    //int对应4byte，1024byte = 1KB，所以这里对应了8KB
    int array[size];

    for(int i=0; i<size; i++)
    {
        array[i] = i;
    }

    long sum = 0;
    
    for(int r=0; r<10; r++)
    {
        for(int i=0; i<size; i++)
        {
            sum += array[i];
        }
    }
    
    printf("sum = %ld\n", sum);

    return 0;
}