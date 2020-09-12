## 1.实现数值类型加法
实际开发中，经常有数值类型求和的需求，例如实现int类型的加法：  

```
    public int add(int num1, int num2) {
        return num1 + num2;
    }
```  

有时候还需要实现long类型的求和：  

```
    public long add(long num1, long num2) {
        return num1 + num2;
    }
```  

如果还需要double类型的求和，需要重新在重载一个输入是double类型的add方法。  
其实逻辑都是一样的，只是输入参数类型不一样而已，正好在java中数值类型有个公共的父类：Number。所以我们可以这么做：  

```
    public <T extends Number> double add(T t1, T t2) {
        double allsum;
        allsum = t1.doubleValue() + t2.doubleValue();
        return allsum;
    }

    @Test
    public void testAdd() {
        int int1 = 1;
        int int2 = 2;
        System.out.println("Integer sum is: " + add(int1, int2));

        long long1 = 100;
        long long2 = 200;
        System.out.println("Long sum is: " + add(long1, long2));

        float f1 = 1.0f;
        float f2 = 2.0f;
        System.out.println("Float sum is: " + add(f1, f2));

        double d1 = 1.0;
        double d2 = 2.0;
        System.out.println("Double sum is: " + add(d1, d2));
    }
```  

将上述的test方法run起来以后，输出如下：  

```
Integer sum is: 3
Long sum is: 300
Float sum is: 3.0
Double sum is: 3.0
```  

## 2.实现数值类型集合的加法
上面是单个数值类型，推广一下，对于数值类型的集合来说，也经常会有类似的需求，这个时候我们可以也做类似的泛型方法：  

```
public class GenericAdd {
    //extend限制返回时候的类型
    public static void sumlist(List<? extends Number> list) {
        double sum = 0.0;

        for(Number each : list) {
            sum += each.doubleValue();
        }

        double sum2 = list.stream().mapToDouble(x -> x.doubleValue()).sum();
        System.out.println(sum);
        System.out.println(sum2);
    }
    
    //super限制添加时候的类型
    public static void lowerBound(List<? super Number> list) {
        list.add(new Integer(1));
        list.add(new Float(2));
        Integer value1 = (Integer) list.get(0);
        Float value2 = (Float) list.get(1);
        System.out.println(value1 + "\t" + value2);
    }
    
    public static void main(String[] args) {
        List<Number> list = new ArrayList<>();
        lowerBound(list);
        System.out.println("---------");

        List<Integer> intList = new ArrayList(){{add(1); add(2); add(3);}};
        sumlist(intList);
        System.out.println("---------");

        List<Double> doubleList = new ArrayList(){{add(10.0); add(20.0); add(30.0);}};
        sumlist(doubleList);
    }

}
```  

上面代码的输出结果如下：  

```
1	2.0
---------
6.0
6.0
---------
60.0
60.0
```  

这样就达到了数值类型集合求和的需求！  