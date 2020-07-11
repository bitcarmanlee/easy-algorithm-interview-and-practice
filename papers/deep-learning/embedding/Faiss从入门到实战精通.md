## 1.Faiss是什么
Faiss是Facebook Ai Research开发的一款稠密向量检索工具。引用Faiss Wiki上面的一段简介  

```
Faiss is a library for efficient similarity search and clustering of dense vectors.
It contains algorithms that search in sets of vectors of any size, up to ones that possibly do not fit in RAM.
It also contains supporting code for evaluation and parameter tuning. 
Faiss is written in C++ with complete wrappers for Python (versions 2 and 3).
Some of the most useful algorithms are implemented on the GPU. 
It is developed by Facebook AI Research.
```  

上面的简介包含了如下信息：  
1. Faiss是针对稠密向量进行相似性搜索和聚类的一个高效类库。  
2. 它包含可搜索任意大小的向量集的算法，这些向量集的大小甚至都不适合RAM。  
3. 它还包含用于评估和参数调整的支持代码。  
4. Faiss用C ++编写，并且有python2与python3的封装代码。   
5. 一些最有用的算法在GPU上有实现。  
6. Faiss是由Facebook AI Research开发的。  

## 2.faiss安装
在[No module named swigfaiss](https://blog.csdn.net/bitcarmanlee/article/details/106317279)  
中有简单介绍，可以用如下方式安装  

```
#cpu 版本
conda install faiss-cpu -c pytorch
# GPU 版本
conda install faiss-gpu cudatoolkit=8.0 -c pytorch # For CUDA8
conda install faiss-gpu cudatoolkit=9.0 -c pytorch # For CUDA9
conda install faiss-gpu cudatoolkit=10.0 -c pytorch # For CUDA10
```  

## 3.faiss的使用方法简介
整体来说，faiss的使用方式可以分为三个步骤：  
1.构建训练数据以矩阵的形式表示，比如我们现在经常使用的embedding，embedding出来的向量就是矩阵的一行。  
2.为数据集选择合适的index，index是整个faiss的核心部分，将第一步得到的训练数据add到index当中。  
3.search，或者说query，搜索到最终结果。  

## 4.faiss原理与核心算法

faiss的主要功能是对向量进行相似搜索。具体就是给定一个向量，在所有已知的向量库中找出与其相似度最高的一些向量，本质是一个KNN(K近邻)问题，比如google的以图找图功能。随着目前embedding的流行，word2vec,doc2vec,img2vec,item2vec,video2vec,everything2vec，所以faiss也越来越受到大家的欢迎。  

根据上面的描述不难看出，faiss本质是一个向量(矢量)数据库，这个数据库在进行向量查询的时候有其独到之处，因此速度比较快，同时占用的空间也比较小。  

faiss中最重要的是索引Index，具体的索引类型见参考文献2.  

<table role="table">
<thead>
<tr>
<th>Method</th>
<th>Class name</th>
<th><code>index_factory</code></th>
<th>Main parameters</th>
<th>Bytes/vector</th>
<th>Exhaustive</th>
<th>Comments</th>
</tr>
</thead>
<tbody>
<tr>
<td>Exact Search for L2</td>
<td><code>IndexFlatL2</code></td>
<td><code>"Flat"</code></td>
<td><code>d</code></td>
<td><code>4*d</code></td>
<td>yes</td>
<td>brute-force</td>
</tr>
<tr>
<td>Exact Search for Inner Product</td>
<td><code>IndexFlatIP</code></td>
<td><code>"Flat"</code></td>
<td><code>d</code></td>
<td><code>4*d</code></td>
<td>yes</td>
<td>also for cosine (normalize vectors beforehand)</td>
</tr>
<tr>
<td>Hierarchical Navigable Small World graph exploration</td>
<td><code>IndexHNSWFlat</code></td>
<td>'HNSWx,Flat`</td>
<td>
<code>d</code>, <code>M</code>
</td>
<td><code>4*d + 8 * M</code></td>
<td>no</td>
<td></td>
</tr>
<tr>
<td>Inverted file with exact post-verification</td>
<td><code>IndexIVFFlat</code></td>
<td><code>"IVFx,Flat"</code></td>
<td>
<code>quantizer</code>, <code>d</code>, <code>nlists</code>, <code>metric</code>
</td>
<td><code>4*d</code></td>
<td>no</td>
<td>Take another index to assign vectors to inverted lists</td>
</tr>
<tr>
<td>Locality-Sensitive Hashing (binary flat index)</td>
<td><code>IndexLSH</code></td>
<td>-</td>
<td>
<code>d</code>, <code>nbits</code>
</td>
<td><code>nbits/8</code></td>
<td>yes</td>
<td>optimized by using random rotation instead of random projections</td>
</tr>
<tr>
<td>Scalar quantizer (SQ) in flat mode</td>
<td><code>IndexScalarQuantizer</code></td>
<td><code>"SQ8"</code></td>
<td><code>d</code></td>
<td><code>d</code></td>
<td>yes</td>
<td>4 bit per component is also implemented, but the impact on accuracy may be inacceptable</td>
</tr>
<tr>
<td>Product quantizer (PQ) in flat mode</td>
<td><code>IndexPQ</code></td>
<td><code>"PQx"</code></td>
<td>
<code>d</code>, <code>M</code>, <code>nbits</code>
</td>
<td>
<code>M</code> (if nbits=8)</td>
<td>yes</td>
<td></td>
</tr>
<tr>
<td>IVF and scalar quantizer</td>
<td><code>IndexIVFScalarQuantizer</code></td>
<td>"IVFx,SQ4" "IVFx,SQ8"</td>
<td>
<code>quantizer</code>, <code>d</code>, <code>nlists</code>, <code>qtype</code>
</td>
<td>SQfp16: 2 * <code>d</code>, SQ8: <code>d</code> or SQ4: <code>d/2</code>
</td>
<td>no</td>
<td>there are 2 encodings: 4 bit per dimension and 8 bit per dimension</td>
</tr>
<tr>
<td>IVFADC (coarse quantizer+PQ on residuals)</td>
<td><code>IndexIVFPQ</code></td>
<td><code>"IVFx,PQy"</code></td>
<td>
<code>quantizer</code>, <code>d</code>, <code>nlists</code>, <code>M</code>, <code>nbits</code>
</td>
<td>
<code>M+4</code> or <code>M+8</code>
</td>
<td>no</td>
<td>the memory cost depends on the data type used to represent ids (int or long), currently supports only nbits &lt;= 8</td>
</tr>
<tr>
<td>IVFADC+R (same as IVFADC with re-ranking based on codes)</td>
<td><code>IndexIVFPQR</code></td>
<td><code>"IVFx,PQy+z"</code></td>
<td>
<code>quantizer</code>, <code>d</code>, <code>nlists</code>, <code>M</code>, <code>nbits</code>, <code>M_refine</code>, <code>nbits_refine</code>
</td>
<td>
<code>M+M_refine+4</code> or <code>M+M_refine+8</code>
</td>
<td>no</td>
<td></td>
</tr>
</tbody>  


上面的索引中，三个最重要的索引为IndexFlatL2,IndexIVFFlat,IndexIVFPQ。下面针对这三种索引来进行分析与说明。  

## 5.IndexFlatL2
看到这个名字大家应该就能猜个八九不离十。没错，这种索引的方式是计算L2距离，为一种暴力的(brute-force))精确搜索的方式，计算方式自然就是计算各向量的欧式距离(L2距离)。  

