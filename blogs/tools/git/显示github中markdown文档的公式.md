github项目中有很多.md文档，这种文档就是markdown形式。发现自己的浏览器里打开这些文档的时候，没法正常显示公式，显示的都是公式的markdown代码形式，例如这种形式  

```
$$ \Vert\vec{x}\Vert_1=\sum_{i=1}^N\vert{x_i}\vert $$
```  

为了在浏览器中能正确显示上述公式，我们可以采取如下方式  

在chrome的扩展程序中，打开chrome网上应用店，然后搜索MathJax Plugin for Github，下载该插件，并且启用，就可以让上述公式正常显示。    

安装过程中提示”程序包无效。详细信息：无法加载扩展程序图标icon16.png"。  
试了很多次，包括清除浏览器缓存，重启机器等方法，都无效。然后想了想，是不是可以通过下载github源码的方式来安装。果断试了试，安装成功，把过程记录一下。  

1.在github上搜索需要的插件名称，进入项目，下载到本地的某个位置，使用git clone xxx即可。  
2.在更多工具里选择扩展程序。或者直接在浏览器中输入chrome://extensions/。  
3.勾选Developer Mode（即开发者模式）。  
4.点击Load unpacked extension...，如果是中文版点击加载已解压的扩展程序...，找到刚刚clone下来的文件夹地址，确定即可。  
5.上面几步就将插件安装好了，去掉Developer Mode开发者模式即可。  
