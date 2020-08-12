## 1.为什么需要Builder模式  
Java的每个类中至少有一个构造函数。如果我们没有明确声明构造函数，编译器会默认帮我们生成一个无参的构造函数。  
Java的构造函数或者说任何方法中，也无法指定默认参数。如果要达到设置默认参数的目的，只能通过方法重载来实现。  
在实际工作中，有的对象属性会比较多。那么当操作这些对象属性的时候，可能会有许多组合。比如构造这个对象的时候，有的场景可能只需要传少量参数，有的场景可能需要传大量的参数或者全部参数。如果按照传统的做法，不同的传参对应的都是一个不同的构造器，代码会显得非常冗长与复杂。  

给大家看一个真实的场景，当时为了排查这个问题费了我相当长的时间。  

```
    public static class Factory implements TProtocolFactory {
        protected boolean strictRead_;
        protected boolean strictWrite_;
        protected int readLength_;

        public Factory() {
            this(false, true);
        }

        public Factory(boolean strictRead, boolean strictWrite) {
            this(strictRead, strictWrite, 0);
        }

        public Factory(boolean strictRead, boolean strictWrite, int readLength) {
            this.strictRead_ = false;
            this.strictWrite_ = true;
            this.strictRead_ = strictRead;
            this.strictWrite_ = strictWrite;
            this.readLength_ = readLength;
        }
       ....
｝
```  
这是我们项目中的一个thrift对象反编译的代码，Factory工厂类里有三个构造方法，其中一个为两个参数，一个是给这两个参数指定了默认值，另外一个构造方法里有三个参数。  

当时我在调用这个类的时候，原来的版本中还有一个四个参数的构造方法，新版本里面那个构造方法被干掉了，然后就悲剧了。。。  

当参数组合情况很多的时候，其实更好的方式，就是使用我们今天的主角：Builder模式。  

## 2.机器人例子  
为了方便说明Builder模式的过程，我们假定现在想造一台机器人Robot，Robot有型号，生产国家，价格，功能，续航等属性。  

```
public class Robot {

    private String model;
    private String country;
    private int price;
    private String ability;
    private int endurance;


    public Robot(String model,String country) {
        this.model = model;
        this.country = country;
    }

    public Robot(String model, String country, int price, String ability, int endurance) {
        this.model = model;
        this.country = country;
        this.price = price;
        this.ability = ability;
        this.endurance = endurance;
    }
}
```  
为了节省篇幅，上面有两个构造方法，有一个构造方法有2个参数，有一个构造方法有5个参数。  
如果这个时候生产计划右边，构造方法中需要传入三个参数，那没办法，只能再添加一个构造函数。。。代码丑到不行，而且长到爆。。。如果Robot类在项目里的很多地方被使用，修改这个类的风险系数是相当高的。。。  


## 3.只是用一个构造函数
针对上面的情况，我们改变一下代码的结构与组织方式。  

```
public class Robot {

    private String model;
    private String country;
    private int price;
    private String ability;
    private int endurance;

    Robot(RobotBuilder builder) {
        this.model = builder.model;
        this.country = builder.country;
        this.price = builder.price;
        this.ability = builder.ability;
        this.endurance = builder.endurance;
    }

    @Override
    public String toString() {
        return "robot model is: " + model + ", country is: " + country + ", price is: " +
                price + ", ability is: " + ability + ", endurance is: " + endurance;
    }

    public static class RobotBuilder {

        private String model;
        private String country;
        private int price;
        private String ability;
        private int endurance;

        // 必选参数
        public RobotBuilder(String model, String country) {
            this.model = model;
            this.country = country;
        }

        public RobotBuilder withOptionPrice(int price) {
            this.price = price;
            return this;
        }

        public RobotBuilder withOptionAbility(String ability) {
            this.ability = ability;
            return this;
        }

        public RobotBuilder withOptionEndurance(int endurance) {
            this.endurance = endurance;
            return this;
        }

        private void ValidateRobotData() {
            if (String.valueOf(this.price) != null) {
                assert (price > 0);
            }
        }

        public Robot buildRobot() {
            ValidateRobotData();
            return new Robot(this);
        }
    }

    public static void main(String[] args) {
        Robot robot = new RobotBuilder("AA1", "USA")
                .withOptionAbility("player")
                .withOptionPrice(100)
                .withOptionEndurance(5)
                .buildRobot();
        System.out.println(robot);
    }
}
```  
通过这种方式，可以是的对象创建过程中只需要一个构造函数。而且在调用的时候也比较清楚，对于参数的性质也一目了然。这种方式处理单纯多属性的场景能起到一定的效果，但是在实际场景中，Robot类中可能还包含比较复杂的对象，并且对象之间还有一定构造顺序。这个时候来看看我们的Builder建造者模式。  

## 4.Builder模式
首先我们还是定义Robot  

