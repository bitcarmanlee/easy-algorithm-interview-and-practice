很多时候我们需要输出double数字的字符串形式。但是java默认的double输出方式为科学记数法，显然不符合我们的要求，以下两种方法都能达到我们的目的。  

## 1.使用DecimalFormat类

```

    public static void t1() {
        Double num1 = 100000000.0;
        System.out.println(num1);  // 1.0E8
        DecimalFormat decimalFormat = new DecimalFormat("#,##0.00");
        System.out.println(decimalFormat.format(num1)); // 100,000,000.00
    }
```  

## 2.使用BigDecimal的toString方法

```
    public static void t2() {
        Double num2 = 100000000.123456;
        BigDecimal bigDecimal = new BigDecimal(num2);
        System.out.println(num2);  // 11.00000000123456E8
        String res = bigDecimal.toString();
        System.out.println(res);  // 100000000.12345600128173828125
        BigDecimal bigDecimal2 = new BigDecimal("100000000.123456");
        System.out.println(bigDecimal2.toString());  // 100000000.123456
    }
```