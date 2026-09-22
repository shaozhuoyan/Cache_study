//编译命令 
//cd /mnt/mydata/Cache_study/workload
//gcc -static random_large_array.c -o random_large_array    SE模式，所以用静态更稳定
#include <stdio.h>
#include <stdlib.h>


//随机访问大数组
int main()
{
    int size = 64*1024;            //这里64对应256kb
    int *array = malloc(size*sizeof(int));
    
    if (array == NULL) {        // 防止申请内存失败
        return 1;
    }

    for(int i=0; i<size; i++)
    {
        array[i] = i;
    }

    long sum = 0;

    srand(1);

    for(int i=0; i<size; i++)
        {
            int index = rand()%size;
            sum += array[index];
        }
        
    printf("sum = %ld\n", sum);
    free(array);

    return 0;
}