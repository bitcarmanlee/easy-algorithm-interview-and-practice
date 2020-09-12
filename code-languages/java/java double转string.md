java中，double转string可以用Double.toString(d)的方式。但是，这种方式有隐藏的坑，请大家看仔细了：  

```
package hello;

public class DoubleToString {
    
    public static void test1(double dou) {
        String dou_str = Double.toString(dou);
        if (dou_str.equals("20160101")) {
            System.out.println("YES!");
        } else {
            System.out.println("NO!");
        }
    }
    
    public static void main(String[] args) {
        double dou = 20160101;
        test1(dou);
    }
}
```  

当运行上述代码以后，控制台华丽丽地输出：  

```
NO！
```  

我们在第六行后面打印出dou_str：  

```
2.0160101E7
```  

原来jvm这货将double用科学计数法表示了double，怪不得转成string以后变了样。。。  

将上面代码修改如下：  

```
package hello;

import java.text.NumberFormat;

public class DoubleToString {
	
    public static void test2(double dou) {
        Double dou_obj = new Double(dou);
        NumberFormat nf = NumberFormat.getInstance();
        nf.setGroupingUsed(false);
        String dou_str = nf.format(dou_obj);
        System.out.println("dou_str is:" + dou_str);
        if (dou_str.equals("20160101")) {
        	System.out.println("YES!");
        } else {
        	System.out.println("NO!");
        }
    }
	
	public static void main(String[] args) {
		double dou = 20160101;
		test2(dou);
	}
}
```  

再运行，再输出，这下就OK了：  

```
dou_str is:20160101
YES!
```  