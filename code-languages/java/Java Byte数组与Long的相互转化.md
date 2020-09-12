## 1.java.nio中的Buffer
java.nio(NEW IO)是JDK 1.4版本开始引入的一个新的IO API，可以替代标准的Java IO API。NIO与原来的IO有同样的作用和目的，但是使用的方式完全不同， NIO支持面向缓冲区的、基于通道的IO操作。 NIO将以更加高效的方式进行文件的读写操作。  

而缓冲区Buffer是一个容器对象，底层的存储结构为一个数组。在NIO中，所有的数据都是缓冲区来处理的。而使用缓冲区的好处显而易见：第一可以减少实际物理的读写次数，第二缓冲区创建初始就被分配了内存，这个内存空间一直在被重用，可以减少动态分配和回收内存的次数。  

在nio库中，Buffer是一个抽象类，具体的实现类可以参考下图  

![在这里插入图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/java/bytelong/1.png)  

## 2.long转byte数组

```
   public static byte[] toByteArray(long value) {
        return ByteBuffer.allocate(Long.SIZE / Byte.SIZE).putLong(value).array();
    }
```  

## 3.byte数组转long

```
    public static long byteArrayToLong(byte[] bytes) {
        ByteBuffer buffer = ByteBuffer.allocate(8);
        buffer.put(bytes, 0, bytes.length);
        buffer.flip();
        return buffer.getLong();
    }
```


## 4.allocate
上面的allocate方法，作用是从堆空间中分配一个容量大小为capacity的byte数组作为缓冲区的byte数据存储器，所有的数据操作，都是在这个byte数组中完成的。  