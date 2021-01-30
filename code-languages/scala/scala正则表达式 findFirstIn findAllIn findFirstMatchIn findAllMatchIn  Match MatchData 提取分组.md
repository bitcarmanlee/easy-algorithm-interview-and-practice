## 0.引子  
节前最后一个工作日，在编写一个简单的正则表达式的时候，卡了比较长的时间。后来总结发现，还是对正则表达式的理解不是很深刻，于是利用假期的时间，特意比较详细地看了一下正则表达式相关内容并加以记录。  

## 1.findFirstIn findFirstMatchIn
正则表达式中常用的方法包括findFirstIn，findFirstMatchIn等类似的方法。先来看个例子，通过例子我们来看两者区别。  

```
  @Test
  def test() = {
    val s = "你好，今天是2021年1月2日18点30分"
    val pattern = """今天是\d+年\d+月\d+日""".r
    val result1 = pattern.findFirstIn(s)
    println(result1)
    val result2 = pattern.findFirstMatchIn(s) match {
      case Some(data) => {
        println("data type is: " + data.getClass.getSimpleName)
        data group 0
      }
      case _ => "empty"
    }
    println(result2)
  }
```  

输出结果：  

```
Some(今天是2021年1月2日)
data type is: Match
今天是2021年1月2日
```  


简单看下源码  

```
  /** Return an optional first matching string of this `Regex` in the given character sequence,
   *  or None if there is no match.
   *
   *  @param source The text to match against.
   *  @return       An [[scala.Option]] of the first matching string in the text.
   *  @example      {{{"""\w+""".r findFirstIn "A simple example." foreach println // prints "A"}}}
   */
  def findFirstIn(source: CharSequence): Option[String] = {
    val m = pattern.matcher(source)
    if (m.find) Some(m.group) else None
  }
```  

firdFirstIn是scala.util.matching.Regex的方法。该方法的输入是一个source，source类型为CharSequence接口，最常见的实现类为字符串。  
返回值为Option[String]。在我们的例子中，因为匹配上了，所以返回的值为Some[String]。  

```
  /** Return an optional first match of this `Regex` in the given character sequence,
   *  or None if it does not exist.
   *
   *  If the match is successful, the [[scala.util.matching.Regex.Match]] can be queried for
   *  more data.
   *
   *  @param source The text to match against.
   *  @return       A [[scala.Option]] of [[scala.util.matching.Regex.Match]] of the first matching string in the text.
   *  @example      {{{("""[a-z]""".r findFirstMatchIn "A simple example.") map (_.start) // returns Some(2), the index of the first match in the text}}}
   */
  def findFirstMatchIn(source: CharSequence): Option[Match] = {
    val m = pattern.matcher(source)
    if (m.find) Some(new Match(source, m, groupNames)) else None
  }
```  

findFirstMatchIn看源码与firdFirstIn差别不大，最大的不同在于返回的类型为Option[Match]。  

## 2.Match MatchData
看下Match的源码  

```
  /** Provides information about a successful match. */
  class Match(val source: CharSequence,
              private[matching] val matcher: Matcher,
              val groupNames: Seq[String]) extends MatchData {

    /** The index of the first matched character. */
    val start = matcher.start

    /** The index following the last matched character. */
    val end = matcher.end

    /** The number of subgroups. */
    def groupCount = matcher.groupCount

    private lazy val starts: Array[Int] =
      ((0 to groupCount) map matcher.start).toArray
    private lazy val ends: Array[Int] =
      ((0 to groupCount) map matcher.end).toArray

    /** The index of the first matched character in group `i`. */
    def start(i: Int) = starts(i)

    /** The index following the last matched character in group `i`. */
    def end(i: Int) = ends(i)

    /** The match itself with matcher-dependent lazy vals forced,
     *  so that match is valid even once matcher is advanced.
     */
    def force: this.type = { starts; ends; this }
  }
```  

第一行注释非常关键，告诉了我们Match类最重要的作用：Provides information about a successful match。如果匹配成功，这个类会给我们提供一些匹配成功的信息，包括匹配成功的起始位置等。  
Match类继承了MatchData，我们再看看MatchData的源码  

```
 trait MatchData {

    /** The source from which the match originated */
    val source: CharSequence

    /** The names of the groups, or an empty sequence if none defined */
    val groupNames: Seq[String]

    /** The number of capturing groups in the pattern.
     *  (For a given successful match, some of those groups may not have matched any input.)
     */
    def groupCount: Int

    /** The index of the first matched character, or -1 if nothing was matched */
    def start: Int

    /** The index of the first matched character in group `i`,
     *  or -1 if nothing was matched for that group.
     */
    def start(i: Int): Int
	...

    /** The matched string in group `i`,
     *  or `null` if nothing was matched.
     */
    def group(i: Int): String =
      if (start(i) >= 0) source.subSequence(start(i), end(i)).toString
      else null
	...

    /** Returns the group with given name.
     *
     *  @param id The group name
     *  @return   The requested group
     *  @throws   NoSuchElementException if the requested group name is not defined
     */
    def group(id: String): String = nameToIndex.get(id) match {
      case None => throw new NoSuchElementException("group name "+id+" not defined")
      case Some(index) => group(index)
    }
```  
MatchData里面用得最多，最重要的方法应该就是group了，group最大的作用，就是用来提起分组。  

