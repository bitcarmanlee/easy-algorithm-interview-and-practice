## 1.java泛型中的关键字
java泛型中有如下关键字：  
1. ? 表示通配符类型  
2. &lt;? extends T> 既然是extends，就是表示泛型参数类型的上界，说明参数的类型应该是T或者T的子类。  
3. &lt;? super T> 既然是super，表示的则是类型的下界，说明参数的类型应该是T类型的父类，一直到object。  

## 2.示例代码

```
public class GenericClass {

    static class Animal {}

    static class FlyAnimal extends Animal {}

    static class Bird extends FlyAnimal {}

    public void testExtend() {
        List<? extends FlyAnimal> list = new ArrayList<Bird>();

		//无法安全添加任何具有实际意义的元素
        //list.add(new Bird());
        //list.add(new FlyAnimal());
        list.add(null);
        Animal animal = list.get(0);
        Bird bird = (Bird)list.get(0);
    }

    public void testSuper() {
        List<? super FlyAnimal> list = new ArrayList<FlyAnimal>();
        list.add(new FlyAnimal());
        list.add(new Bird());
        //list.add(new Animal());
        //List<? super FlyAnimal> list2 = new ArrayList<Bird>();
        //FlyAnimal flyAnimal = list.get(0); 不能确定返回类型
        
    }

```  

## 3.extends分析
`List<? extends FlyAnimal>` 表示 “具有任何从FlyAnimal继承类型的列表”，编译器无法确定List所持有的类型，所以无法安全的向其中添加对象。但是可以添加null，因为null可以表示任何类型。  

同时，由于list里面的类型是从FlyAnimal中继承过来的，所以可以安全取出FlyAnimal类型。  

所以最后总结下来是：list的add方法不能添加任何有意思的元素，但是可以接受现有子类型Bird的赋值。同时可以安全取出元素类型。  

## 4.super分析
List&lt;? super FlyAnimal> 表示“具有任何FlyAnimal父类的列表”，列表的类型至少是一个 FlyAnimal 类型，因此可以安全的向其中添加FlyAnimal及其子类型。由于List&lt;? super FlyAnimal>中的类型可能是任何FlyAnimal的父类型，无法赋值为FlyAnimal的子类型Bird的List&lt;Bird>.  
同时，因为List&lt;? super FlyAnimal>表示的类型是FlyAnimal的父类，所以编译器也无法确定返回的类型。  

## 5.泛型类型实际上都是相同的基本类型
在泛型接口泛型类泛型方法的定义过程中，经常会见到用T等形式的参数表示泛型的形参，用于接收来自外部使用时传入的类型实参。那么如果传入不同类型的实参，生成的相应对象实例的类型是否一样呢？  

```
class GenClazz<T> {
    private T data;
    public GenClazz() {}

    public GenClazz(T data) {
        this.data = data;
    }

    public T getData() {
        return data;
    }
}
```  

定义了如上的测试类，然后写个简单的测试方法  

```
    public void test1() {
        GenClazz<String> name = new GenClazz<String>("xiaoming");
        GenClazz<Integer> age = new GenClazz<Integer>(123);

        System.out.println("name class: " + name.getClass());
        System.out.println("age class: " + age.getClass());
        System.out.println(name.getClass() == age.getClass());
    }
```  

最后第三行会输出true!  
由此，我们发现，在使用泛型类时，虽然传入了不同的泛型实参，但并没有真正意义上生成不同的类型，传入不同泛型实参的泛型类在内存上只有一个，即还是原来的最基本的类型（本实例中为GenClazz），当然，在逻辑上我们可以理解成多个不同的泛型类型。  

究其原因，在于Java中的泛型这一概念提出的目的，导致其只是作用于代码编译阶段，在编译过程中，对于正确检验泛型结果后，会将泛型的相关信息擦除，也就是说，成功编译过后的class文件中是不包含任何泛型信息的。泛型信息不会进入到运行时阶段。  

对此总结成一句话：泛型类型在逻辑上看以看成是多个不同的类型，实际上都是相同的基本类型。  

## 6.最终小结
extends 可用于的返回类型限定，不能用于参数类型限定。  
super 可用于参数类型限定，不能用于返回类型限定。  
带有super超类型限定的通配符可以向泛型对易用写入，带有extends子类型限定的通配符可以向泛型对象读取。——《Core Java》  