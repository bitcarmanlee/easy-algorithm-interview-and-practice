mac中，sublime全部查找替换的快捷键为option + cmd + f   

现在要想批量在行首添加注释，可以有以下操作：  
先按option + cmd + f，在find what中输入 ^,查找到所有的行首，然后就可以在行首批量添加。  
同理，要想在行末批量添加，  
先按option + cmd + f，在find what中输入 $,查找到所有的行尾，然后就可以在行尾批量添加。  

需要注意的是，以上操作需要将左下方的Regular expression激活，因为^,$是正则表达式的写法  