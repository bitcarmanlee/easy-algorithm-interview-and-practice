## 1.jar包中的资源文件
在日常项目中，经常会将一些资源文件或者配置文件打入最终的jar包中。我们可以查看jar包中是否包含这个文件，但是无法看到jar包中这个文件的具体内容。这个时候怎么办呢？下面教大家一种比较简单快捷的方式。  

## 2.读取jar包中的资源文件
假设项目A中，resources里有个zookeeper.properties的文件。打包的时候，这个zookeeper.properties自然被打入了A.jar，而且是在classpath里。  
现在我们的需求是从这个A.jar中查看zookeeper.properties的具体内容，步骤如下。  
1.新起一个maven工程，这个工程只需将项目A导入dependency里即可，这样A.jar就会在External Libraries里。  
2.然后新建一个类。代码如下  

```
import org.junit.Test;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * Created by WangLei on 18-9-25.
 */
public class ReadZkConfig {

    @Test
    public void test()  {
        InputStream stream =  ReadZkConfig.class.getClassLoader().getResourceAsStream("zookeeper.properties");
        BufferedReader br = new BufferedReader(new InputStreamReader(stream));
        String line;
        try {
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

}
```  

注意jar包中的资源文件无法以file的方式读取，需要用stream的方式读取。
