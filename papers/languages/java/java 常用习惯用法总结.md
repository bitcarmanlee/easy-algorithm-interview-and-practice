注：本文是根据网络上的文章受启发，自己再写代码总结而成。因为无法找到原文的原始出处，所以没法给出原文链接。文章也会引用部分网络素材内容，如果原作者看到请与我联系。  

## 0.前言
本博主的java水平与专业java开发同学相比水平不可同日而语，所以平时有空的话会多写写java代码。正好在网上看到一篇关于java习惯用法的总结，觉得还不错，于是按照文章里的大致架构，自己重新实现了一把里面的相关代码，相当于自己做个小小的总结。  

## 1.基本方法实现
equals()  
hashcode()  
compareTo()  
clone()  

### 1.1 equals()实例与hashCode()实例

```
import java.util.Arrays;

public class Person {
	String name;
	int birthday;
	byte[] raw;
	
	public boolean equals(Object obj) {
		// 原文中的代码有误，需要将!符号后面的表达式扩起来
		if (!(obj instanceof Person)) { 
			return false;
		}
		Person other = (Person) obj;
		return name.equals(other.name)
			&& birthday == other.birthday
			&& Arrays.equals(raw, other.raw);
	}
	
	public int hashCode() {
		return name.hashCode() + birthday + Arrays.hashCode(raw);
	}
	
	public static void main(String[] args) {
		Person leilei = new Person();
		leilei.name = "leilei";
		leilei.birthday = 19991010;
		
		Person lulu = new Person();
		lulu.name = "leilei";
		lulu.birthday = 19991010;
		
		System.out.println(leilei.equals(lulu));
	}

}
```  

equals()方法需要注意的几个点  
1.参数必须是Object类型，不能是外围类。jdk源码中的equals()方法，传入的参数就是Object类型。  
2.foo.equals(null) 必须返回false，不能抛NullPointerException。(注意，null instanceof 任意类 总是返回false，因此上面的代码可以运行)  
3.基本类型比较使用 ==，基本类型数组域的比较使用Arrays.equals()。  
4.覆盖equals()时，记得要相应地覆盖 hashCode()，与 equals() 保持一致  

hashCode()方法注意的几个点  
1.当x和y两个对象具有x.equals(y) == true ，你必须要确保x.hashCode() == y.hashCode()。  
2.根据逆反命题，如果x.hashCode() != y.hashCode()，那么x.equals(y) == false 必定成立。  
3.你不需要保证，当x.equals(y) == false时，x.hashCode() != y.hashCode()。但是，如果你可以尽可能地使它成立的话，这会提高哈希表的性能。  
4.hashCode()最简单的合法实现就是简单地return 0；虽然这个实现是正确的，但是这会导致HashMap这些数据结构运行得很慢。  

### 1.2 compareTo()方法实现

```
package leilei.bit.edu.common;

import java.util.TreeSet;

public class PersonA implements Comparable<PersonA>{
	String firstName;
	String lastName;
	int birthday;
	
	public int compareTo(PersonA other) {
		if(firstName.compareTo(other.firstName) != 0) {
			return firstName.compareTo(other.firstName);
		} else if(lastName.compareTo(other.lastName) != 0) {
			return lastName.compareTo(other.lastName);
		} else if(birthday < other.birthday) {
			return -1;
		} else if(birthday > other.birthday) {
			return 1;
		} else {
			return 0;
		}
	}
	
	@Override
	public String toString() {
		return "firstName: " + firstName + ",lastName: " + lastName;
	}
	
	public static void main(String[] args) {
		PersonA p1 = new PersonA();
		p1.firstName = "li";
		p1.lastName = "lei";
		
		PersonA p2 = new PersonA();
		p2.firstName = "han";
		p2.lastName = "meimei";
		
		PersonA p3 = new PersonA();
		p3.firstName = "xiao";
		p3.lastName = "ming";
		
		TreeSet tree = new TreeSet();
		tree.add(p1);
		tree.add(p2);
		tree.add(p3);
		
		for(Object obj:tree) {
			System.out.println(obj);
		}
	}
}

```  

