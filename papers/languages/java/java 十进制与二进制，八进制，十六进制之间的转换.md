实际开发过程中，经常会有十进制的数据跟其他进制数据互相转化的情况。比如十进制与二进制，八进制，十六进制之间的相互转化。为了方便起见，特意将java中不同进制间相互转化的代码整理以备后续使用。   

```
package leilei.bit.edu.sort;

public class NumRadixConvert {

	public static void decimal_to_other() {
		int a = 10;
		
		//注意返回的类型都是String
		String hex = Integer.toHexString(a);
		String oct = Integer.toOctalString(a);
		String bin = Integer.toBinaryString(a);
		
		System.out.println("hex is: " + hex);
		System.out.println("oct is: " + oct);
		System.out.println("bin is: " + bin);
	}
	
	public static void other_to_decimal() {
		int hex_to_dec = Integer.valueOf("F",16);
		int oct_to_dec = Integer.valueOf("12",8);
		int bin_to_dec = Integer.valueOf("111111",2);
		
		System.out.println("hex_to_dec is: " + hex_to_dec);
		System.out.println("oct_to_dec is: " + oct_to_dec);
		System.out.println("bin_to_dec is: " + bin_to_dec);
	}
	
	public static void parse_int() {
		int parse_hex = Integer.parseInt("F",16);
		int parse_oct = Integer.parseInt("12",8);
		int parse_bin = Integer.parseInt("111111",2);
		
		System.out.println("parse_hex is: " + parse_hex);
		System.out.println("parse_oct is: " + parse_oct);
		System.out.println("parse_bin is: " + parse_bin);
		
	}
	
	public static void main(String[] args) {
		decimal_to_other();
		System.out.println();
		other_to_decimal();
		System.out.println();
		parse_int();
	}
}

```  

代码运行结果  

```
hex is: a
oct is: 12
bin is: 1010

hex_to_dec is: 15
oct_to_dec is: 10
bin_to_dec is: 63

parse_hex is: 15
parse_oct is: 10
parse_bin is: 63

```  

代码本身比较简单，也没太多技术含量，就当个笔记吧。  