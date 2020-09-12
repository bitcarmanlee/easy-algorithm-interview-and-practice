打扑克牌，打麻将的时候，都会有洗牌这个动作。洗牌问题其实很简单，如果有一个数组中有n个元素，怎样设计一个洗牌(shuffle)算法保证随机性。  

最简单的思路自然是新建一个新数组，每次从原数组中剩下的元素随机挑选一个放入新数组，知道原数组为空。  

考虑一下这种方式的随机性。一个元素shuffle以后位于第一个位置的概率为$\frac{1}{n}$，即第一次被抽中。  
出现在第二个位置的概率为：    
$$
\begin{aligned}
p &= p(第一次没抽中) \times p(第二次抽中) \\\\
& = (1-\frac{1}{n}) \times \frac{1}{n-1} \\\\
& = \frac{1}{n}
\end{aligned}
$$  

以此类推，可知该元素被等概率得分配到任意的位置，符合随机性要求。(此部分推导来自novoland的github上的文章)    

按该思路实现洗牌算法时有两个问题。首先，新牌堆显然需要  的空间；其次，元素从旧数组移入新牌堆后势必会留下空洞，在后续抽牌时要跳过这些空洞位置。  

但实际上，新牌堆和旧牌堆元素之和始终为 n，因此整个洗牌过程可以就地完成。我们可以从前向后遍历，对元素 i，前 i-1 个位置构成新牌堆，i 及其后续元素属于旧牌堆。从旧牌堆中随机抽一个元素，与 i 处元素交换，即完成了一次抽牌动作。  

该算法有个名字，叫 Fisher–Yates shuffle。  

说完理论以后，我们来看看代码。talk is cheap, show me the code  

```
package edu.bit.pro;

import java.util.Random;

public class Shuffle_Rand {

    public static void shuffle(int[] a) {
        Random rand = new Random();
        for(int i=a.length-1; i>0; i--) {
            int j = rand.nextInt(i+1); //注意是i+1

            int tmp = a[i];
            a[i] = a[j];
            a[j] = tmp;

        }
    }

    public static void printArray(int[] a) {
        for(int i=0; i<a.length; i++) {
            System.out.print(a[i] + " ");
        }
    }

    public static void main(String[] args) {
        int[] a = {0,1,2,3,4,5,6,7,8,9};
        System.out.println("before shuffle: ");
        printArray(a);


        System.out.println("\nafter shuffle: ");
        shuffle(a);
        printArray(a);
    }
}

```  

将代码run起来以后，得到输出：  

```
before shuffle: 
0 1 2 3 4 5 6 7 8 9 
after shuffle: 
2 5 7 1 0 8 6 4 9 3 
```  

代码不难理解，稍微需要注意的就是` int j = rand.nextInt(i+1)`这一行。注意需要时(i+1)，而不是i。因为第j个元素在交换的时候，包括了他自己，所以此时j的范围应该是从0到i并且包括i。我们看看Random里nextInt的描述：  

```
Returns a pseudorandom, uniformly distributed value between 0 (inclusive) and the specified value(exclusive),
 drawn from this random number generator's sequence.
```  

很明显，用nextInt方法时，传入参数n以后，产生的随机数的范围是0-(n-1)，因为the specified value (exclusive)。所以我们上面那行代码应该是(i+1)，而不是i。  

另外偷偷告诉大家，java里的Collections模块里就实现了shuffle功能，采用的算法，就是我们刚才提到的 Fisher–Yates shuffle。  