输出：  

```
firstName: han,lastName: meimei
firstName: li,lastName: lei
firstName: xiao,lastName: ming
```  

TreeSet在java内部是一种排序的数据结构。根据程序的输出可以看出，person对象在tree中是根据firstName排序的。  

1.总是实现泛型版本 Comparable 而不是实现原始类型 Comparable 。因为这样可以节省代码量和减少不必要的麻烦。  
2.只关心返回结果的正负号（负/零/正），它们的大小不重要。  
3.Comparator.compare()的实现与这个类似。  

### 1.3 clone()方法
实际中我很少使用clone方法，怕自己的理解有偏差，直接将原文的clone部分摘过来  

```
class Values implements Cloneable {
  String abc;
  double foo;
  int[] bars;
  Date hired;
 
  public Values clone() {
    try {
      Values result = (Values)super.clone();
      result.bars = result.bars.clone();
      result.hired = result.hired.clone();
      return result;
    } catch (CloneNotSupportedException e) {  // Impossible
      throw new AssertionError(e);
    }
  }
}

```  
1.使用 super.clone() 让Object类负责创建新的对象。  
2.基本类型域都已经被正确地复制了。同样，我们不需要去克隆String和BigInteger等不可变类型。  
3.手动对所有的非基本类型域（对象和数组）进行深度复制（deep copy）。   
4.实现了Cloneable的类，clone()方法永远不要抛CloneNotSupportedException。因此，需要捕获这个异常并忽略它，或者使用不受检异常（unchecked exception）包装它。  
5.不使用Object.clone()方法而是手动地实现clone()方法是可以的也是合法的。  

## 2.应用类

### 2.1 StringBuilder 与 StringBuffer
这两个类在实际开发中用得很多，举一个很简单的小例子。  

```
	@Test
	public void Str_Build() {
		StringBuilder sb = new StringBuilder();
		sb.append("I ");
		sb.append("love");
		sb.append(" coding");
		System.out.println(sb.toString());
	}
```  

让代码run起来  

```
I love coding
```  

注意点：  
1.不要像这样使用重复的字符串连接：s += item ，因为它的时间效率是O(n^2)。  
2.使用StringBuilder或者StringBuffer时，可以使用append()方法添加文本和使用toString()方法去获取连接起来的整个文本。示例代码中就是这么做的。  
3.优先使用StringBuilder，因为它更快。StringBuffer的所有方法都是同步的，而你通常不需要同步的方法。  
4.StringBuilder的缺陷之一，就是开发过程中，经常用sb作为new出来的对象名称。。。  

### 2.2 生成一个随机整数

```
	@Test
	public void int_random() {
		Random rand = new Random();
		int a = rand.nextInt(10) + 1;
		System.out.println("random num is: " + a);
	}
```  

让代码run起来  

```
random num is: 10
```  

### 2.3 使用Iterator.remove()

```
	@Test
	public void collections_remove() {
		List<Integer> list = new ArrayList<Integer>();
		for(int i=1; i<=10; i++) {
			list.add(i);
		}
		
		Iterator<Integer> it = list.iterator();
		while(it.hasNext()) {
			int num = it.next();
			
			if(num%2 == 0) {
				System.out.println(num + "===" + num);
				it.remove();
			}
		}
		
		for(int each:list) {
			System.out.print(each + " ");
		}
	}
```  

让代码run起来  

```
2===2
4===4
6===6
8===8
10===10
1 3 5 7 9 
```  

remove()方法作用在next()方法最近返回的条目上。每个条目只能使用一次remove()方法。  

### 2.4 反转字符串
c++的程序猿里的一道经典面试题就是反转字符串。对于java或者python等更高级的语言来说，反转字符串都是一句话搞定的事情。  


```
	@Test
	public void reverse_str() {
		String raw_str = "some";
		String rev_str = new StringBuilder(raw_str).reverse().toString();
		System.out.println("rev_str is: " + rev_str);
	}
```  

让代码run起来  

