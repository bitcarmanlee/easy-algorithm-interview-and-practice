## 1.求整数的n次方
现在想求$m^n$的值，如何用比较快速的方法求得上述值？  
例如我们想求$12^{75}$的值，快速解法如下：  
1.75的二进制数形式为1001011   
2.$12^{75} = 12^{64} * 12^8 * 12 ^ 2 * 12$  
具体求解的时候，我们先计算$12^1$，然后根据$12^1$求$12^2$，再根据$12^2$求$12^4$，以此类推，最后求$12^64$，即75的二进制数形式总共为多少位，我们就要在原基础上平方几次。这样，就将复杂度为n的计算降到了log(n)。  

直接看代码  

```
    public void power() {
	    // 测试4^5的值
        int n = 4, m = 5;
        int power2num = n;
        int result = 1;
        while(m != 0) {
	        // 只有当最低位为1时，结果才乘上现在的值
            if ((m & 1) != 0)
                result *= power2num;
            // 每移位一次，幂方计算一次
            power2num *= power2num;
            m >>= 1;
        }
    }
```  

## 2.求矩阵的n次方
矩阵n次方的求法与整数n次方的求法思路类似。代码如下  

先看两个矩阵相乘的代码  

```
    public long[][] matrixMult(long[][] a, long[][] b) {
        // a的列必须与b的行相等
        assert a.length == b[0].length;
        int n = a.length, m = a[0].length, p = b[0].length;
        long[][] result = new long[n][p];
        //矩阵乘法的基本方式为三层循环
        for(int i=0; i<n; i++) {
            for(int j=0; j<p; j++) {
                for(int k=0; k<m; k++) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return result;
    }
```  

```
    public long[][] matrixPower(long[][] matrix, int p) {
        long[][] result = new long[matrix.length][matrix[0].length];

        for(int i=0; i<result.length; i++) {
            result[i][i] = 1;
        }

        long[][] pingfang = matrix;
        for(; p != 0; p >>= 1) {
            if((p & 1) != 0) {
                // 注意result在前面
                result = matrixMult(result, pingfang);
            }
            pingfang = matrixMult(pingfang, pingfang);
        }
        return result;
    }
```  
