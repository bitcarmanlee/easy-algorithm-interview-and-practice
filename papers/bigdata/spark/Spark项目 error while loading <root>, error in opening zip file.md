IDE中的一个spark项目，从git上重新拉取代码以后，报了以下一堆错误：  

```
error: error while loading <root>, error in opening zip file
[ERROR] error: error while loading <root>, error in opening zip file
error: scala.reflect.internal.MissingRequirementError: object scala.runtime in compiler mirror not found.
    at scala.reflect.internal.MissingRequirementError$.signal(MissingRequirementError.scala:16)
    at scala.reflect.internal.MissingRequirementError$.notFound(MissingRequirementError.scala:17)
    at scala.reflect.internal.Mirrors$RootsBase.getModuleOrClass(Mirrors.scala:48)
    at scala.reflect.internal.Mirrors$RootsBase.getModuleOrClass(Mirrors.scala:40)
    at scala.reflect.internal.Mirrors$RootsBase.getModuleOrClass(Mirrors.scala:61)
    at scala.reflect.internal.Mirrors$RootsBase.getPackage(Mirrors.scala:172)
    at scala.reflect.internal.Mirrors$RootsBase.getRequiredPackage(Mirrors.scala:175)
    at scala.reflect.internal.Definitions$DefinitionsClass.RuntimePackage$lzycompute(Definitions.scala:183)
    at scala.reflect.internal.Definitions$DefinitionsClass.RuntimePackage(Definitions.scala:183)
    at scala.reflect.internal.Definitions$DefinitionsClass.RuntimePackageClass$lzycompute(Definitions.scala:184)
    at scala.reflect.internal.Definitions$DefinitionsClass.RuntimePackageClass(Definitions.scala:184)
    at scala.reflect.internal.Definitions$DefinitionsClass.AnnotationDefaultAttr$lzycompute(Definitions.scala:1024)
    at scala.reflect.internal.Definitions$DefinitionsClass.AnnotationDefaultAttr(Definitions.scala:1023)
    at scala.reflect.internal.Definitions$DefinitionsClass.syntheticCoreClasses$lzycompute(Definitions.scala:1153)
    at scala.reflect.internal.Definitions$DefinitionsClass.syntheticCoreClasses(Definitions.scala:1152)
    at scala.reflect.internal.Definitions$DefinitionsClass.symbolsNotPresentInBytecode$lzycompute(Definitions.scala:1196)
    at scala.reflect.internal.Definitions$DefinitionsClass.symbolsNotPresentInBytecode(Definitions.scala:1196)
    at scala.reflect.internal.Definitions$DefinitionsClass.init(Definitions.scala:1261)
    at scala.tools.nsc.Global$Run.<init>(Global.scala:1290)
    at scala.tools.nsc.Driver.doCompile(Driver.scala:32)
    at scala.tools.nsc.Main$.doCompile(Main.scala:79)
    at scala.tools.nsc.Driver.process(Driver.scala:54)
    at scala.tools.nsc.Driver.main(Driver.scala:67)
    at scala.tools.nsc.Main.main(Main.scala)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:498)
    at org_scala_tools_maven_executions.MainHelper.runMain(MainHelper.java:161)
    at org_scala_tools_maven_executions.MainWithArgsInFile.main(MainWithArgsInFile.java:26)
```  

思路一：因为项目代码中将scala从2.10.4升级为2.10.6。报错的信息里有提到`object scala.runtime in compiler mirror not found.`，猜测有可能是scala配置的问题？于是将本地的scala版本升级为2.10.6，发现无法解决问题。  

思路二：通过google各种搜索，有比较多的同学反映是本地maven仓库中有一些jar包因为各种各样的原因下载不完全，导致报错。于是先删除了本地maven库中scala相关的jar包，还是无法解决问题。  

思路三：沿着思路二，是本地仓库中某个jar包出错的概率比较大。但是debug信息中又没有明确指出哪个jar包有问题，比较坑爹。。看了一下本地的maven库，还好不到10G。于是一狠心，将本地maven库清空。再重新编译项目，OK！  