```
public class Robot {

    private String model;
    private String country;
    private int price;
    private String ability;
    private int endurance;
    
    ...(省略get/set方法)
    
    @Override
    public String toString() {
        return "robot model is: " + model + ", country is: " + country + ", price is: " +
                price + ", ability is: " + ability + ", endurance is: " + endurance;
    }
}
```  

接下来我们使用一个Builder的抽象类(也可以是接口)定义机器人的构建过程。  
 

```
public abstract class Builder {
    public abstract void buildModel();
    public abstract void buildCountry();
    public abstract void buildPrice();
    public abstract void buildAbility();
    public abstract void buildEndurance();

    public abstract Robot getRobot();
}
```  

然后是Builder的具体实现类  

```
public class ImpBuilder extends Builder {

    Robot robot = new Robot();

    @Override
    public void buildModel() {
        robot.setModel("AA1");
    }

    @Override
    public void buildCountry() {
        robot.setCountry("US");
    }

    @Override
    public void buildPrice() {
        robot.setPrice(100);
    }

    @Override
    public void buildAbility() {
        robot.setAbility("player");
    }

    @Override
    public void buildEndurance() {
        robot.setEndurance(5);
    }

    @Override
    public Robot getRobot() {
        return robot;
    }
}
```  
注意这里面有getRobot方法，会返回我们希望得到的Robot对象。  
机器人组装类如下  

```
public class RobotInstall {

    public void Construct(Builder builder) {
        builder.buildModel();
        builder.buildCountry();
        builder.buildPrice();
        builder.buildAbility();
        builder.buildEndurance();
    }
}
```  

最后是我们的客户端调用  

```
public class Client {

    public static void main(String[] args) {
        RobotInstall install = new RobotInstall();
        Builder builder = new ImpBuilder();

        install.Construct(builder);
        Robot robot = builder.getRobot();
        System.out.println(robot);
    }
}
```  

Builder模式在使用的时候使用了链式调用的方式，可读性很好。而且Builder的内部构造方法中，只接收了必传的参数。对于我们希望得到的真正对象，还可以将其构造方法设置为private的方式，让调用者无法直接创建对象。客户端在调用的时候，代码量很少很容易写，而且可读性非常好。唯一的缺点可能就是，整个Builder模式的代码会变得更复杂。但是对于后期我们需要扩展或者有新需求的场景来说，这种复杂是值得的。  


## 5.scala中的Builder模式
现在项目中scala的使用场景也很多，下面手撕一个scala版本。  
首先还是Robot类  

```
class Robot(builder: RobotBuilder) {

    val model = builder.model
    val country = builder.country
    val price = builder.price

    override def toString: String = "model is: " + model + ", country is: " + country + ", price is: " + price

}
```  
RobotBuilder如下  

```
class RobotBuilder {

    var model = ""
    var country = ""
    var price = 0

    def setModel(model: String) = {
        this.model = model
        this
    }

    def setCountry(country: String) = {
        this.country = country
        this
    }

    def setPrice(price: Int) = {
        this.price = price
        this
    }

    def build = {
        new Robot(this)
    }

}
```  

客户端代码  

```
object Client {

    def main(args: Array[String]): Unit = {
        val robot : Robot = new RobotBuilder()
            .setModel("AA1")
            .setCountry("US")
            .setPrice(100)
            .build
        println(s"Robot:$robot")
    }

}

```  

上面这种方式与java中的处理方式类似，当Robot新增加了属性以后不需要增加新的构造函数，只需要在RobotBuilder中相应进行增加逻辑即可。  

## 6. case class的方式
scala很重要的一个特点就是不可变性。scala强调尽可能多使用val，少使用var，很明显上面的代码不符合这个原则。  
我们看看使用case class来解决这个问题。  

```
case class Robot(model: String = "", country: String = "", price: Int = 0) {
    override def toString: String = "model is: " + model + ", country is: " + country + ", price is: " + price
}

object Robot {

    def main(args: Array[String]): Unit = {
        val robot1 = Robot(model = "AA1", country = "US", price = 100)
        val robot2 = Robot(country = "CH")
        println(s"robot1 is: $robot1")
        println(s"robot2 is: $robot2")
    }
}
```  
代码更简洁，也更易于维护，更pure scala。  

## 7.  总结
经典的Builder创建模式UML图如下  
![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/service/design-pattern/1.png)    


其中  
Product是产品类，相当于我们例子中的Robot  
Builder是抽象类  
ConcretBuilder是具体的Builder实现类，相当于例子中的ImpBuilder  
Director为统一的组装过程，相当于例子中的RobotInstall  

通过上面的说明，可以得到Builder模式使用的场景大致如下:  
1.当对象具有大量可选参数时。  
2.当创建复杂对象的算法应该独立于该对象的组成部分以及它们的装配方式时。  
3.当构造过程必须允许被构造的对象有不同的表示时。  