```
rev_str is: emos
```  

### 2.5 Thread/Runnable

```
//实现Runnable的方式
void startAThread0() {
  new Thread(new MyRunnable()).start();
}
 
class MyRunnable implements Runnable {
  public void run() {
    ...
  }
}

//继承Thread的方式
void startAThread1() {
  new MyThread().start();
}
 
class MyThread extends Thread {
  public void run() {
    ...
  }
}

匿名继承Thread的方式
void startAThread2() {
  new Thread() {
    public void run() {
      ...
    }
  }.start();
}
```  

不要直接调用run()方法。总是调用Thread.start()方法，这个方法会创建一条新的线程并使新建的线程调用run()。  

### 2.6 try-finally

```
IO流的例子
void writeStuff() throws IOException {
  OutputStream out = new FileOutputStream(...);
  try {
    out.write(...);
  } finally {
    out.close();
  }
}

锁的例子
void doWithLock(Lock lock) {
  lock.acquire();
  try {
    ...
  } finally {
    lock.release();
  }
}
```  

1.如果try之前的语句运行失败并且抛出异常，那么finally语句块就不会执行。但无论怎样，在这个例子里不用担心资源的释放。  
2.如果try语句块里面的语句抛出异常，那么程序的运行就会跳到finally语句块里执行尽可能多的语句，然后跳出这个方法（除非这个方法还有另一个外围的finally语句块）。  

## 3.输入输出
### 3.1 从输入流中读取字节数据

```
	@Test
	public void test1() throws Exception {
		InputStream in = new FileInputStream(new File("xxx"));
		try {
			while(true) {
				int n = in.read();
				if(n == -1) {
					break;
				} else {
					System.out.println(n);
				}
			}
			
		} finally {
			in.close();
		}
	}
```  

输出：  

```
112
97
99
107
97
103
101
...
```  

由此可见，read()方法要么返回下一次从流里读取的字节数（0到255，包括0和255），要么在达到流的末端。  

### 3.2 从输入流中读取块数据

```
	@Test
	public void test2() throws Exception {
		InputStream in = new FileInputStream(new File("xxx"));
		try {
			byte[] buf = new byte[100];
			while(true) {
				int n = in.read(buf);
				if(n == -1) {
					break;
				} else {
					System.out.println(n);
				}
			}
			
		} finally {
			in.close();
		}
	}
```  

输出：  

```
100
100
100
100
100
100
81
```  

要记住的是，read()方法不一定会填满整个buf，所以你必须在处理逻辑中考虑返回的长度。  

### 3.3 读取文本文件

```
	@Test
	public void test3() throws Exception {
		String filename = "xxx";
		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(new File(filename)),"utf-8"));
		try {
			while (true) {
				String line = br.readLine();
				if (line == null) {
					break;
				} else {
					System.out.println(line);
				}
			}
		} finally {
			br.close();
		}
	}
```  

1.BufferedReader对象的创建显得很冗长。这是因为Java把字节和字符当成两个不同的概念来看待  
2.你可以使用任何类型的InputStream来代替FileInputStream，比如socket  
3.当达到流的末端时，BufferedReader.readLine()会返回null。  
4.要一次读取一个字符，使用Reader.read()方法。  
5.你可以使用其他的字符编码而不使用UTF-8，但最好不要这样做。  

### 3.4.向文本写文件

```
	@Test
	public void test4() throws Exception {
		String filename = "xxx";
		PrintWriter out = new PrintWriter(
				new OutputStreamWriter(new FileOutputStream(new File(filename)),"utf-8"));
		try {
			out.println("hello");
			out.println(42);
			out.println("world");
		} finally {
			out.close();
		}
	}
```  

1.Printwriter对象的创建显得很冗长。这是因为Java把字节和字符当成两个不同的概念来看待  
2.就像System.out，你可以使用print()和println()打印多种类型的值。  
3.你可以使用其他的字符编码而不使用UTF-8，但最好不要这样做。  

## 4 预防性(Defensive Checking)检测
### 4.1  预防性检测数值  

