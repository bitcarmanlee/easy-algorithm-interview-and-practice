## 1.安装sublime
这步没啥好说的，自己去sublime官网下载安装即可。

## 2.安装package control
可以直接采取在线安装的形式  
按  

```
ctrl+`
```  

的快捷键，调出console控制台。注意`是tab键上方的按键。    
在控制台中输入  

```
import urllib.request,os; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); open(os.path.join(ipp, pf), 'wb').write(urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ','%20')).read())
```  

正常情况下开始下载安装。  

如果安装过程中，出现unable to download xxx 的提示，可以用以下办法解决  


在Perferences -> Package Settings -> Package Control -> Settings-User中，添加如下内容  
```
	"downloader_precedence":
	{
		"linux":
		[
			"curl",
			"urllib",
			"wget"
		],
		"osx":
		[
			"curl",
			"urllib"
		],
		"windows":
		[
			"wininet"
		]
	},
```  

最后该配置文件变为  

```
{
	"bootstrapped": true,
	"downloader_precedence":
	{
		"linux":
		[
			"curl",
			"urllib",
			"wget"
		],
		"osx":
		[
			"curl",
			"urllib"
		],
		"windows":
		[
			"wininet"
		]
	},
	"in_process_packages":
	[
	],
	"installed_packages":
	[
		"Package Control",
		"SqlBeautifier"
	]
}

```  

然后就可以正常下载了。  


## 3. 下载插件
package control下载完成以后，在Perferences -> Package Control中打开，然后找到install packages，在弹出的对话框中输入想要安装的插件即可。  

以SQL格式化工具SqlBeautifier为例，在对话框中输入SqlBeautifier，然后下载安装即可。  

在Mac机器上，选择对应的SQL语句，先按command+K，再按command+F，即可格式化SQL。  