最近的项目需要使用到分词技术。本着不重复造轮子的原则，使用了ansj_seg来进行分词。本文结合博主使用经过，教大家用最快的速度上手使用ansj分词。  

## 1.给ansj来个硬广
项目的github地址：https://github.com/NLPchina/ansj_seg  
项目的文档地址：http://nlpchina.github.io/ansj_seg/  
首先必须感谢作者给我们提供这么好用的开源工具。  

## 2.配置maven
在maven项目的pom中配置ansj的dependency：  

```
<dependency>
	<groupId>org.ansj</groupId>
	<artifactId>ansj_seg</artifactId>
    <version>3.7.3-SNAPSHOT</version>
</dependency>
```  

## 3.使用实例
先不说那么多的理论，直接上可以run起来的代码。毕竟在工作过程中，解决问题是第一位的。只有解决完问题以后，我们才有功夫来慢慢研究其中的门道。  

对于分词来说，最重要的任务无非就是拿到切分以后的结果(词)。直接看代码：  

```
import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.ToAnalysis;

import java.util.*;

/**
 * Created by WangLei on 16-12-9.
 */
public class AnsjTest {

    public static void test() {
        //只关注这些词性的词
        Set<String> expectedNature = new HashSet<String>() {{
            add("n");add("v");add("vd");add("vn");add("vf");
            add("vx");add("vi");add("vl");add("vg");
            add("nt");add("nz");add("nw");add("nl");
            add("ng");add("userDefine");add("wh");
        }};
        String str = "欢迎使用ansj_seg,(ansj中文分词)在这里如果你遇到什么问题都可以联系我.我一定尽我所能.帮助大家.ansj_seg更快,更准,更自由!" ;
        Result result = ToAnalysis.parse(str); //分词结果的一个封装，主要是一个List<Term>的terms
        System.out.println(result.getTerms());

        List<Term> terms = result.getTerms(); //拿到terms
        System.out.println(terms.size());

        for(int i=0; i<terms.size(); i++) {
            String word = terms.get(i).getName(); //拿到词
            String natureStr = terms.get(i).getNatureStr(); //拿到词性
            if(expectedNature.contains(natureStr)) {
                System.out.println(word + ":" + natureStr);
            }
        }
    }

    public static void main(String[] args) {
        test();
    }
}
```  
将代码run起来：  

```
欢迎/v, 使用/v, ansj/en, _, seg/en, ,, (, ansj/en, 中文/nz, 分词/n, ), 在/p, 这里/r, 如果/c, 你/r, 遇到/v, 什么/r, 问题/n, 都/d, 可以/v, 联系/v, 我/r, ./m, 我/r, 一定/d, 尽/v, 我/r, 所/u, 能/v, ./m, 帮助/v, 大家/r, ./m, ansj/en, _, seg/en, 更/d, 快/a, ,, 更/d, 准/a, ,, 更/d, 自由/a, !]
45
欢迎:v
使用:v
中文:nz
分词:n
遇到:v
问题:n
可以:v
联系:v
尽:v
能:v
帮助:v
```  

上面的代码就拿到了我们想要的分词结果！  

## 4.词性
在作者的文档中，详细标明了相关词性：  

```
# 1. 名词  (1个一类，7个二类，5个三类)
名词分为以下子类：
n 名词
nr 人名
nr1 汉语姓氏
nr2 汉语名字
nrj 日语人名
nrf 音译人名
ns 地名
nsf 音译地名
nt 机构团体名
nz 其它专名
nl 名词性惯用语
ng 名词性语素
nw 新词
# 2. 时间词(1个一类，1个二类)
t 时间词
tg 时间词性语素
# 3. 处所词(1个一类)
s 处所词
# 4. 方位词(1个一类)
f 方位词
# 5. 动词(1个一类，9个二类)
v 动词
vd 副动词
vn 名动词
vshi 动词“是”
vyou 动词“有”
vf 趋向动词
vx 形式动词
vi 不及物动词（内动词）
vl 动词性惯用语
vg 动词性语素
# 6. 形容词(1个一类，4个二类)
a 形容词
ad 副形词
an 名形词
ag 形容词性语素
al 形容词性惯用语
# 7. 区别词(1个一类，2个二类)
b 区别词
bl 区别词性惯用语
# 8. 状态词(1个一类)
z 状态词
# 9. 代词(1个一类，4个二类，6个三类)
r 代词
rr 人称代词
rz 指示代词
rzt 时间指示代词
rzs 处所指示代词
rzv 谓词性指示代词
ry 疑问代词
ryt 时间疑问代词
rys 处所疑问代词
ryv 谓词性疑问代词
rg 代词性语素
# 10. 数词(1个一类，1个二类)
m 数词
mq 数量词
# 11. 量词(1个一类，2个二类)
q 量词
qv 动量词
qt 时量词
# 12. 副词(1个一类)
d 副词
# 13. 介词(1个一类，2个二类)
p 介词
pba 介词“把”
pbei 介词“被”
# 14. 连词(1个一类，1个二类)
c 连词
 cc 并列连词
# 15. 助词(1个一类，15个二类)
u 助词
uzhe 着
ule 了 喽
uguo 过
ude1 的 底
ude2 地
ude3 得
usuo 所
udeng 等 等等 云云
uyy 一样 一般 似的 般
udh 的话
uls 来讲 来说 而言 说来
uzhi 之
ulian 连 （“连小学生都会”）
# 16. 叹词(1个一类)
e 叹词
# 17. 语气词(1个一类)
y 语气词(delete yg)
# 18. 拟声词(1个一类)
o 拟声词
# 19. 前缀(1个一类)
h 前缀
# 20. 后缀(1个一类)
k 后缀
# 21. 字符串(1个一类，2个二类)
x 字符串
 xx 非语素字
 xu 网址URL
# 22. 标点符号(1个一类，16个二类)
w 标点符号
wkz 左括号，全角：（ 〔  ［  ｛  《 【  〖〈   半角：( [ { <
wky 右括号，全角：） 〕  ］ ｝ 》  】 〗 〉 半角： ) ] { >
wyz 左引号，全角：“ ‘ 『 
wyy 右引号，全角：” ’ 』
wj 句号，全角：。
ww 问号，全角：？ 半角：?
wt 叹号，全角：！ 半角：!
wd 逗号，全角：， 半角：,
wf 分号，全角：； 半角： ;
wn 顿号，全角：、
wm 冒号，全角：： 半角： :
ws 省略号，全角：……  …
wp 破折号，全角：——   －－   ——－   半角：---  ----
wb 百分号千分号，全角：％ ‰   半角：%
wh 单位符号，全角：￥ ＄ ￡  °  ℃  半角：$
```