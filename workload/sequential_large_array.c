//编译命令 
//cd /mnt/mydata/Cache_study/workload
//gcc -static sequential_large_array.c -o sequential_large_array   SE模式，所以用静态更稳定

#include <stdio.h>
#include <stdlib.h>

//顺序访问大数组
int main()
{

    int size = 64*1024;         //256kb   //1024*1024;        //1MB等于1024KB，所以这里是4MB
    int *array = malloc(size*sizeof(int));

    if (array == NULL) {        // 防止申请内存失败
        return 1;
    }

    for(int i=0;i<size;i++)
    {
        array[i]=i;
    }

    long sum=0;

    for(int i=0;i<size;i++)
        {
            sum += array[i];
        }
        
    printf("sum=%ld\n",sum);
    free(array);

    return 0;
}
