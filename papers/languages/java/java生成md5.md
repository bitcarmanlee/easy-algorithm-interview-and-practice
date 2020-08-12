系统中的密码等用户信息，肯定不能用明文来存储。如果有发生信息泄露等问题，用明文存储的密码就太危险了。所以一般我们都用md5等方式来对密码进行加密处理。  
以下代码就可以用来生成字符串的md5加密。  

```
public class Md5UtilDemo {

    public static String md5(String plainText) {
        String encryptText = null;
        try {
            //拿到一个md5转换器
            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(plainText.getBytes("UTF8"));
            byte s[] = md.digest();
            String result = "";
            for (int i = 0; i < s.length; i++) {
                result += Integer.toHexString((0x000000FF & s[i]) | 0xFFFFFF00).substring(6);
            }
            return result;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return encryptText;
    }

    public static void main(String[] args) {
        String inputStr = "abc";
        String result = md5(inputStr);
        System.out.println(result);
        System.out.println(result.length());
    }

}
```  

代码run起来的结果：  

```
900150983cd24fb0d6963f7d28e17f72
32
```  

其中，`Integer.toHexString((0x000000FF & s[i]) | 0xFFFFFF00).substring(6)`的作用 是显示一个byte型的单字节十六进制(两位十六进制表示)的编码。  

byteVar & 0x000000FF的作用是，如果byteVar 是负数，则会清除前面24个零，正的byte整型不受影响。(...) | 0xFFFFFF00的作用是，如果byteVar 是正数，则置前24位为一，这样toHexString输出一个小于等于15的byte整型的十六进制时，倒数第二位为零且不会被丢弃，这样可以通过substring方法进行截取最后两位即可。  