## 1.应用场景
java中有丰富的集合类，日常开发中几乎时刻需要使用到各种各样的集合类，其中常用的集合类包括有Map,Set,List,Array等等。下面我们就来针对各个集合类的相互转化做一下总结。  

## 2.实测代码
二话不说，直接上代码。  

```
import org.junit.Test;

import java.util.*;

/**
 * Created by WangLei on 17-12-18.
 */
public class CollectionsTest {

    Map<String, Integer> map = new HashMap<String, Integer>() {{
        put("a", 1);
        put("b", 2);
        put("c", 3);
    }};

    Set<String> set = new HashSet() {{
        add("a");
        add("b");
        add("c");
    }};

    List<String> list = new ArrayList() {{
        add("a");
        add("b");
        add("c");

    }};

    String[] arr = {"a", "b", "c"};

    @Test
    public void map2List() {
        List<String> keyList = new ArrayList(map.keySet());
        System.out.println("keyList is: " + keyList);
        //ArrayList有如下构造方法：public ArrayList(Collection<? extends E> c)
        List<String> valueList = new ArrayList(map.values());
        System.out.println("valueList is: " + valueList);
    }

    @Test
    public void map2set() {
        Set<String> keySet = map.keySet();
        //HashSet有如下构造方法：public HashSet(Collection<? extends E> c)
        Set<String> valueSet = new HashSet(map.values());
        System.out.println("valueSet is: " + valueSet);
    }

    @Test
    public void arrayset() {
        // array -> set
        Set<String> set = new HashSet(Arrays.asList(arr));
        System.out.println("set is: " + set);
        //set -> array
        String[] resultArray = set.toArray(new String[set.size()]);
        Arrays.stream(resultArray).forEach(x -> System.out.print(x + " "));
    }

    @Test
    public void listset() {
        // list -> set
        Set<String> resultset = new HashSet<>(list);
        System.out.println("result set is: " + resultset);
        // set -> list
        List<String> resultlist = new ArrayList(set);
        System.out.println("result list is: " + resultlist);
    }

    @Test
    public void listarray() {
        // list -> array
        String[] resultarray = list.toArray(new String[list.size()]);
        // array -> list
        List<String> resultlist = Arrays.asList(arr);
    }
}
```  

代码中方法的名称就表示了该方法的用途，就不一一解释了。  

## 3.几个注意的小点
1.ArrayList,HashSet等集合类都有`public ArrayList(Collection<? extends E> c)`这种形式的构造方法，可以传一个集合进来初始化。  

2.Set，List等接口都有toArray方法，源码如下：  

```
<T> T[] toArray(T[] a);
```  

2.`Arrays.asList`方法的源码如下：  

```
    public static <T> List<T> asList(T... a) {
        return new ArrayList<>(a);
    }
```  

可以直接将数组变为一个ArrayList  