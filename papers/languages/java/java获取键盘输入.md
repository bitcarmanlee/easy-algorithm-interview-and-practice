## 1.使用System.in.read
此种方法能从控制台接收一个字符，并且将该字符打印出来  

```
    public static void t1() throws IOException {
        System.out.println("Enter a Char: ");
        char c = (char) System.in.read();
        System.out.println("your char is: " + c);
    }
```  

此方法的缺点显而易见：  
1.每次只能获取一个字符。  
2.read方法获取的是int类型，需要根据需求做各种类型转换。  

## 2.使用BufferedReader

```
    public static void t2() {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String str;
        try {
            System.out.println("please enter your name: ");
            String name = br.readLine();
            System.out.println("Your name is: " + name);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
```  

这种方法可以从控制台接受一个字符串，。并且打印出来。但是这种方式对于多次输入也不是很方便。  

## 3.使用Scanner

```
    public static void t3() {
        Scanner sc = new Scanner(System.in);
        System.out.println("please input your name: ");
        String name = sc.nextLine();
        System.out.println("please input your age: ");
        int age = sc.nextInt();
        System.out.println("please input your salary: ");
        float salary = sc.nextFloat();
        System.out.println("your msg is: ");
        System.out.println("name: " + name + ", age: " + age + ", salary: " + salary);
    }
```  

从 JDK 5.0 开始，基本类库中增加了java.util.Scanner类，根据它的 API 文档说明，这个类是采用正则表达式进行基本类型和字符串分析的文本扫描器。使用它的Scanner(InputStream source)构造方法，可以传入系统的输入流System.in而从控制台中读取数据。  


从这三种方式的对比很容易看出，用Scanner的方式获取数据是最容易与方便的！  
