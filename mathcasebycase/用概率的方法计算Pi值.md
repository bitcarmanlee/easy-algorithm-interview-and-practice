精确计算Pi的值，从古至今都吸引了无数的数学家。迄今为止，科学家还没有计算得出精确的Pi值，也没有发现小数点后面的值有什么规律。  
现在，我们用一种比较简单的概率的方式来近似计算Pi的值。  
二话不说，直接上代码。  

```
public class PiCaculate {

    public static double caculate() {
        Random r = new Random();
        //d1,d2都是从[0,1)的随机浮点数
        double d1 = r.nextDouble();
        double d2 = r.nextDouble();
        double result = Math.sqrt(d1*d1 + d2*d2);
        return result;
    }

    public static void main(String[] args) {
        int count = 0;
        int nums = 100000;
        for(int i=0; i<nums; i++) {
            double result = caculate();
            if(result <= 1.0) {
                count++;
            }
        }
        double pi = 4 * (float)count / (float)nums;
        System.out.println("Pi is: " + pi);
    }
}
```  

将代码run起来：  
```
Pi is: 3.14028000831604
```  

稍微解释一下代码的思路：  
现在假设有一个单位圆，圆点为中心，1为半径。d1,d2为两随机浮点数，取值范围均为[0,1]。假设d1为x坐标，d2为y坐标，如果$x^2+y^2 < 1$，那么该点在圆内；反之则在圆外。由对称性易知，落在圆内的概率为单位圆面积的四分之一，即为Pi/4。  


spark中计算Pi值的demo，我们来看看spark中的源码  

```
from __future__ import print_function

import sys
from random import random
from operator import add

from pyspark import SparkContext


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    sc = SparkContext(appName="PythonPi")
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 < 1 else 0

    count = sc.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    print("Pi is roughly %f" % (4.0 * count / n))

    sc.stop()
```  

可以看出，里面计算Pi的思路，跟我们之前的思路是一样滴！  