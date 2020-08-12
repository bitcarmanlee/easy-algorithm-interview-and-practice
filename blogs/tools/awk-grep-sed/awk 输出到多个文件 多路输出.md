awk中经常需要根据不同条件，将内容输出到不同文件中。写了个简单的awk小脚本，可以满足这个需求。  

```
#!/bin/awk -f

{
    if(NR==FNR)
        {a[$0]++}
    else
        {if($1 in a)
            print $0 >> "user_agence"
         else
            print $0 >> "user_no_agence"
        }
}
```  

按照以上方式，就将不同的内容输出到了多个文件中。  