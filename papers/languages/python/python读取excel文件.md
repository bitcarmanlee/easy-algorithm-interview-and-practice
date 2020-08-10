## 0.前言
windows里做数据工作的杀手锏是excel。而且对于大部分产品，运营的同学来说，excel是最常用的工具，甚至都没有之一。但是RD的工作环境大部分情况下都是基于linux系统，linux的世界里是不认识excel这种格式的东东的。所以，在服务器上将excel文件转化成我们需要的格式就显得很常见。  

## 1.xlrd模块
python中的xlrd模块可以很方便的读取excel文件。使用  

```
pip install xlrd
```  

就可以很方便地安装此模块  

## 2.常用方式
### 1.打开一个excel文件

```
data = xlrd.open_workbook(file)
```  

### 2.得到一个工作表

```
table = data.sheets()[0] #通过索引的方式
table = data.sheet_by_name(sheet_name) #通过sheet的名字
```  

### 3.得到表的具体属性与数据

```
nrows = table.nrows #行
ncols = table.ncols #列
cell = table.cell(i,j).value.encode("utf-8") #得到具体一个cell的值
```  

## 3.操作excel表格代码

```
#!/usr/bin/env python
#coding:utf-8

import xlrd

def open_excel(file = "行业&包名mapping.xlsx"):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,ex:
        print ex


def readfile(file = "行业&包名mapping.xlsx"):
    data = open_excel(file)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols

    f = open("result","w")
    for i in range(nrows):
        line = ""
        for j in range(ncols):
            each_cell = table.cell(i,j).value.encode("utf-8") #得到具体一个cell的值                                                                                                                          
            line = line + each_cell + ","
        line = line[:-1]
        line += "\n"
        f.writelines(line)

def excel_table_byindex(file = "行业&包名mapping.xlsx", row_index=0,sheet_index=0):
    data = open_excel(file)
    table = data.sheets()[sheet_index]
    nrows = table.nrows #行
    ncols = table.ncols #列
    coldata = table.row_values(row_index) #一行，为一个list
    print ",".join(coldata)

def excel_table_byname(file = "行业&包名mapping.xlsx", col_index=0, sheet_name = u"Sheet1"):
    data = open_excel(file)
    table = data.sheet_by_name(sheet_name)
    nrows = table.nrows
    ncols = table.ncols
    coldata = table.col_values(col_index) #一列，为一个list
    print ",".join(coldata)

excel_table_byindex()
excel_table_byname()
```  