## 3.提取分组

```
  @Test
  def test() = {
    val s = "你好，今天是2021年1月2日18点30分"
    val pattern = """今天是(\d+)年(\d+)月(\d+)日""".r
    val result = pattern.findFirstMatchIn(s)
    val year = result match {
      case Some(data) => data group 1
      case _ => "-1"
    }
    println(year)  // 结果为 2021
  }
```  

上面的例子就是提取分组的一个典型例子，就是利用findFirstMatchIn的group方法，提取匹配结果的第一个分组，就得到了年份数据。  

## 4.提取分组的另外一种方式
实际中提取分组还有另外一种常用方式。  

```
  @Test
  def test() = {
    val s = "你好，今天是2021年1月2日18点30分"
    val pattern = """今天是(\d+)年(\d+)月(\d+)日""".r
    val pattern(year, month, day) = s
    println(s"year is $year.\n" +
      f"month is $month.\n" + raw"day is $day")
  }
```  

上面的代码看起来很正常，完全没毛病，但实际上却会报错有问题，本人就是在这里被卡了很长时间。  

```
scala.MatchError: 你好，今天是2021年1月2日18点30分 (of class java.lang.String)

	at com.xiaomi.mifi.pdata.common.T4.t8(T4.scala:114)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	...
```  

当时百思不得其解，不知道问题出在哪里。仔细看了源码以后，才明白什么情况。如果我们在IDE中点击  
```val pattern(year, month, day) = s```  
这一行查看源码，会发现调用的其实是unapplySeq方法。  

```
  def unapplySeq(s: CharSequence): Option[List[String]] = s match {
    case null => None
    case _    =>
      val m = pattern matcher s
      if (runMatcher(m)) Some((1 to m.groupCount).toList map m.group)
      else None
  }
```  

这个方法上面有一段关键的注释  

```
  /** Tries to match a [[java.lang.CharSequence]].
   *
   *  If the match succeeds, the result is a list of the matching
   *  groups (or a `null` element if a group did not match any input).
   *  If the pattern specifies no groups, then the result will be an empty list
   *  on a successful match.
   *
   *  This method attempts to match the entire input by default; to find the next
   *  matching subsequence, use an unanchored `Regex`.
```  

这个方法默认是匹配整个输出，如果是要匹配子串，需要用unanchored这种方式。  

将上面的代码稍作改动  
```
  @Test
  def test() = {
    val s = "你好，今天是2021年1月2日18点30分"
    val pattern = """今天是(\d+)年(\d+)月(\d+)日""".r.unanchored
    val pattern(year, month, day) = s
    println(s"year is $year.\n" +
      f"month is $month.\n" + raw"day is $day")
  }
```  

可以得到我们预期的结果  

```
year is 2021.
month is 1.
day is 2
```  

## 5.findAllIn findAllMatchIn  
findAllIn与firdFirstIn对应，findAllMatchIn与findFirstMatchIn对应，表示所有匹配结果。  
先来看一个例子  

```
  @Test
  def t9() = {
    val dateRegex =  """(\d{4})-(\d{2})-(\d{2})""".r
    val dates = "dates in history: 2004-01-20, 2005-02-28, 1998-01-15, 2009-10-25"
    val result =  dateRegex.findAllIn(dates)
    val array =  for (each <- result) yield each
    println(array)
    println(array.mkString("\t"))
  }
```  

```
non-empty iterator
2004-01-20	2005-02-28	1998-01-15	2009-10-25
```  

findAllIn的方法签名如下：  
```
  /** Return all non-overlapping matches of this `Regex` in the given character 
   *  sequence as a [[scala.util.matching.Regex.MatchIterator]],
   *  which is a special [[scala.collection.Iterator]] that returns the
   *  matched strings but can also be queried for more data about the last match,
   *  such as capturing groups and start position.
   ....

  def findAllIn(source: CharSequence) = new Regex.MatchIterator(source, this, groupNames)
```  

返回的是一个MatchIterator，根据注释信息可以看出来MatchIterator是scala.collection.Iterator的一个特例，所以直接println(array)得到的信息是一个non-empty iterator。  

如果我们想得到所有能匹配上的年份，则可以使用findAllMatchIn方法。该方法可以得到先得到所有的Match对象，然后再分组提取出年份即可。  

```
  @Test
  def t10() = {
    val dateRegex =  """(\d{4})-(\d{2})-(\d{2})""".r
    val dates = "dates in history: 2004-01-20, 2005-02-28, 1998-01-15, 2009-10-25"
    val result = dateRegex.findAllMatchIn(dates)
    val array = for(each <- result) yield each.group(1)
    println(array)
    println(array.mkString("\t"))
  }
```  

最后的输出结果为  

```
non-empty iterator
2004	2005	1998	2009
```