看一下官方给的一个例子  

```
import numpy as np
d = 64                           # dimension
nb = 100000                      # database size
nq = 10000                       # nb of queries
np.random.seed(1234)             # make reproducible
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000. # # 每一项增加了一个等差数列的对应项数
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.


import faiss                   # make faiss available
index = faiss.IndexFlatL2(d)   # build the index
print(index.is_trained)        # 表示索引是否需要训练的布尔值
index.add(xb)                  # add vectors to the index
print(index.ntotal)            # 索引中向量的数量。


k = 4                          # we want to see 4 nearest neighbors
D, I = index.search(xb[:5], k) # sanity check
print(I)
print(D)

D, I = index.search(xq, k)     # actual search
print(I[:5])                   # neighbors of the 5 first queries
print(I[-5:])                  # neighbors of the 5 last qu
```  

输出结果为  

```
True
100000
[[  0 393 363  78]
 [  1 555 277 364]
 [  2 304 101  13]
 [  3 173  18 182]
 [  4 288 370 531]]
[[0.        7.1751733 7.207629  7.2511625]
 [0.        6.3235645 6.684581  6.7999454]
 [0.        5.7964087 6.391736  7.2815123]
 [0.        7.2779055 7.5279865 7.6628466]
 [0.        6.7638035 7.2951202 7.3688145]]
[[ 381  207  210  477]
 [ 526  911  142   72]
 [ 838  527 1290  425]
 [ 196  184  164  359]
 [ 526  377  120  425]]
[[ 9900 10500  9309  9831]
 [11055 10895 10812 11321]
 [11353 11103 10164  9787]
 [10571 10664 10632  9638]
 [ 9628  9554 10036  9582]]
```  

