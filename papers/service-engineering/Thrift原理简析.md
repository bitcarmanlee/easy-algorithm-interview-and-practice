Apache Thrift是一个跨语言的服务框架,本质上为RPC，同时具有序列化、反序列化机制；当我们开发的service需要开放出去的时候,就会遇到跨语言调用的问题,JAVA语言开发了一个UserService用来提供获取用户信息的服务,如果服务消费端有PHP/Python/C++等,我们不可能为所有的语言都适配出相应的调用方式,有时候我们会很无奈的使用Http来作为访问协议;但是如果服务消费端不能使用HTTP,而且更加倾向于以操作本地API的方式来使用服务,那么我们就需要Thrift来提供支持.  

不过,如果你的JAVA服务,并没有跨语言调用的需求,那么使用thrift作为RPC框架,似乎不是最好的选择,不管thrift是否性能优越,但是它使用起来确实没有类似于Hessian/CXF等那样便捷和易于使用.  


本文以UserService为例,描述一下使用thrift的方式,以及其原理..  

## 1. service.thrift

```
struct User{  
    1:i64 id,  
    2:string name,  
    3:i64 timestamp,  
    4:bool vip    
}  
  
service UserService{  
    User getById(1:i64 id)  
}
```  

你可以将自己的JAVA服务通过".thrift"文件描述出来,并提供给服务消费端,那么消费端即可以生成自己的API文件..Thrift框架目前已经支持大部分主流的语言,.需要注意,因为Thrift考虑到struct/service定义需要兼容多种语言的"风格",所以它只支持一些基本的数据类型(比如i32,i64,string等),以及service定义的方法不能重名,即使参数列表不同.(并不是所有的语言都能像JAVA一样支持重载)  

## 2. 生成API文件
首先下载和安装thrift客户端,比如在windows平台下,下载thrift.exe,不过此处需要提醒,不同的thrift客户端版本生成的API可能不兼容.本例使用thrift-0.9.0.exe;通过"--gen"指定生成API所适配的语言.本实例为生成java客户端API.  

```
> thrift.exe --gen java -o service service.thrift  
```  

需要明确的是:Thrift和其他RPC框架不同,thrift在生成的API文件中,已经描述了"调用过程"(即硬编码),而不是像其他RPC那样在运行时(runtime)动态解析方法调用或者参数.  

## 3. UserService实现类

```
public class UserServiceImpl implements UserService.Iface {  
    @Override  
    public User getById(long id){  
        System.out.println("invoke...id:" + id);  
        return new User();//for test  
    }  
}  
```  

实现类,需要放在Thrift server端.    

## 4.原理简析
User.java: thrift生成API的能力还是非常的有限,比如在struct中只能使用简单的数据类型(不支持Date,Collection&lt;?&gt;等),不过我们能从User中看出,它生成的类实现了"Serializable"接口和"TBase"接口  

其中Serializable接口表明这个类的实例是需要序列化之后在网络中传输的,为了不干扰JAVA本身的序列化和反序列化机制,它还重写了readObject和writeObject方法.不过这对thrift本身并没有帮助.  

TBase接口是thrift序列化和反序列化时使用的,它的两个核心方法:read和write.在上述的thrift文件中,struct定义的每个属性都有一个序号,比如:1:id,那么thrift在序列化时,将会根据序号的顺序依次将属性的"名称 + 值"写入inputStream中,反序列化也是如此.(具体参见read和write的实现).  

```
//read方法逐个读取字段,按照"索引",最终将"struct"对象封装完毕.  
//write方法也非常类似,按照"索引"顺序逐个输出到流中.  
while (true){  
        schemeField = iprot.readFieldBegin();  
        if (schemeField.type == org.apache.thrift.protocol.TType.STOP) {   
          break;  
        }  
        switch (schemeField.id) {  
          case 1: // ID  
            if (schemeField.type == org.apache.thrift.protocol.TType.I32) {  
              struct.id = iprot.readI32();  
              struct.setIdIsSet(true);  
            } else {   
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);  
            }  
            break;  
          case 2: // NAME  
          ..  
        }  
}  
```  

因为thrift的序列化和反序列化实例数据时,是根据"属性序号"进行,这可以保证数据在inputstream和outputstream中顺序是严格的,此外每个struct中"序号"不能重复,但是可以不需要从"1"开始.如果"序号"有重复,将导致无法生成API文件.这一点也要求API开发者,如果更改了thrift文件中的struct定义,需要重新生成客户端API,否则服务将无法继续使用(可能报错,也可能数据错误).thrift序列化/反序列化的过程和JAVA自带的序列化机制不同,它将不会携带额外的class结构,此外thrift这种序列化机制更加适合网络传输,而且性能更加高效.  



UserService.Client:  在生成的UserService中,有个Client静态类,这个类就是一个典型的代理类,此类已经实现了UserService的所有方法.开发者需要使用Client类中的API方法与Thrift server端交互,它将负责与Thrift server的Socket链接中,发送请求和接收响应.  

需要注意的时,每次Client方法调用,都会在一个Socket链接中进行,这就意味着,在使用Client消费服务之前,需要和Thrift server建立有效的TCP链接.(稍后代码示例)  

