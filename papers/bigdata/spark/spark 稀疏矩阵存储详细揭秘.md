spark mllib模块中，矩阵的表示位于org.apache.spark.mllib.linalg包的Matrices中。而Matrix的表示又分两种方式：dense与sparse。在实际场景应用场景中，因为大数据本身的稀疏性，sparse的方式比dense的方式使用更为频繁。而网络上大部分的资料对与sparse方式解释不是很清晰，本人也花了一些时间来理解，所以特此记录。  

## 1.稀疏矩阵的一些表达方式
### 1.1 coo
这种方式构造稀疏矩阵很容易理解，需要三个等长数组，alues数组存放矩阵中的非0元素，row indices存放非0元素的行坐标，column indices存放非0元素的列坐标。  
这种方式的优点：  
１．容易构造  
２．可以快速地转换成其他形式的稀疏矩阵  
３．支持相同的(row,col)坐标上存放多个值  
缺点如下：  
１．构建完成后不允许再插入或删除元素  
２．不能直接进行科学计算和切片操作  

### 1.2 csr_matrix
csr_matrix同样由3个数组组成，values存储非0元素，column indices存储非0元素的列坐标，row offsets依次存储每行的首元素在values中的坐标，如果某行全是0则对应的row offsets值为-1。  

这种方式的优点：  
１．高效地按行切片  
２．快速地计算矩阵与向量的内积  
３．高效地进行矩阵的算术运行，CSR + CSR、CSR * CSR等  
缺点：  
１．按列切片很慢（考虑CSC）  
２．一旦构建完成后，再往里面添加或删除元素成本很高  

### 1.3 csc_matrix
csr是基于行，则csc是基于列，特点自然跟csr_matrix类似。  

### 1.4 dia_matrix
对角线存储法，按对角线方式存，列代表对角线，行代表行。省略全零的对角线。  
适用场景：  
如果原始矩阵就是一个对角性很好的矩阵那压缩率会非常高，比如下图，但是如果是随机的那效率会非常糟糕。  

当然还有根据各种场景合适的存储方式，这里就不再一一列举了。  

## 2.spark中的稀疏矩阵表达
mllib中，稀疏矩阵可以用` Matrices.sparse`来生成。  
先看看SparseMatrix的源码：  

```
class SparseMatrix @Since("1.3.0") (
    @Since("1.2.0") val numRows: Int,
    @Since("1.2.0") val numCols: Int,
    @Since("1.2.0") val colPtrs: Array[Int],
    @Since("1.2.0") val rowIndices: Array[Int],
    @Since("1.2.0") val values: Array[Double],
    @Since("1.3.0") override val isTransposed: Boolean) extends Matrix {

  require(values.length == rowIndices.length, "The number of row indices and values don't match! " +
    s"values.length: ${values.length}, rowIndices.length: ${rowIndices.length}")
  // The Or statement is for the case when the matrix is transposed
  require(colPtrs.length == numCols + 1 || colPtrs.length == numRows + 1, "The length of the " +
    "column indices should be the number of columns + 1. Currently, colPointers.length: " +
    s"${colPtrs.length}, numCols: $numCols")
  require(values.length == colPtrs.last, "The last value of colPtrs must equal the number of " +
    s"elements. values.length: ${values.length}, colPtrs.last: ${colPtrs.last}")
  /**
   * Column-major sparse matrix.
   * The entry values are stored in Compressed Sparse Column (CSC) format.
   * ...
```  

上面代码的注释中，透露了一个很重要的信息：spark mllib中的稀疏矩阵是通过CSC的格式存储的！  

在spark shell中测试一下：  

```
scala> import org.apache.spark.mllib.linalg.Matrices
import org.apache.spark.mllib.linalg.Matrices

scala> val mx = Matrices.sparse(2,4, Array(0, 1, 2, 3, 4),Array(0, 1, 1, 1), Array(9, 8, 6, 5))
mx: org.apache.spark.mllib.linalg.Matrix = 
2 x 4 CSCMatrix
(0,0) 9.0
(1,1) 8.0
(1,2) 6.0
(1,3) 5.0
```  

根据源码可以看出，构造一个稀疏矩阵需要5个参数，分别为行、列，colPtrs为每列的首元素在values中的坐标，rowIndices为每个元素的行坐标，values为对应的值。  

## 3.如果有每行/每列均为0怎么办
CSC这种方式在存储矩阵的时候，有三个数组。最开始的时候，我想到一个问题：如果只存这三个数组，能完整表示这个稀疏矩阵么？  
答案是不能。为什么呢？这个问题经过作者深入思考，原因如下。  
比如上面的矩阵为一个2*4的矩阵，具体形式为：     
9 0 0 0   
0 8 6 5  
如果给上面矩阵添加一行全0行，  
9 0 0 0  
0 8 6 5  
0 0 0 0  
大家会发现这个稀疏矩阵按CSC的方式存储，对应的三个数组与上面的矩阵是一样的！  
因为colPtrs为矩阵的列数+1，所以如果只存三个数组，只能确定矩阵的列数，无法确定矩阵的行数，矩阵往后面追加再多的全0行，对应的三个数组都是一样的！  
所以在构造方法中，才会要求指定矩阵的行数与列数！  
我们可以在spark shell中再尝试一下：  

```
scala> val mx = Matrices.sparse(3,4, Array(0, 1, 2, 3, 4),Array(0, 1, 1, 1), Array(9, 8, 6, 5))
mx: org.apache.spark.mllib.linalg.Matrix = 
3 x 4 CSCMatrix
(0,0) 9.0
(1,1) 8.0
(1,2) 6.0
(1,3) 5.0

scala> val mx = Matrices.sparse(4,4, Array(0, 1, 2, 3, 4),Array(0, 1, 1, 1), Array(9, 8, 6, 5))
mx: org.apache.spark.mllib.linalg.Matrix = 
4 x 4 CSCMatrix
(0,0) 9.0
(1,1) 8.0
(1,2) 6.0
(1,3) 5.0

```  
我们不改变后面三个数组的值，只改变构造函数中的行数，可以看出就构造除了不同的稀疏矩阵！