具体的步骤为：  
一、构建数据集  
1.xb相当于数据库中待搜索的向量，这些向量都会建立索引并且我们会进行搜索，xb的大小为nb * d。  
2.xq为查询向量，我们期望找到xb中xq的K近邻向量。xq的大小为xq * d。如果是查询单个向量，nq = 1。  
二、构建索引  
三、搜索  

IndexFlatL2的结果是精确，可以用来作为其他索引测试中准确性程度的参考。当数据集比较大的时候，暴力搜索的时间复杂度很高，因此我们一般会使用其他方式的索引。  

## 6.IndexIVFFlat
上面的IndexFlatL2为暴力搜索，速度慢，实际中我们需要更快的方式，于是就有了IndexIVFFlat。  
为了加快搜索的速度，我们可以将数据集分割为几部分，将其定义为Voronoi Cells，每个数据向量只能落在一个cell中。查询时只需要查询query向量落在cell中的数据了，降低了距离计算次数。  
IndexIVFFlat需要一个训练的阶段，其与另外一个索引quantizer有关，通过quantizer来判断属于哪个cell。  

IndexIVFFlat在搜索的时候，引入了nlist(cell的数量)与nprob(执行搜索的cell树)参数。通过调整这些参数可以在速度与精度之间平衡。  

```
import numpy as np
d = 64                              # 向量维度
nb = 100000                         # 向量集大小
nq = 10000                          # 查询次数
np.random.seed(1234)                # 随机种子,使结果可复现
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.

import faiss

nlist = 100
k = 4
quantizer = faiss.IndexFlatL2(d)  # the other index
index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
# here we specify METRIC_L2, by default it performs inner-product search

assert not index.is_trained
index.train(xb)
assert index.is_trained

index.add(xb)                  # 添加索引可能会有一点慢
D, I = index.search(xq, k)     # 搜索
print(I[-5:])                  # 最初五次查询的结果
index.nprobe = 10              # 默认 nprobe 是1 ,可以设置的大一些试试
D, I = index.search(xq, k)
print(I[-5:])                  # 最后五次查询的结果
```  

最后的结果为  

```
[[ 9900  9309  9810 10048]
 [11055 10895 10812 11321]
 [11353 10164  9787 10719]
 [10571 10664 10632 10203]
 [ 9628  9554  9582 10304]]
[[ 9900 10500  9309  9831]
 [11055 10895 10812 11321]
 [11353 11103 10164  9787]
 [10571 10664 10632  9638]
 [ 9628  9554 10036  9582]]
```  

由上面的实验可以看出，结果并不是完全一致的，增大nprobe可以得到与brute-force更为接近的结果，nprobe就是速度与精度的调节器。  