1) 发送请求:  


```
//参见:TServiceClient  
//API方法调用时,发送请求数据流  
protected void sendBase(String methodName, TBase args) throws TException {  
    oprot_.writeMessageBegin(new TMessage(methodName, TMessageType.CALL, ++seqid_));//首先写入"方法名称"和"seqid_"  
    args.write(oprot_);//序列化参数  
    oprot_.writeMessageEnd();  
    oprot_.getTransport().flush();  
}  
  
protected void receiveBase(TBase result, String methodName) throws TException {  
    TMessage msg = iprot_.readMessageBegin();//如果执行有异常  
    if (msg.type == TMessageType.EXCEPTION) {  
      TApplicationException x = TApplicationException.read(iprot_);  
      iprot_.readMessageEnd();  
      throw x;  
    }//检测seqid是否一致  
    if (msg.seqid != seqid_) {  
      throw new TApplicationException(TApplicationException.BAD_SEQUENCE_ID, methodName + " failed: out of sequence response");  
    }  
    result.read(iprot_);//反序列化  
    iprot_.readMessageEnd();  
}  
```  

Thrift提供了简单的容错方式:每次方法调用,都会在Client端标记一个seqid,这是一个自增的本地ID,在TCP请求时将此seqid追加到流中,同时Server端响应时,也将此seqid原样返回过来;这样客户端就可以根据此值用来判断"请求--响应"是对应的,如果出现乱序,将会导致此请求以异常的方式结束.  

2) 响应  

```
/参考: TBaseProcessor.java  
@Override  
public boolean process(TProtocol in, TProtocol out) throws TException {  
    TMessage msg = in.readMessageBegin();  
    ProcessFunction fn = processMap.get(msg.name);//根据方法名,查找"内部类"  
    if (fn == null) {  
      TProtocolUtil.skip(in, TType.STRUCT);  
      in.readMessageEnd();  
      TApplicationException x = new TApplicationException(TApplicationException.UNKNOWN_METHOD, "Invalid method name: '"+msg.name+"'");  
      out.writeMessageBegin(new TMessage(msg.name, TMessageType.EXCEPTION, msg.seqid));  
      x.write(out);//序列化响应结果,直接输出  
      out.writeMessageEnd();  
      out.getTransport().flush();  
      return true;  
    }  
    fn.process(msg.seqid, in, out, iface);  
    return true;  
}  
```  

thrift生成的UserService.Processor类,就是server端用来处理请求过程的"代理类";server端从socket中读取请求需要调用的"方法名" +参数列表,并交付给Processor类处理;和其他的RPC调用不同的时,thrift并没有使用类似于"反射机制"的方式来调用方法,而是将UserService的每个方法生成一个"内部类":  

```
public static class getById<I extends Iface> extends org.apache.thrift.ProcessFunction<I, getById_args> {  
  public getById() {  
    super("getById");//其中getById为标识符  
  }  
  
  public getById_args getEmptyArgsInstance() {  
    return new getById_args();  
  }  
  
  protected boolean isOneway() {  
    return false;  
  }  
  //实际处理方法  
  public getById_result getResult(I iface, getById_args args) throws org.apache.thrift.TException {  
    getById_result result = new getById_result();  
    result.success = iface.getById(args.id);//直接调用实例的具体方法，硬编码  
    return result;  
  }  
}  
```  

这个"内部类",将会在Processor初始化的时候,放入到一个map中,此后即可以通过"方法名"查找,然后调用其"getResult"方法了.由此可见，thrift客户端与server端均没有使用到“反射机制”，全程都是硬编码实现，之所以这么做的原因可能是考虑到性能，也可能是考虑到开发者可以在生成的代码基础上任意调整以适应特殊的情况；如果使用反射机制，将会无法兼顾上述2个情况。  

```
public static class Processor<I extends Iface> extends org.apache.thrift.TBaseProcessor<I> implements org.apache.thrift.TProcessor {  
  
    public Processor(I iface) {  
      super(iface, getProcessMap(new HashMap<String, org.apache.thrift.ProcessFunction<I, ? extends org.apache.thrift.TBase>>()));  
    }  
  
    protected Processor(I iface, Map<String,  org.apache.thrift.ProcessFunction<I, ? extends  org.apache.thrift.TBase>> processMap) {  
      super(iface, getProcessMap(processMap));  
    }  
  
    private static <I extends Iface> Map<String,  org.apache.thrift.ProcessFunction<I, ? extends  org.apache.thrift.TBase>> getProcessMap(Map<String,  org.apache.thrift.ProcessFunction<I, ? extends  org.apache.thrift.TBase>> processMap) {  
      //放入map  
      processMap.put("getById", new getById());  
      return processMap;  
    }  
    ....  
}  
```  

3) Server端Socket管理和执行策略  

