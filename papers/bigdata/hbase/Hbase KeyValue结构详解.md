## 1综述
Hbase是面向列的存储结构，而实际存储单元里存储的都是KeyValue结构。在看Hbase的API中，发现Hbase的API中就有KeyValue类，这个KeyValue类就是Hbase中数据存储的基本类型。那么这个KeyValue里到底包含哪些内容了？为了方便理解，特意为大家来剖析一下KeyValue类的结构。  

## 2.KeyValue类源码
首先为了从大体上了解KeyValue结构，我们可以先看看KeyValue类中源码上的关于此类的注释。不得不说，老外这点做得很好，基本会用言简意赅的语言来概括或者描述此部分代码。  

```
/**
 * An HBase Key/Value. This is the fundamental HBase Type.  
 * ...
 * KeyValue wraps a byte array and takes offsets and lengths into passed array at where to start
 * interpreting the content as KeyValue. The KeyValue format inside a byte array is:
 * <code>&lt;keylength> &lt;valuelength> &lt;key> &lt;value></code> Key is further decomposed as:
 * <code>&lt;rowlength> &lt;row> &lt;columnfamilylength> &lt;columnfamily> &lt;columnqualifier>
 * &lt;timestamp> &lt;keytype></code>
```  

这段注释就很关键信息量也很大：  
1.第一句话就告诉了我们，KeyValue是hbase中的基础类，很重要。  
2.后面那部分的信息就很关键了，其实就告诉了我们KeyValue中的结构：  
KeyValue的整体结构为：  
keylength  valuelength key value  
而Key的结构为：  
rowlength 	row	 columnfamilylength	 columnfamily	 columnqualifier	 timestamp	 keytype  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/bigdata/hbase/keyvalue/1.png)    

如果用一张图来形象描述，如上图所示，可以清楚表示KeyValue内部的存储结构！  

根据注释里的原文，我们还可以得知：HBase的KeyValue内部维护着一个字节数组，然后通过不同的偏移量来获取不同的部分。  

## 3.进一步细节
在KeyValue中，其中的KeyLength为4B：  

```
  /** Size of the key length field in bytes*/
  public static final int KEY_LENGTH_SIZE = Bytes.SIZEOF_INT;
```  

ValueLength标识Value在字节数组中所占的长度，为4B：  

```
  public static final int ROW_OFFSET =
    Bytes.SIZEOF_INT /*keylength*/ +
    Bytes.SIZEOF_INT /*valuelength*/;
```  

Column Family Length:储列簇Column Family的长度，为1B  
 

```
  /** Size of the family length field in bytes */
  public static final int FAMILY_LENGTH_SIZE = Bytes.SIZEOF_BYTE;
```  

Row Length：存储rowkey的长度，为2B  

```
  /** Size of the row length field in bytes */
  public static final int ROW_LENGTH_SIZE = Bytes.SIZEOF_SHORT;
```  

TimeStamp是Long型，肯定就是占8B了：  

```
  /** Size of the timestamp field in bytes */
  public static final int TIMESTAMP_SIZE = Bytes.SIZEOF_LONG;
```  

KeyType为1B：  

```
  /** Size of the key type field in bytes */
  public static final int TYPE_SIZE = Bytes.SIZEOF_BYTE;
```  

从ColumnQualifier开始内容前面不在带有长度了。TimeStamp和KeyType因为所占的长度是固定的，所以不用包含长度信息。而Qualifier的长度信息，则用以下的方式可以得出：  

```
  // Size of the length shorts and bytes in key.
  public static final int KEY_INFRASTRUCTURE_SIZE = ROW_LENGTH_SIZE
      + FAMILY_LENGTH_SIZE + TIMESTAMP_TYPE_SIZE;

  /**
   * @return Qualifier length
   */
  @Override
  public int getQualifierLength() {
    return getQualifierLength(getRowLength(),getFamilyLength());
  }

  /**
   * @return Qualifier length
   */
  private int getQualifierLength(int rlength, int flength) {
    return getKeyLength() - (int) getKeyDataStructureSize(rlength, flength, 0);
  }
```  

## 4.KeyValue的实现
在Hbase中，所有数据都是以Byte的形式存在的。在KeyValue中，使用的是byte数组来存储实际内容。  

```
  ////
  // KeyValue core instance fields.
  private byte [] bytes = null;  // an immutable byte array that contains the KV
  private int offset = 0;  // offset into bytes buffer KV starts at
  private int length = 0;  // length of the KV starting from offset.
```  

其中，bytes数组用来存储KeyValue中的实际内容，offset表示KeyValue在数组bytes中的起始位置，length则是KeyValue在数组bytes中自起始位置offset后的长度。  

KeyValue提供了一系列的Offset方法在数组中定位各个字段的的起始位置，如getValueOffset，getRowOffset等。也提供了一系列的length方法来获取KeyValue中各个字段的大小。  