项目中经常有发送http请求的需求，现在将java,python,scala中发送http请求的方法稍作记录，以备不时之需。  

## 1.java版本
java代码相对来说最为冗长。。。这也是java的一贯风格。。。  

```
import org.apache.commons.lang3.StringUtils;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;


public class HttpUtils {

    protected static Logger LOGGER = LoggerFactory.getLogger(HttpUtils.class);

    public static HttpClient httpClient = new DefaultHttpClient();

    public static String getResponse(String url, int retryTimes) {
        for(int i = 0; i < retryTimes; i++) {
            LOGGER.info("get response with the request: {}", url);
            try {
                HttpResponse response = httpClient.execute(new HttpGet(url));
                HttpEntity entity = response.getEntity();
                if(response.getStatusLine().getStatusCode() == 200) {
                    String res = genResponseContext(entity.getContent());
                    if(StringUtils.isNotBlank(res)) return res;
                }

            } catch (Exception ex) {
                System.out.println("get response with error");
                ex.printStackTrace();
                LOGGER.error("get response with error: \n", ex);
                try {
                    Thread.sleep(1000 * (i + 1));
                } catch (InterruptedException interEx) {
                    interEx.printStackTrace();
                }
            }
        }

        return StringUtils.EMPTY;
    }

    public static String genResponseContext(InputStream is) {
        BufferedReader reader = null;
        try {
            StringBuilder sb = new StringBuilder();
            reader = new BufferedReader(new InputStreamReader(is));
            String line;
            while( (line = reader.readLine()) != null) {
                sb.append(line).append("\n");
            }
            return sb.toString().trim();
        } catch (Exception ex) {
            LOGGER.error("get response error: {} \n", ex);
            return null;
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (Exception e) {
                }
            }
        }
    }

    public static void main(String[] args) {
        String url = "http://www.baidu.com";
        String result = getResponse(url, 2);
        System.out.println(result);
    }
}

```  

## 2.python版本  
python代码相对来说就简单很多了。。。  

```
#!/usr/bin/env python
# -*- coding: utf-8

import urllib2


def send_http_request(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = response.read()
    print data


send_http_request("http://www.baidu.com")
```  

## 3.scala版本  
scala也是JVM系，所以跟java版本有一点像，但简洁很多。  

```
import org.apache.http.client.methods.HttpGet
import org.apache.http.impl.client.DefaultHttpClient

import scala.io.Source

object HttpUtils {

    def send_http_request(url: String): Unit = {
        val httpclient = new DefaultHttpClient()
        try {
            val response = httpclient.execute(new HttpGet(url))
            val entity = response.getEntity
            val result = Source.fromInputStream(entity.getContent).getLines().mkString("\n")
            println(result)
        } catch {
            case ex: Exception => ex.printStackTrace()
        }
    }

    def main(args: Array[String]): Unit = {
        val url = "http://www.baidu.com"
        send_http_request(url)
    }
}

```