```
TThreadPoolServer  
public void serve() {  
    try {  
      //启动服务  
      serverTransport_.listen();  
    } catch (TTransportException ttx) {  
      LOGGER.error("Error occurred during listening.", ttx);  
      return;  
    }  
  
    // Run the preServe event  
    if (eventHandler_ != null) {  
      eventHandler_.preServe();  
    }  
  
    stopped_ = false;  
    setServing(true);  
    //循环,直到被关闭  
    while (!stopped_) {  
      int failureCount = 0;  
      try {  
        //accept客户端Socket链接,  
        //对于每个新链接,将会封装成runnable,并提交给线程或者线程池中运行.  
        TTransport client = serverTransport_.accept();  
        WorkerProcess wp = new WorkerProcess(client);  
        executorService_.execute(wp);  
      } catch (TTransportException ttx) {  
        if (!stopped_) {  
          ++failureCount;  
          LOGGER.warn("Transport error occurred during acceptance of message.", ttx);  
        }  
      }  
    }  
    //....  
}  
```  

Thrift Server端,设计思路也非常的直接...当前Service server启动之后,将会以阻塞的方式侦听Socket链接(代码参考TThreadPoolServer),每建立一个Socket链接,都会将此Socket经过封装之后,放入线程池中,本质上也是一个Socket链接对应一个Worker Thread.这个Thread只会处理此Socket中的所有数据请求,直到Socket关闭.  

```
//参考:WorkerProcess  
while (true) {  
  
    if (eventHandler != null) {  
      eventHandler.processContext(connectionContext, inputTransport, outputTransport);  
    }  
  
    if(stopped_ || !processor.process(inputProtocol, outputProtocol)) {  
      break;  
    }  
}  
```  

当有Socket链接不是很多的时候,TThreadPoolServer并不会有太大的性能问题,可以通过指定ThreadPool中线程的个数进行简单的调优..如果Socket链接很多,我们只能使用TThreadedSelectorServer来做支撑,TThreadedSelectorServer内部基于NIO模式,具有异步的特性,可以极大的提升server端的并发能力;不过在绝大多数情况下,在thrift中使用"异步"似乎不太容易让人接受,毕竟这意味着Client端需要阻塞,并且在高并发环境中这个阻塞时间是不可控的.但SelecorServer确实可以有效的提升Server的并发能力，而且在一定程度上可以提升吞吐能力，这或许是我们优化Thrift Server比较可靠的方式之一.  

## 3. Client端代码示例

```
public class UserServiceClient {  
  
    public void startClient() {  
        TTransport transport;  
        try {  
            transport = new TSocket("localhost", 1234);  
            TProtocol protocol = new TBinaryProtocol(transport);  
            UserService.Client client = new UserService.Client(protocol);  
            transport.open();  
            User user = client.getById(1000);  
            ////  
            transport.close();  
        } catch (TTransportException e) {  
            e.printStackTrace();  
        } catch (TException e) {  
            e.printStackTrace();  
        }  
    }  
  
}  
```  

## 4.Server端代码示例 

```
public class Server {  
    public void startServer() {  
        try {  
            TServerSocket serverTransport = new TServerSocket(1234);  
            UserService.Processor process = new Processor(new UserServiceImpl());//入口  
            Factory portFactory = new TBinaryProtocol.Factory(true, true);  
            Args args = new Args(serverTransport);  
            args.processor(process);  
            args.protocolFactory(portFactory);  
            TServer server = new TThreadPoolServer(args);  
            server.serve();  
        } catch (TTransportException e) {  
            e.printStackTrace();  
        }  
    }  
}  
```  

到这里,你就会发现,一个service,需要server端启动一个ServerSocket,而且还需要指定一个Processor，此Processor通常已经有thrift编译器生成好了。那么Processor在初始化（参见上述源码），将会为每个方法创建一个内部类的实例，并保存在map中，那么当socket中有请求时，将会反序列化字节流并解析出“方法名”、参数列表，然后根据方法名，从map中查询出方法对应的实例（有点command模式），我们从上述源码中已经知道，每个方法对应的内部类都实现了统一的接口，此时只需要执行相应的方法即可（比如getResult方法），这些方法内部都是硬编码直接调用service实现类的实际方法，而且service的实例在创建Processor实例时已经传递过去。  

如果你有很多service,它们需要使用不同的端口，不过通常需要让这些service尽可能的分布在不同的物理server上,否则一个物理server上运行太多的ServerSocket进程并不是一件让人愉快的事情. 或者你让几个service整合成一个.  
 
问题总没有想象的那么简单,其实service被拆分的粒度越细,越容易被部署和扩展,对于负载均衡就更加有利.如何让一个service分布式部署,稍后再继续分享.  

## 5.总结:
1) thrift文件定义struct和serivice API,此文件可以被其他语言生成API文件或者类文件.  
2) 使用thrift客户端生成API文件  
3) JAVA服务端(即服务提供端),实现service功能.  
4) 服务端将server发布成一个Thrift server: 即将service嵌入到一个serverSocket中.  
5) 客户端启动Socket,并和Thrift server建立TCP连接.并使用Client代理类操作远程接口.  

原文链接地址：http://shift-alt-ctrl.iteye.com/blog/1987416
其他参考资料地址：https://www.kancloud.cn/digest/thrift/118984
