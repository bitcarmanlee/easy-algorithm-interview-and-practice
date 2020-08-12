在日常开发中通常我们会存储配置参数信息到属性文件，这些属性文件最常见的就是键值对文件。对于配置文件来说，最常见的操作无非就这两种：读与写。以下针对这两种场景我们来做一个详细的示例。  

## 1.读取properties文件中的键值对
假设我们在与src平级的路径中有一个conf文件夹，里面有个province.properties的属性文件，文件里的内容格式如下：  

```
北京市={"citycode":"010","adcode":"110100","name":"北京市","center":"116.405285,39.904989","level":"city","districts":[{"citycode":"010","adcode":"110101","name":"东城区","center":"116.418757,39.917544","level":"district","districts":[]},{"citycode":"010","adcode":"110102","name":"西城区","center":"116.366794,39.915309","level":"district","districts":[]},{"citycode":"010","adcode":"110105","name":"朝阳区","center":"116.486409,39.921489","level":"district","districts":[]},{"citycode":"010","adcode":"110106","name":"丰台区","center":"116.286968,39.863642","level":"district","districts":[]},{"citycode":"010","adcode":"110107","name":"石景山区","center":"116.195445,39.914601","level":"district","districts":[]},{"citycode":"010","adcode":"110108","name":"海淀区","center":"116.310316,39.956074","level":"district","districts":[]},{"citycode":"010","adcode":"110109","name":"门头沟区","center":"116.105381,39.937183","level":"district","districts":[]},{"citycode":"010","adcode":"110111","name":"房山区","center":"116.139157,39.735535","level":"district","districts":[]},{"citycode":"010","adcode":"110112","name":"通州区","center":"116.658603,39.902486","level":"district","districts":[]},{"citycode":"010","adcode":"110113","name":"顺义区","center":"116.653525,40.128936","level":"district","districts":[]},{"citycode":"010","adcode":"110114","name":"昌平区","center":"116.235906,40.218085","level":"district","districts":[]},{"citycode":"010","adcode":"110115","name":"大兴区","center":"116.338033,39.728908","level":"district","districts":[]},{"citycode":"010","adcode":"110116","name":"怀柔区","center":"116.637122,40.324272","level":"district","districts":[]},{"citycode":"010","adcode":"110117","name":"平谷区","center":"117.112335,40.144783","level":"district","districts":[]},{"citycode":"010","adcode":"110118","name":"密云区","center":"116.843352,40.377362","level":"district","districts":[]},{"citycode":"010","adcode":"110119","name":"延庆区","center":"115.985006,40.465325","level":"district","districts":[]}]}

```  

现在我们想把里层的name解析出来，代码如下  

```
    @Test
    public void test() throws IOException {
        Properties prop = new Properties();
        String str = Demo1.class.getClassLoader().getResource("").getPath();
        String input = str + "/conf/province.properties";
        InputStream is = new BufferedInputStream(new FileInputStream(
        prop.load(new InputStreamReader(is,"UTF-8"));
        // 如下写法也可以：
        // InputStream is = XXXClass.class.getClassLoader().getResourceAsStream("province.properties");
        Set<Object> keySet = prop.keySet();
        for(String key: keySet.toArray(new String[keySet.size()])) {
            String line = prop.getProperty(key);
            JSONObject json = JSONObject.fromObject(line);
            JSONArray jsonArray = json.getJSONArray("districts");
            for(int i=0; i < jsonArray.size(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                String name = jsonObject.getString("name");
                System.out.println(name);
            }
        }
    }
```  

api层面的使用方式很简单，使用Properties对象的getProperty方法就可以找到对应属性的值。如果没有找到相应属性，则返回null。  

## 2.向内存或属性文件中写入键值对
上面的例子中我们演示了如何读取键值对，接下来我们再演示一下如何写入键值对。  

```
    @Test
    public void test()  {
        try {
            OutputStream os = new FileOutputStream("test.properties");
            Properties prop = new Properties();
            prop.setProperty("name", "leilei");
            prop.setProperty("age", "18");
            prop.setProperty("interest", "algorithm"); //将键值对写入内存

			//通过keySet遍历
            Set<Object> keys = prop.keySet();
            for (String key : keys.toArray(new String[0])) {
                System.out.println(key + "\t" + prop.get(key));
            }

			//通过entrySet遍历
            Set<Map.Entry<Object,Object>> entrys = prop.entrySet();
            for(Map.Entry<Object,Object> entry: entrys) {
                System.out.println(entry.getKey().toString() + "\t" + entry.getValue().toString());
            }

			//通过propertyNames遍历
            Enumeration<?> e = prop.propertyNames();
            while(e.hasMoreElements()) {
                String key = (String) e.nextElement();
                String value = prop.getProperty(key);
                System.out.println(key + "\t" + value);
            }

            prop.store(os, "test properties " + new Date().toString()); //写入文件
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

```  

Properties类可以通过setProperty方法将键值对保存到内存中，此时可以通过getProperty方法读取。如果我们想将键值对持久化到文件中，可以使用store()方法将键值对写入到属性文件中。  
