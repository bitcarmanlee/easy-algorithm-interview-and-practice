## 1.BLAS(Basic Linear Algebra Subprograms)与LAPACK (Linear Algebra PACKage)
Blas是Netlib基于Fortran实现的基本向量乘法，矩阵乘法的一种科学计算函数库。  

Fortran语言是为了满足数值计算的需求而发展出来的。1953年12月，IBM公司工程师约翰·巴科斯（J. Backus）因深深体会编写程序很困难，而写了一份备忘录给董事长斯伯特·赫德（Cuthbert Hurd），建议为IBM704系统设计全新的电脑语言以提升开发效率。当时IBM公司的顾问冯·诺伊曼强烈反对，因为他认为不切实际而且根本不必要。但赫德批准了这项计划。1957年，IBM公司开发出第一套FORTRAN语言，在IBM704电脑上运作。历史上第一支FORTRAN编程在马里兰州的西屋贝地斯核电厂试验。1957年4月20日星期五的下午，一位IBM软件工程师决定在电厂内编译第一支FORTRAN编程，当代码输入后，经过编译，打印机列出一行消息：“源程序错误……右侧括号后面没有逗号”，这让现场人员都感到讶异，修正这个错误后，打印机输出了正确结果。而西屋电气公司因此意外地成为FORTRAN的第一个商业用户。1958年推出FORTRAN Ⅱ，几年后又推出FORTRAN Ⅲ，1962年推出FORTRAN Ⅳ后，开始广泛被使用。      

1966年，美国标准化协会制定了Fortran（x3.9-1966，也就是Fortran 66）和Fortran（x3.10-1966）标准。这时Fortran语言还不是结构化的程序设计语言。  

1976年，美国标准化协会重新对Fortran（x3.9-1966）进行了评估，公布了新的Fortran标准，也就是Fortran 77。Fortran 77是具有结构化特性的编程语言。Fortran77在短时间内获取了巨大的成功，广泛地应用于科学和工程计算，几乎统治了数值计算领域。  

1980年，Fortran 77被ISO接纳为国际标准。  

1991年发布的Fortran 90大幅改进了旧版Fortran的型式，加入了面向对象的观念与提供指针，并同时加强数组的功能。(参考文献1)  

后来，Netlib实现的这个代码库对应的接口规范被称为BLAS。  

LAPACK也是Netlib用Fortan编写的代码库，实现了高级的线性运算功能，例如矩阵分解，求逆等，底层是调用的BLAS代码库。后来LAPACK也变成一套代码接口标准。  

因此，BLAS与LAPACK有狭义与广义上两种含义  
狭义上，其对应Netlib实现的代码库  
广义上，其对应Netlib实现的代码库对应的接口规范。  

## 2.ATLAS(Automatically Tuned Linear Algebra Software)
ATLAS与OpenBLAS是对应BLAS/LAPACK的开源版本，他们实现了BLAS的全部功能与接口，并对计算过程进行了优化，因此计算速度更快。  

## 3.MKL
MKL是Intel对BLAS/LAPACK的实现，属于商业库。既然是Intel出品，肯定会基于Intel的CPU架构对算法实现相应的优化，因此计算速度更快。  

## 4.EIGEN
EIGEN是基于C++实现的可以用来进行线性代数、矩阵、向量操作等运算的库，采用源码的方式提供给用户，支持多平台。  



## 参考文献
1.https://zh.wikipedia.org/wiki/Fortran