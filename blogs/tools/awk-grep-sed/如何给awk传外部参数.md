在awk中，传参的方式主要有如下两种：  

## 1.用-v传参

```
[xxx@xxx expensive_user]$ A=3
[xxx@xxx expensive_user]$ B=4
[xxx@xxx expensive_user]$ echo | awk -v A=$A -v B=$B '{printf("%.2f\n",A/B)}'
0.75
```  

## 2.在action后传参
这种方式就是在awk的动作语句后面指定参数的值  

```
[xxx@xxx expensive_user]$ A=3
[xxx@xxx expensive_user]$ B=4
[xxx@xxx expensive_user]$ echo |awk '{printf("%.2f\n",A/B)}' A=$A B=$B
0.75
```  

还有通过环境变量传参的方式。但是那种方式我使用的概率非常非常小，所以就不再给大家介绍。  