## 7.IndexIVFPQ
IndexFlatL2 和 IndexIVFFlat都要存储所有的向量数据。对于超大规模数据集来说，可能会不大显示。因此IndexIVFPQ索引可以用来压缩向量，具体的压缩算法为PQ(乘积量化, Product Quantizer)。  

```
import numpy as np

d = 64                              # 向量维度
nb = 100000                         # 向量集大小
nq = 10000                          # 查询次数
np.random.seed(1234)                # 随机种子,使结果可复现
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.

import faiss

nlist = 100
m = 8
k = 4
quantizer = faiss.IndexFlatL2(d)    # 内部的索引方式依然不变
index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)
                                    # 每个向量都被编码为8个字节大小
index.train(xb)
index.add(xb)
D, I = index.search(xb[:5], k)      # 测试
print(I)
print(D)
index.nprobe = 10                   # 与以前的方法相比
D, I = index.search(xq, k)          # 检索
print(I[-5:])

```  

结果为  

```
[[   0   78  608  159]
 [   1 1063  555  380]
 [   2  304  134   46]
 [   3   64  773  265]
 [   4  288  827  531]]
[[1.6157436 6.1152253 6.4348025 6.564184 ]
 [1.389575  5.6771317 5.9956017 6.486294 ]
 [1.7025063 6.121688  6.189084  6.489888 ]
 [1.8057687 6.5440307 6.6684756 6.859398 ]
 [1.4920276 5.79976   6.190908  6.3791513]]
[[ 9900  8746  9853 10437]
 [10494 10507 11373  9014]
 [10719 11291 10424 10138]
 [10122  9638 11113 10630]
 [ 9229 10304  9644 10370]]

```  

IndexIVFPQ能正确找到距离最小的向量(他本身)，但是距离不为0，这是因为向量数据存储时候有压缩，会损失一部分精度。  

另外搜索真实查询时，虽然结果大多是错误的(与刚才的IVFFlat进行比较)，但是它们在正确的空间区域，而对于真实数据，情况更好，因为：  
1.统一数据很难进行索引，因为没有规律性可以被利用来聚集或降低维度  
2.对于自然数据，语义最近邻居往往比不相关的结果更接近。  
(参考文献4)  

## 8.索引选择
如果需要精确的搜索结果，不要降维、不要量化，使用 Flat，同时，使用Flat 意味着数据不会被压缩，将占用同等大小的内存；  
如果内存很紧张，可以使用 PCA 降维、PQ 量化编码，来减少内存占用，最终占用的内存大小约等于 <降维后的向量维度> * <量化后的每个向量的字节数> * <向量个数>； 如果量化编码后的字节数大于64，推荐使用SQx 替换PQx，准确度相同但速度会更快；为了便于量化编码，可以使用 OPQx_y 先对向量做线性变换，y 必须是编码后字节数x的倍数，但最好小于维度dim和4x；  
如果总向量个数 N 小于 1百万，推荐使用 IVFx ，x 的选值介于 4sqrt(N) 和 16*sqrt(N) 之间，训练数据的大小至少要是x的30倍；如果总向量个数 N 大于 1百万、小于 1千万，推荐使用 IMI2x10，实际内部聚类个数是 2 ^ (2 * 10)，将需要64 * 2 ^ 10 个向量参与训练；如果总向量个数 N 大于 1千万、小于 1亿，推荐使用 IMI2x12；如果总向量个数 N 大于 1亿、小于 10亿，推荐使用 IMI2x14；IMI方法不支持GPU；  
IndexIVF 天生支持 add_with_ids 方法，对于不支持 add_with_ids方法的类型，可以使用IndexIDMap 辅助。  
(参考文献5)  


## 参考文献
1.faiss的wiki地址：https://github.com/facebookresearch/faiss/wiki  
2.faiss的index: https://github.com/facebookresearch/faiss/wiki/Faiss-indexes  
3.PQ算法: https://hal.inria.fr/file/index/docid/514462/filename/paper_hal.pdf  
4.https://www.jianshu.com/p/43db601b8af1  
5.https://github.com/vieyahn2017/iBlog/issues/339  