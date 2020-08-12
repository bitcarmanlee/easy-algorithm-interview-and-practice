简单明了，实现strip（）函数的功能  

```
function ltrim(s) { sub(/^[ \t\r\n]+/, "", s); return s }
function rtrim(s) { sub(/[ \t\r\n]+$/, "", s); return s }
function trim(s) { return rtrim(ltrim(s)); }
```  

```
BEGIN{
        FS=","
}

{
        $0 = rtrim($0);
        if($2!="-" && $3=="-")
                a[$4]++;
        {
        if($4!="-")
                b[$4]++;
        else
                b[$5]++;
        }
}

END{
        print "   client    incr_num_day";
        for(i in a) printf("%10s   %d\n",i,a[i])
        print "\n\n   client    all_num";                                                                                                                                                     
        for(j in b) printf("%10s   %d\n",j,b[j]);
}
```  

下面为调用函数的一个小实例  