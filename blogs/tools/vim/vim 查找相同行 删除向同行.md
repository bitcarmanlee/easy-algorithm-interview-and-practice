## vim 查找相同的两行
思路：先将两行排序，然后查找前一行等于后一行的内容  

```
:sort
/^\(.\+\)$\n\1
```  

`^\(.\+\)$\n`表示一整行的模式，`\1`表示第一个组  

## vim删除相同的行
给出vim wiki上的两种解法，链接如下：  
http://vim.wikia.com/wiki/Uniq_-_Removing_duplicate_lines  

There are two versions (and \v "verymagic" version as a variant of the second): the first leaves only the last line, the second leaves only the first line. (Use \zs for speed reason.)  


```
g/^\(.*\)\n\1$/d
g/\%(^\1\n\)\@<=\(.*\)$/d
g/\v%(^\1\n)@<=(.*)$/d
```  

Breakdown of the second version:  

```
g/\%(^\1\n\)\@<=\(.*\)$/d
g/                     /d  <-- Delete the lines matching the regexp
            \@<=           <-- If the bit following matches, make sure the bit preceding this symbol directly precedes the match
                \(.*\)$    <-- Match the line into subst register 1
  \%(     \)               <-- Group without placing in a subst register.
     ^\1\n                 <-- Match subst register 1 followed the new line between the 2 lines
```  

具体就不解释了，自行看解释（其实主要是我自己也没看太明白，哈哈）