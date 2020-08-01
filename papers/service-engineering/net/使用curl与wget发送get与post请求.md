## 1.发送get请求
用curl命令行发送get请求  

```
curl www.baidu.com
<!DOCTYPE html>
<!--STATUS OK--><html> <head><meta http-equiv=content-type content=text/html;charset=utf-8><meta http-equiv=X-UA-Compatible content=IE=Edge><meta content=always name=referrer><link rel=stylesheet type=text/css href=http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css><title>百度一下，你就知道</title></head> <body link=#0000cc> <div id=wrapper> <div id=head> <div class=head_wrapper> <div class=s_form> <div class=s_form_wrapper> <div id=lg> <img hidefocus=true src=//www.baidu.com/img/bd_logo1.png width=270 height=129> </div> <form id=form name=f action=//www.baidu.com/s class=fm> <input type=hidden name=bdorz_come value=1> <input type=hidden name=ie value=utf-8> <input type=hidden name=f value=8> <input type=hidden name=rsv_bp value=1> <input type=hidden name=rsv_idx value=1> <input type=hidden name=tn value=baidu><span class="bg s_ipt_wr"><input id=kw name=wd class=s_ipt value maxlength=255 autocomplete=off autofocus></span><span class="bg s_btn_wr"><input type=submit id=su value=百度一下 class="bg s_btn"></span> </form> </div> </div> <div id=u1> <a href=http://news.baidu.com name=tj_trnews class=mnav>新闻</a> <a href=http://www.hao123.com name=tj_trhao123 class=mnav>hao123</a> <a href=http://map.baidu.com name=tj_trmap class=mnav>地图</a> <a href=http://v.baidu.com name=tj_trvideo class=mnav>视频</a> <a href=http://tieba.baidu.com name=tj_trtieba class=mnav>贴吧</a> <noscript> <a href=http://www.baidu.com/bdorz/login.gif?login&amp;tpl=mn&amp;u=http%3A%2F%2Fwww.baidu.com%2f%3fbdorz_come%3d1 name=tj_login class=lb>登录</a> </noscript> <script>document.write('<a href="http://www.baidu.com/bdorz/login.gif?login&tpl=mn&u='+ encodeURIComponent(window.location.href+ (window.location.search === "" ? "?" : "&")+ "bdorz_come=1")+ '" name="tj_login" class="lb">登录</a>');</script> <a href=//www.baidu.com/more/ name=tj_briicon class=bri style="display: block;">更多产品</a> </div> </div> </div> <div id=ftCon> <div id=ftConw> <p id=lh> <a href=http://home.baidu.com>关于百度</a> <a href=http://ir.baidu.com>About Baidu</a> </p> <p id=cp>&copy;2017&nbsp;Baidu&nbsp;<a href=http://www.baidu.com/duty/>使用百度前必读</a>&nbsp; <a href=http://jianyi.baidu.com/ class=cp-feedback>意见反馈</a>&nbsp;京ICP证030173号&nbsp; <img src=//www.baidu.com/img/gs.gif> </p> </div> </div> </div> </body> </html>

```  

curl常用的参数如下:  

```
-o，--output：将信息输出到文件
-I，--head：仅返回头部信息
-d，--data：http post方式传送数据
```  

同样，wget也可以达到上面类似的目的:  

```
wget www.baidu.com
--2018-06-11 15:00:17--  http://www.baidu.com/
正在解析主机 www.baidu.com (www.baidu.com)... 61.135.169.125, 61.135.169.121
正在连接 www.baidu.com (www.baidu.com)|61.135.169.125|:80... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度： 2381 (2.3K) [text/html]
正在保存至: “index.html”

100%[=======================================================================================================================>] 2,381       --.-K/s   用时 0s    

2018-06-11 15:00:17 (297 MB/s) - 已保存 “index.html” [2381/2381])

```  

## 2.发送post请求

```
curl -d "param1=value1&param2=value2" "http://www.baidu.com"
```  

其中,`param1=value1&param2=value2`表示传入的参数，后面的则为请求的url。  

当然用wget也可以用来发post请求  

```
wget --post-data="param1=value1&param2=value2" "http://www.baidu.com"

```  

## 3.get与post的区别
1.GET 被强制服务器支持  
2.浏览器对URL的长度有限制，所以GET请求不能代替POST请求发送大量数据  
3.GET请求发送数据更小  
4.GET请求是安全的  
5.GET请求是幂等的  
6.POST请求不能被缓存  
7.POST请求相对GET请求是「安全」的  