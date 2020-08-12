今天在排除代码中的Bug的时候，在浮点数运算过程中遇到了NAN与INFINITY的问题。特此记录一下。  
首先明确一点的是，java浮点数中有两个特殊情况：NAN,INFINITY  

## 1.NAN
NAN是一个特殊的值。在JDK中，NAN是这么定义的：  

```
    /**
     * A constant holding a Not-a-Number (NaN) value of type
     * {@code double}. It is equivalent to the value returned by
     * {@code Double.longBitsToDouble(0x7ff8000000000000L)}.
     */
    public static final double NaN = 0.0d / 0.0;
```  

特意将注释也copy下来。相信加上注释，同学们就都明白是什么意思了。Not-a-Number准确道出了NAN的含义。  

```
    @Test
    public void testNan() {
        double NaN1 = Double.NaN;
        double NaN2 = 0.0 / 0.0;
        System.out.println(Double.isNaN(NaN1)); //true
        System.out.println(Double.isNaN(NaN2)); //true
        System.out.println(NaN1 == NaN1); //false

    }
```  

NAN表示非数字，它与任何值都不相等，甚至不等于它自己，所以要判断一个数是否为NAN要用isNAN方法。  

## 2.INFINITY
INFINITY主要是为了解决除数为0的情况。稍微有点数学基础的同学，都应该明白无限这个概念。  

```
    /**
     * A constant holding the positive infinity of type
     * {@code double}. It is equal to the value returned by
     * {@code Double.longBitsToDouble(0x7ff0000000000000L)}.
     */
    public static final double POSITIVE_INFINITY = 1.0 / 0.0;

    /**
     * A constant holding the negative infinity of type
     * {@code double}. It is equal to the value returned by
     * {@code Double.longBitsToDouble(0xfff0000000000000L)}.
     */
    public static final double NEGATIVE_INFINITY = -1.0 / 0.0;

```  

```
    /**
     * A constant holding the positive infinity of type
     * {@code float}. It is equal to the value returned by
     * {@code Float.intBitsToFloat(0x7f800000)}.
     */
    public static final float POSITIVE_INFINITY = 1.0f / 0.0f;

    /**
     * A constant holding the negative infinity of type
     * {@code float}. It is equal to the value returned by
     * {@code Float.intBitsToFloat(0xff800000)}.
     */
    public static final float NEGATIVE_INFINITY = -1.0f / 0.0f;
```  

这是JDK中的相关定义。很容易看出来，double与float中都有INFINITY的相关定义。  

```
   @Test
    public void testInfinity() {
        double Inf1 = Double.POSITIVE_INFINITY;
        double Inf2 = Double.NEGATIVE_INFINITY;

        float Inf3 = Float.POSITIVE_INFINITY;
        float Inf4 = Float.NEGATIVE_INFINITY;

        System.out.println(Double.isInfinite(Inf1)); //true
        System.out.println(Float.isInfinite(Inf3)); //true

        System.out.println(Inf1 == Inf3); //true
        System.out.println(Inf2 == Inf4); //true

        System.out.println(Inf1 * 0); //NaN

        System.out.println(Inf1 + 1); //Infinity
        System.out.println(Inf1 * 0.4); //Infinity
        System.out.println(Inf1 / 0); //Infinity
    }
```  

从测试代码中，可以得出如下结论：  
1.double或者float判断是不是INFINITY都使用isInfinite方法。  
2.double中的INFINITY与float中的INFINITY是相等的。  
3.INFINITY乘以0得到NAN。  
4.INFINITY做除了乘以0意外的任何四则运算，得到的结果仍然是INFINITY。  

第三点跟第四点，结果INFINITY的数学性质，很容易理解。  