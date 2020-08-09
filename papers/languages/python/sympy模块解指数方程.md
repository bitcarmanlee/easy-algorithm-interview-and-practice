遇到一个形如$\alpha * e^{-29} = 0.1$的方程，求解$\alpha$的值。  
python中的sympy模块可以很轻松地解决这个问题。具体代码如下  

```
from sympy.abc import x, y, z, a, b
from sympy import exp

print sympy.solve(exp(-1 * x * 29) - 0.1, x)
```  

求解可得$\alpha$的值为0.0793994859653119  