## 1.HashMap的基础结构
在1.7中，HashMap 底层是基于 数组 + 链表的结构组成。在1.8中，如果链表的长度大于一定的值，链表会转成红黑树。  

## 2.HashMap的参数(1.8)

```
    /**
     * The default initial capacity - MUST be a power of two.
     */
    static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16

    /**
     * The maximum capacity, used if a higher value is implicitly specified
     * by either of the constructors with arguments.
     * MUST be a power of two <= 1<<30.
     */
    static final int MAXIMUM_CAPACITY = 1 << 30;

    /**
     * The load factor used when none specified in constructor.
     */
    static final float DEFAULT_LOAD_FACTOR = 0.75f;

    /**
     * The bin count threshold for using a tree rather than list for a
     * bin.  Bins are converted to trees when adding an element to a
     * bin with at least this many nodes. The value must be greater
     * than 2 and should be at least 8 to mesh with assumptions in
     * tree removal about conversion back to plain bins upon
     * shrinkage.
     */
    static final int TREEIFY_THRESHOLD = 8;

    /**
     * The bin count threshold for untreeifying a (split) bin during a
     * resize operation. Should be less than TREEIFY_THRESHOLD, and at
     * most 6 to mesh with shrinkage detection under removal.
     */
    static final int UNTREEIFY_THRESHOLD = 6;

    /**
     * The smallest table capacity for which bins may be treeified.
     * (Otherwise the table is resized if too many nodes in a bin.)
     * Should be at least 4 * TREEIFY_THRESHOLD to avoid conflicts
     * between resizing and treeification thresholds.
     */
    static final int MIN_TREEIFY_CAPACITY = 64;
...

    /**
     * The number of key-value mappings contained in this map.
     */
    transient int size;
    ...
        /**
     * The next size value at which to resize (capacity * load factor).
     *
     * @serial
     */
    // (The javadoc description is true upon serialization.
    // Additionally, if the table array has not been allocated, this
    // field holds the initial array capacity, or zero signifying
    // DEFAULT_INITIAL_CAPACITY.)
    int threshold;

```  

DEFAULT_INITIAL_CAPACITY:16，数组的初始值，没太多好解释的。  
MAXIMUM_CAPACITY：最大值，基本上不会达到这个值。  
DEFAULT_LOAD_FACTOR：size / capacity(DEFAULT_INITIAL_CAPACITY)  
threshold: capacity * load factor，超过这个阈值会rehash。  

//一个桶的树化阈值  
//当桶中元素个数超过这个值时，需要使用红黑树节点替换链表节点  
//这个值必须为 8，要不然频繁转换效率也不高  
static final int TREEIFY_THRESHOLD = 8;  

//一个树的链表还原阈值  
//当扩容时，桶中元素个数小于这个值，就会把树形的桶元素 还原（切分）为链表结构  
//这个值应该比上面那个小，至少为 6，避免频繁转换  
static final int UNTREEIFY_THRESHOLD = 6;  

//哈希表的最小树形化容量  
//当哈希表中的容量大于这个值时，表中的桶才能进行树形化  
//否则桶内元素太多时会扩容，而不是树形化  
//为了避免进行扩容、树形化选择的冲突，这个值不能小于 4 * TREEIFY_THRESHOLD  
static final int MIN_TREEIFY_CAPACITY = 64;  

## 3.HashMap中DEFAULT_LOAD_FACTOR为什么是0.75
如果该值设为0.5，会在hashmap容量达到一半时候就扩容。比如从16扩大32，从32到64，64到128，浪费的空间会越来越大。  
而如果该值设置为1，则每次空间使用完毕才会扩容，put时候操作耗时会增加。  
所以0.75是时间与空间的一个平衡。  

## 4.put时候操作
1.7插入元素到单链表中采用头插入法，1.8采用的是尾插入法  

## 5.HashMap死循环
HashMap在并发执行put操作时会引起死循环，是因为多线程会导致HashMap的Entry链表形成环形数据结构。  

