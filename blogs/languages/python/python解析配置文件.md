最近有个python小项目，有一堆文件需要处理。所以将文件位置写入配置文件中，顺便写了一个解析配置文件的类，仅供大家参考，需要的同学请拿走  

```
#!/usr/bin/env python
#coding:utf-8

#-----------------------------------------------------
# author: wanglei
# date  : 20160321
# desc  : 解析配置文件
# pram  : 配置文件位置
#-----------------------------------------------------


import ConfigParser

class confParse(object):

    def __init__(self,conf_path):
        self.conf_path = conf_path
        self.conf_parser = ConfigParser.ConfigParser()
        self.conf_parser.read(conf_path)

    def get_sections(self):
        return self.conf_parser.sections()

    def get_options(self,section):
        return self.conf_parser.options(section)

    def get_items(self,section):
        return self.conf_parser.items(section)

    def get_val(self,section,option,is_bool = False,is_int = False):
        if is_bool and not is_int:
            #bool类型配置
            val = self.conf_parser.getboolean(section,option)
            return val
        elif not is_bool and is_int:
            val = self.conf_parser.getint(section,option)
            return val

        val = self.conf_parser.get(section,option)
        return val
```  



配置文件格式如下  


```
[labels_of_search]
base_dir = /home/lei.wang/datas/datas_user_label
cheap = %(base_dir)s/cheap_all
receptions = %(base_dir)s/receptions_all
breakfast = %(base_dir)s/breakfast_all

[result_file]
result_file = /home/lei.wang/datas/datas_user_label/hive_data/user_labels
```  

注意%(xxx)s的用法，xxx需要放在同一个section里  




