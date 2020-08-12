栈是一种常见的数据结构。如果用一句话来概括栈的特点，估计大部分同学都能脱口而出：后进先出，即先进来的元素保存在栈的最底部，新来的元素则在栈顶堆积，直到栈满为止；而取元素的时候，只能从栈顶取，直到栈空为止。整个过程，与摞书的过程很类似：放书的时候都是摞在最上面，取书的时候也是从最上面开始取。要想取出下面的书，就必须先将上面的书先取走。  

原理就讲这么多，本身也比较简单。接下来，照例是咱们的口号：  
talk is cheap, show me the code  

```
package leilei.bit.edu.stacktest;

/**
 * @author lei.wang
 *
 */

public class Stack {
	
	//存数据的数组
	int[] data;
	
	//栈的最大长度
	private int size;
	//栈顶的位置
	private int top;
	
	public Stack(int size) {
		this.size = size;
		data = new int[size];
		top = -1;
	}
	
	public int getSize() {
		return size;
	}
	
	public int getTop() {
		return top;
	}
	
	/**
	 * 判断是否为空栈
	 * @return
	 */
	public boolean isEmpty()	 {
		return top == -1;
	}
	
	/**
	 * 判断是否为满栈
	 * @return
	 */
	public boolean isFull() {
		return (top+1) == size;
	}
	
	/**
	 * 压栈操作
	 * @param data
	 * @return
	 */
	public boolean push(int data) {
		if(isFull()) {
			System.out.println("the stack is full!");
			return false;
		} else {
			top++;
			this.data[top] = data;
			return true;
		}
	}
	
	
	/**
	 *  弹栈操作
	 * @return
	 * @throws Exception
	 */
	public int pop() throws Exception {
		if(isEmpty()) {
			throw new Exception("the stack is empty!");
		} else {
			return this.data[top--];
		}
	}
	
	/**
	 * 获取栈顶的元素,但不弹栈
	 * @return
	 */
	public int peek() {
		return this.data[getTop()];
	}
	
	public static void main(String[] args) {
		Stack stack = new Stack(20);
		stack.push(0);
		stack.push(1);
		stack.push(2);
		stack.push(3);
		System.out.println("Now the top_num is:" + stack.peek());
		
		while(! stack.isEmpty()) {
			try {
				System.out.println(stack.pop());
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
}

```  

代码运行结果  

```
Now the top_num is:3
3
2
1
0
```  

代码本身比较简单，就不在过多解释，如果还有不懂的地方请看注释；注释还不懂的话，请留言。  