```
package leilei.bit.edu.common;

public class Checking {
	
	public static int factorial(int n) {
		if (n < 0) {
			throw new IllegalArgumentException("Undefined");
		} else if(n > 13) {
			throw new ArithmeticException("Reuslt overflow");
		} else if(n == 0) {
			return 1;
		} else {
			return factorial(n-1) * n;
		}
	}
	
	public static void main(String[] args) {
		int n = 5;
		int ret = factorial(n);
		System.out.println("ret is: " + ret);
	}
}

```  

1.不要认为输入的数值都是正数、足够小的数等等。要显式地检测这些条件。  
2.一个设计良好的函数应该对所有可能性的输入值都能够正确地执行。要确保所有的情况都考虑到了并且不会产生错误的输出（比如溢出）。  

### 4.2 预防性检测对象

```
public int findIndex(List<String> list, String target) {
  if (list == null || target == null)
    throw new NullPointerException();
  ...
}
```  
1.不要认为对象参数不会为空（null）。要显式地检测这个条件。  

### 4.3预防性检测数组索引

```
	public static void outOfBound(int[] b, int index) {
		if(b==null) {
			throw new NullPointerException();
		}
		if(index < 0 || index >= b.length) {
			throw new IndexOutOfBoundsException();
		}
		...
	}
```  
不要认为所以给的数组索引不会越界。要显式地检测它。  

### 4.4 预防性检测数组区间

```
	public static void errorRange(int[] b, int off, int len) {
		if(b == null) {
			throw new NullPointerException();
		}
		if (off < 0 || off > b.length || len < 0 || b.length - off < len) {
			throw new IndexOutOfBoundsException();
		}
		...
	}
```  
不要认为所给的数组区间（比如，从off开始，读取len个元素）是不会越界。要显式地检测它。  

## 5.数组
### 5.1 填充数组元素
### 5.2 复制一个范围内的数组元素
### 5.3 调整数组大小

具体代码如下：  

```
package leilei.bit.edu.bigNum;

import java.util.Arrays;

public class Array_Test {
	
	public static void printArray(int[] a) {
		for(int i=0; i<a.length; i++) {
			System.out.print(a[i] + " ");
		}
	}
	
	public static void fill_test() {
		int[] a = new int[5];
		Arrays.fill(a,0,5,1);
		printArray(a);
	}
	
	public static void copy_test() {
		int[] a = {1,2,3,4,5};
		int[] b = new int[5];
		System.arraycopy(a, 0, b, 0, a.length);
		printArray(b);
	}
	
	public static void copyOf_test() {
		int[] a = {1,2,3,4,5};
		a = Arrays.copyOf(a,10);
		printArray(a);
	}
	
	public static void main(String[] args) {
		fill_test();
		System.out.println();
		copy_test();
		System.out.println();
		copyOf_test();
	}
}

```  

代码运行结果如下：  

```
1 1 1 1 1 
1 2 3 4 5 
1 2 3 4 5 0 0 0 0 0 
```  

## 6.包装
以下代码演示了将四个字节包装成一个int，以及将一个int分解成四个字节。  

```
package leilei.bit.edu.bigNum;

public class Pack {
	
	public static void pack() {
		byte[] a = {1,2,3,4};
		int result = (a[0] & 0xFF) << 24
					|(a[1] & 0xFF) << 16
					|(a[2] & 0xFF) << 8
					|(a[3] & 0xFF) << 0;
		System.out.println("result is: " + result);
 	}
	
	public static void unpack() {
		int x = 16909060;
		byte[] result = {
				(byte)(x >>> 24),
				(byte)(x >>> 16),
				(byte)(x >>> 8),
				(byte)(x >>> 0)
		};
		System.out.print("the unpack result is: ");
		for(int i=0; i<result.length; i++) {
			System.out.print(result[i] + " ");
		}
	}
	
	public static void main(String[] args) {
		pack();
		unpack();
	}

}

```  

让代码run起来：  

```
result is: 16909060
the unpack result is: 1 2 3 4 
```  