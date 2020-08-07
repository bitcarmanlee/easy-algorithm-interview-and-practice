## 1.问题描述
新安装的ubuntu18系统，自己下载的软件包安装好以后，无法将启动图标固定在dock栏上，导致每次启动都要去软件安装的目录中执行对应的启动脚本，非常不方便。为了解决上述问题，可以采用如下解决方案。    

## 2.解决办法
以pycharm为例  

在`~/.local/share/applications`目录中，新建pycharm.desktop文件  

```
[Desktop Entry]

Encoding=UTF-8

Name=PyCharm

Exec=.../soft/pycharm-community-2020.1.1/bin/pycharm.sh
Icon=.../soft/pycharm-community-2020.1.1/bin/pycharm.svg

Terminal=false

Type=Application

Categories=Development
```  

对应的Exec是pycharm的启动脚本位置，Icon是对应的图标位置。  

添加完上述文件以后，点击左下角的“显示应用程序”，然后找到pycharm的图标，右击，选择添加到收藏夹即可。  

## 3. 消除侧边栏出现两个图标
启动时，侧边栏会出现两个图标，体验还是很差的。  
具体的解决方案：  
在terminate中执行`xprop |grep WM_CLASS`，此时鼠标会变成一个十字的准星。此时点击已经打开的pycharm界面，会出现如下内容：  

`WM_CLASS(STRING) = "jetbrains-pycharm-ce", "jetbrains-pycharm-ce"`  

然后在pycharm.desktop后面添加一行：  
`StartupWMClass=jetbrains-pycharm-ce`  
即可。  