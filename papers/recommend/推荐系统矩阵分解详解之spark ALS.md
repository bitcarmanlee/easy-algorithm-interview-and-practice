## 1.推荐系统与spark
做推荐系统的同学，一般都会用到spark。spark的用途相当广泛，可以用来做效果数据分析，更是构建特征与离线训练集的不二人选，同时spark streaming也是做实时数据的常用解决方案，mllib包与ml包里面也实现了很多常用的算法，是针对大数据集分布式算法最常用的算法框架。因此能熟练掌握spark的使用算是做推荐系统的基本功。  

## 2.ALS算法
spark mllib/ml中，recommendation包里只有一个算法:ALS，估计做过推荐系统相关的同学，都会或多或少用过ALS，下面我们来对ALS做个总结。  

[推荐系统中的矩阵分解详解](https://blog.csdn.net/bitcarmanlee/article/details/106108002)
一文中，提到我们最终的目标是将原始的user-item评分矩阵分解为两个低秩矩阵，损失函数为
$$\min \limits_{q^\*,p^\*} \sum \limits_{(u, i)} (r_{ui} - q_i^Tp_u) ^ 2$$  

有了损失函数以后，就是确定优化算法来求解了。  
大规模数据集中，常用的优化算法一般是两种：梯度下降(gradient descent)系列与交叉最小二乘法（alternative least squares，ALS）。梯度下降我们已经比较熟悉了，那么ALS是什么呢？或者说，ALS与普通的最小二乘有什么区别？  

上面的损失函数与一般损失函数区别就在于其有不止一个变量，包含一个物品向量$q_i$与用户向量$p_u$，所以ALS的优化方式总结起来为:  
固定$q_i$求$p_{u+1}$，再固定$p_{u+1}$求$q_{i+1}$。  

ALS相比GD系列算法，主要有以下两个优点：  
1.$q_i$与$p_u$的计算是独立的，因此计算的时候可以并行提高计算速度。  
2.在一般的推荐场景中，user-item的组合非常多，比如千万级别的用户与十万甚至百万级别的item很常见。对于这种场景，用GD或者SGD去挨个迭代是非常慢的。当然我们也可以用负采样等方法，但是整体也不会太快。而ALS可以用一些矩阵的技巧来解决计算低效的问题。  

ALS的每步迭代都会降低误差，并且误差有下界，所以 ALS 一定会收敛。但由于问题是非凸的，ALS 并不保证会收敛到全局最优解。但在实际应用中，ALS 对初始点不是很敏感，是否全局最优解造成的影响并不大。(参考文献1)  

## 3.spark中的ALS
下面我们来看看spark中的ALS。mllib与ml包中均有ALS实现，API会有一些差异，但是基本的思想是一致的，我们就以mllib中的ALS为例分析一下，spark版本2.3。  
首先看一下Rating类  

```
/**
 * A more compact class to represent a rating than Tuple3[Int, Int, Double].
 */
@Since("0.8.0")
case class Rating @Since("0.8.0") (
    @Since("0.8.0") user: Int,
    @Since("0.8.0") product: Int,
    @Since("0.8.0") rating: Double)
```

这个类就是我们输入的训练集，总共散列：user, prodcut(item)，rating。分别表示用户，物品，分数。

然后是ALS类

```
/**
 * Alternating Least Squares matrix factorization.
 *
 * ALS attempts to estimate the ratings matrix `R` as the product of two lower-rank matrices,
 * `X` and `Y`, i.e. `X * Yt = R`. Typically these approximations are called 'factor' matrices.
 * The general approach is iterative. During each iteration, one of the factor matrices is held
 * constant, while the other is solved for using least squares. The newly-solved factor matrix is
 * then held constant while solving for the other factor matrix.
 *
 * This is a blocked implementation of the ALS factorization algorithm that groups the two sets
 * of factors (referred to as "users" and "products") into blocks and reduces communication by only
 * sending one copy of each user vector to each product block on each iteration, and only for the
 * product blocks that need that user's feature vector. This is achieved by precomputing some
 * information about the ratings matrix to determine the "out-links" of each user (which blocks of
 * products it will contribute to) and "in-link" information for each product (which of the feature
 * vectors it receives from each user block it will depend on). This allows us to send only an
 * array of feature vectors between each user block and product block, and have the product block
 * find the users' ratings and update the products based on these messages.
 *
 * For implicit preference data, the algorithm used is based on
 * "Collaborative Filtering for Implicit Feedback Datasets", available at
 * <a href="http://dx.doi.org/10.1109/ICDM.2008.22">here</a>, adapted for the blocked approach
 * used here.
 *
 * Essentially instead of finding the low-rank approximations to the rating matrix `R`,
 * this finds the approximations for a preference matrix `P` where the elements of `P` are 1 if
 * r &gt; 0 and 0 if r &lt;= 0. The ratings then act as 'confidence' values related to strength of
 * indicated user
 * preferences rather than explicit ratings given to items.
 */
@Since("0.8.0")
class ALS private (
    private var numUserBlocks: Int,
    private var numProductBlocks: Int,
    private var rank: Int,
    private var iterations: Int,
    private var lambda: Double,
    private var implicitPrefs: Boolean,
    private var alpha: Double,
    private var seed: Long = System.nanoTime()
  ) extends Serializable with Logging {
...
```  

一般看知名开源项目的时候，注释都是非常好非常重要的信息，看懂了注释对我们理解代码有非常大的好处。  
```
ALS attempts to estimate the ratings matrix R as the product of two lower-rank matrices, 
X and Y, i.e. X * Yt = R. 
Typically these approximations are called 'factor' matrices.

The general approach is iterative. During each iteration, 
one of the factor matrices is held constant, 
while the other is solved for using least squares.
The newly-solved factor matrix is then held constant while solving for the other factor matrix.
```  

这段注释就简明扼要地介绍了ALS的精髓。  
1.ALS是将评分矩阵R分解为两个低秩矩阵X,Y，有$X * Y^T = R$  
2.这些低秩矩阵的近似被称为因子(factor)。  
3.基本的实现方式是迭代。在每轮迭代时，先固定一个因子为常量，然后对另外一个因子用最小二乘求解。然后这个新求得的解固定，作为常量固定用来求解另外一个因子。  

是不是看完以后就基本知道了ALS的思路？注释是不是非常精彩？  
注释的中间一大段是讲spark计算的时候并行优化的问题，本文暂时先不讨论。  

```
For implicit preference data, the algorithm used is based on
 "Collaborative Filtering for Implicit Feedback Datasets", available at
 <a href="http://dx.doi.org/10.1109/ICDM.2008.22">here</a>, 
 adapted for the blocked approach  used here.
 
Essentially instead of finding the low-rank approximations to the rating matrix `R`,
this finds the approximations for a preference matrix `P` 
where the elements of `P` are 1 if
 r &gt; 0 and 0 if r &lt;= 0.
 The ratings then act as 'confidence' values related to strength of
indicated user
 preferences rather than explicit ratings given to items.
```  
这段注释也非常精彩非常重要，主要是提到了隐式反馈的问题。  

[推荐系统中的矩阵分解详解](https://blog.csdn.net/bitcarmanlee/article/details/106108002)  
文中，已经详细解释了隐式反馈，这里就不再多做描述，可以去仔细查看关于隐式反馈的部分。  

看完了注释，再看ALS的构造方法就很清楚了  

```
class ALS private (
    private var numUserBlocks: Int,
    private var numProductBlocks: Int,
    private var rank: Int,
    private var iterations: Int,
    private var lambda: Double,
    private var implicitPrefs: Boolean,
    private var alpha: Double,
    private var seed: Long = System.nanoTime()
  ) extends Serializable with Logging {
...  


```  
numUserBlocks, numProductBlocks都是spark并行计算的参数，rank是我们想得到的隐向量维度，iteration为算法迭代次数，lambda为正则参数，implicitPrefs表示是否为隐式数据集，alpha为隐式计算中，$c_{ui} = 1 + \alpha d_{ui}$中的超参数。  

```
  /**
   * Constructs an ALS instance with default parameters: {numBlocks: -1, rank: 10, iterations: 10,
   * lambda: 0.01, implicitPrefs: false, alpha: 1.0}.
   */
  @Since("0.8.0")
  def this() = this(-1, -1, 10, 10, 0.01, false, 1.0)
```  
可以看出，ALS给的默认参数中，rank为10，iteration为10，lambda为0.01，隐式反馈默认为fasle，$\alpha$为1.0。  

## 4.具体训练过程
mllib中的ALS类主要是有train与trainImplicit方法，两者的区别从名字就可以看出来，一个是显示数据集，另外一个是隐式数据集，具体的原理大致相同，以train方法为例，我们来分析一下具体过程。  

```
@Since("0.8.0")
object ALS {
  /**
   * Train a matrix factorization model given an RDD of ratings by users for a subset of products.
   * The ratings matrix is approximated as the product of two lower-rank matrices of a given rank
   * (number of features). To solve for these features, ALS is run iteratively with a configurable
   * level of parallelism.
   *
   * @param ratings    RDD of [[Rating]] objects with userID, productID, and rating
   * @param rank       number of features to use (also referred to as the number of latent factors)
   * @param iterations number of iterations of ALS
   * @param lambda     regularization parameter
   * @param blocks     level of parallelism to split computation into
   * @param seed       random seed for initial matrix factorization model
   */
  @Since("0.9.1")
  def train(
      ratings: RDD[Rating],
      rank: Int,
      iterations: Int,
      lambda: Double,
      blocks: Int,
      seed: Long
    ): MatrixFactorizationModel = {
    new ALS(blocks, blocks, rank, iterations, lambda, false, 1.0, seed).run(ratings)
  }
```  

返回的是一个MatrixFactorizationModel对象。MatrixFactorizationModel的具体分析后面再讲。  

再跟踪到run方法中，找到关键的信息：  

```
  /**
   * Run ALS with the configured parameters on an input RDD of [[Rating]] objects.
   * Returns a MatrixFactorizationModel with feature vectors for each user and product.
   */
  @Since("0.8.0")
  def run(ratings: RDD[Rating]): MatrixFactorizationModel = {
    require(!ratings.isEmpty(), s"No ratings available from $ratings")

    val sc = ratings.context

    val numUserBlocks = if (this.numUserBlocks == -1) {
      math.max(sc.defaultParallelism, ratings.partitions.length / 2)
    } else {
      this.numUserBlocks
    }
    val numProductBlocks = if (this.numProductBlocks == -1) {
      math.max(sc.defaultParallelism, ratings.partitions.length / 2)
    } else {
      this.numProductBlocks
    }

    val (floatUserFactors, floatProdFactors) = NewALS.train[Int](
      ratings = ratings.map(r => NewALS.Rating(r.user, r.product, r.rating.toFloat)),
      rank = rank,
      numUserBlocks = numUserBlocks,
      numItemBlocks = numProductBlocks,
      maxIter = iterations,
      regParam = lambda,
      implicitPrefs = implicitPrefs,
      alpha = alpha,
      nonnegative = nonnegative,
      intermediateRDDStorageLevel = intermediateRDDStorageLevel,
      finalRDDStorageLevel = StorageLevel.NONE,
      checkpointInterval = checkpointInterval,
      seed = seed)
      ...
```  

具体的训练过程是在NewALS.train实现的，这也跟目前spark发展的趋势吻合，API向ML包靠拢，mllib包里的代码逐渐废弃。  

点进train方法，看看里面的具体实现。  

```
  def train[ID: ClassTag]( // scalastyle:ignore
      ratings: RDD[Rating[ID]],
      rank: Int = 10,
      numUserBlocks: Int = 10,
      numItemBlocks: Int = 10,
      maxIter: Int = 10,
      regParam: Double = 0.1,
      implicitPrefs: Boolean = false,
      alpha: Double = 1.0,
      nonnegative: Boolean = false,
      intermediateRDDStorageLevel: StorageLevel = StorageLevel.MEMORY_AND_DISK,
      finalRDDStorageLevel: StorageLevel = StorageLevel.MEMORY_AND_DISK,
      checkpointInterval: Int = 10,
      seed: Long = 0L)(
      implicit ord: Ordering[ID]): (RDD[(ID, Array[Float])], RDD[(ID, Array[Float])]) = {

    require(!ratings.isEmpty(), s"No ratings available from $ratings")
    require(intermediateRDDStorageLevel != StorageLevel.NONE,
      "ALS is not designed to run without persisting intermediate RDDs.")

    val sc = ratings.sparkContext

    // Precompute the rating dependencies of each partition
    val userPart = new ALSPartitioner(numUserBlocks)
    val itemPart = new ALSPartitioner(numItemBlocks)
    val blockRatings = partitionRatings(ratings, userPart, itemPart)
      .persist(intermediateRDDStorageLevel)
    val (userInBlocks, userOutBlocks) =
      makeBlocks("user", blockRatings, userPart, itemPart, intermediateRDDStorageLevel)
    userOutBlocks.count()    // materialize blockRatings and user blocks
    val swappedBlockRatings = blockRatings.map {
      case ((userBlockId, itemBlockId), RatingBlock(userIds, itemIds, localRatings)) =>
        ((itemBlockId, userBlockId), RatingBlock(itemIds, userIds, localRatings))
    }
    val (itemInBlocks, itemOutBlocks) =
      makeBlocks("item", swappedBlockRatings, itemPart, userPart, intermediateRDDStorageLevel)
    itemOutBlocks.count()    // materialize item blocks

    // Encoders for storing each user/item's partition ID and index within its partition using a
    // single integer; used as an optimization
    val userLocalIndexEncoder = new LocalIndexEncoder(userPart.numPartitions)
    val itemLocalIndexEncoder = new LocalIndexEncoder(itemPart.numPartitions)

    // These are the user and item factor matrices that, once trained, are multiplied together to
    // estimate the rating matrix.  The two matrices are stored in RDDs, partitioned by column such
    // that each factor column resides on the same Spark worker as its corresponding user or item.
    val seedGen = new XORShiftRandom(seed)
    var userFactors = initialize(userInBlocks, rank, seedGen.nextLong())
    var itemFactors = initialize(itemInBlocks, rank, seedGen.nextLong())

    val solver = if (nonnegative) new NNLSSolver else new CholeskySolver

    var previousCheckpointFile: Option[String] = None
    val shouldCheckpoint: Int => Boolean = (iter) =>
      sc.checkpointDir.isDefined && checkpointInterval != -1 && (iter % checkpointInterval == 0)
    val deletePreviousCheckpointFile: () => Unit = () =>
      previousCheckpointFile.foreach { file =>
        try {
          val checkpointFile = new Path(file)
          checkpointFile.getFileSystem(sc.hadoopConfiguration).delete(checkpointFile, true)
        } catch {
          case e: IOException =>
            logWarning(s"Cannot delete checkpoint file $file:", e)
        }
      }

    if (implicitPrefs) {
      for (iter <- 1 to maxIter) {
        userFactors.setName(s"userFactors-$iter").persist(intermediateRDDStorageLevel)
        val previousItemFactors = itemFactors
        itemFactors = computeFactors(userFactors, userOutBlocks, itemInBlocks, rank, regParam,
          userLocalIndexEncoder, implicitPrefs, alpha, solver)
        previousItemFactors.unpersist()
        itemFactors.setName(s"itemFactors-$iter").persist(intermediateRDDStorageLevel)
        // TODO: Generalize PeriodicGraphCheckpointer and use it here.
        val deps = itemFactors.dependencies
        if (shouldCheckpoint(iter)) {
          itemFactors.checkpoint() // itemFactors gets materialized in computeFactors
        }
        val previousUserFactors = userFactors
        userFactors = computeFactors(itemFactors, itemOutBlocks, userInBlocks, rank, regParam,
          itemLocalIndexEncoder, implicitPrefs, alpha, solver)
        if (shouldCheckpoint(iter)) {
          ALS.cleanShuffleDependencies(sc, deps)
          deletePreviousCheckpointFile()
          previousCheckpointFile = itemFactors.getCheckpointFile
        }
        previousUserFactors.unpersist()
      }
    } else {
      for (iter <- 0 until maxIter) {
        itemFactors = computeFactors(userFactors, userOutBlocks, itemInBlocks, rank, regParam,
          userLocalIndexEncoder, solver = solver)
        if (shouldCheckpoint(iter)) {
          val deps = itemFactors.dependencies
          itemFactors.checkpoint()
          itemFactors.count() // checkpoint item factors and cut lineage
          ALS.cleanShuffleDependencies(sc, deps)
          deletePreviousCheckpointFile()
          previousCheckpointFile = itemFactors.getCheckpointFile
        }
        userFactors = computeFactors(itemFactors, itemOutBlocks, userInBlocks, rank, regParam,
          itemLocalIndexEncoder, solver = solver)
      }
    }
    val userIdAndFactors = userInBlocks
      .mapValues(_.srcIds)
      .join(userFactors)
      .mapPartitions({ items =>
        items.flatMap { case (_, (ids, factors)) =>
          ids.view.zip(factors)
        }
      // Preserve the partitioning because IDs are consistent with the partitioners in userInBlocks
      // and userFactors.
      }, preservesPartitioning = true)
      .setName("userFactors")
      .persist(finalRDDStorageLevel)
    val itemIdAndFactors = itemInBlocks
      .mapValues(_.srcIds)
      .join(itemFactors)
      .mapPartitions({ items =>
        items.flatMap { case (_, (ids, factors)) =>
          ids.view.zip(factors)
        }
      }, preservesPartitioning = true)
      .setName("itemFactors")
      .persist(finalRDDStorageLevel)
    if (finalRDDStorageLevel != StorageLevel.NONE) {
      userIdAndFactors.count()
      itemFactors.unpersist()
      itemIdAndFactors.count()
      userInBlocks.unpersist()
      userOutBlocks.unpersist()
      itemInBlocks.unpersist()
      itemOutBlocks.unpersist()
      blockRatings.unpersist()
    }
    (userIdAndFactors, itemIdAndFactors)
  }

```  


train里面的参数，有如下几个比较重要的：  
rating:输入的训练集  
rank: 隐向量维度，默认为10  
numUserBlocks: user的blocks，用于并行计算，默认为10。  
numItemBlocks: Int = 10, item的blocks，用于并行计算，默认为10。  
maxIter: Int = 10  
regParam: Double = 0.1  
implicitPrefs: Boolean = false 隐式反馈数据集，默认为false  
alpha: Double = 1.0  
nonnegative: Boolean = false 具体求解方法，默认为CholeskySolver(乔里斯基分解)，如果为true为非负矩阵分解。  

```
    // Precompute the rating dependencies of each partition
    val userPart = new ALSPartitioner(numUserBlocks)
    val itemPart = new ALSPartitioner(numItemBlocks)
```  
将user,item按ALSPartitioner进行划分。  
而ALSPartitioner就是HashPartitioner。  

```
  /**
   * Partitioner used by ALS. We require that getPartition is a projection. That is, for any key k,
   * we have getPartition(getPartition(k)) = getPartition(k). Since the default HashPartitioner
   * satisfies this requirement, we simply use a type alias here.
   */
  private[recommendation] type ALSPartitioner = org.apache.spark.HashPartitioner
```  

```
    // Encoders for storing each user/item's partition ID and index within its partition using a
    // single integer; used as an optimization
    val userLocalIndexEncoder = new LocalIndexEncoder(userPart.numPartitions)
    val itemLocalIndexEncoder = new LocalIndexEncoder(itemPart.numPartitions)
```  

这两行，是将user特征与item特征编码变成整数。  

```
    val solver = if (nonnegative) new NNLSSolver else new CholeskySolver
```  

确定求解方法。如果nonnegative参数为true，使用非负矩阵分解，否则使用乔里斯基分解。  


```
    if (implicitPrefs) {
    if (implicitPrefs) {
      for (iter <- 1 to maxIter) {
        userFactors.setName(s"userFactors-$iter").persist(intermediateRDDStorageLevel)
        val previousItemFactors = itemFactors
        itemFactors = computeFactors(userFactors, userOutBlocks, itemInBlocks, rank, regParam,
          userLocalIndexEncoder, implicitPrefs, alpha, solver)
        previousItemFactors.unpersist()
        itemFactors.setName(s"itemFactors-$iter").persist(intermediateRDDStorageLevel)
        // TODO: Generalize PeriodicGraphCheckpointer and use it here.
        val deps = itemFactors.dependencies
        if (shouldCheckpoint(iter)) {
          itemFactors.checkpoint() // itemFactors gets materialized in computeFactors
        }
        val previousUserFactors = userFactors
        userFactors = computeFactors(itemFactors, itemOutBlocks, userInBlocks, rank, regParam,
          itemLocalIndexEncoder, implicitPrefs, alpha, solver)
          ...
```  

上面就涉及到计算itemFactors与userFactors的核心逻辑，computeFactors方法我们再点进去观察一下  

```
  private def computeFactors[ID](
      srcFactorBlocks: RDD[(Int, FactorBlock)],
      srcOutBlocks: RDD[(Int, OutBlock)],
      dstInBlocks: RDD[(Int, InBlock[ID])],
      rank: Int,
      regParam: Double,
      srcEncoder: LocalIndexEncoder,
      implicitPrefs: Boolean = false,
      alpha: Double = 1.0,
      solver: LeastSquaresNESolver)
```  

solver具体的求解在这个位置  

```
...
          // Weight lambda by the number of explicit ratings based on the ALS-WR paper.
          dstFactors(j) = solver.solve(ls, numExplicits * regParam)
          j += 1
        }
        dstFactors
```  

再进到solve方法中  

```
  /** Trait for least squares solvers applied to the normal equation. */
  private[recommendation] trait LeastSquaresNESolver extends Serializable {
    /** Solves a least squares problem with regularization (possibly with other constraints). */
    def solve(ne: NormalEquation, lambda: Double): Array[Float]
  }

  /** Cholesky solver for least square problems. */
  private[recommendation] class CholeskySolver extends LeastSquaresNESolver {

    /**
     * Solves a least squares problem with L2 regularization:
     *
     *   min norm(A x - b)^2^ + lambda * norm(x)^2^
     *
     * @param ne a [[NormalEquation]] instance that contains AtA, Atb, and n (number of instances)
     * @param lambda regularization constant
     * @return the solution x
     */
    override def solve(ne: NormalEquation, lambda: Double): Array[Float] = {
      val k = ne.k
      // Add scaled lambda to the diagonals of AtA.
      var i = 0
      var j = 2
      while (i < ne.triK) {
        ne.ata(i) += lambda
        i += j
        j += 1
      }
      CholeskyDecomposition.solve(ne.ata, ne.atb)
      val x = new Array[Float](k)
      i = 0
      while (i < k) {
        x(i) = ne.atb(i).toFloat
        i += 1
      }
      ne.reset()
      x
    }
  }

  /** NNLS solver. */
  private[recommendation] class NNLSSolver extends LeastSquaresNESolver {
    private var rank: Int = -1
    private var workspace: NNLS.Workspace = _
    private var ata: Array[Double] = _
    private var initialized: Boolean = false

    private def initialize(rank: Int): Unit = {
      if (!initialized) {
        this.rank = rank
        workspace = NNLS.createWorkspace(rank)
        ata = new Array[Double](rank * rank)
        initialized = true
      } else {
        require(this.rank == rank)
      }
    }

    /**
     * Solves a nonnegative least squares problem with L2 regularization:
     *
     *   min_x_  norm(A x - b)^2^ + lambda * n * norm(x)^2^
     *   subject to x >= 0
     */
    override def solve(ne: NormalEquation, lambda: Double): Array[Float] = {
      val rank = ne.k
      initialize(rank)
      fillAtA(ne.ata, lambda)
      val x = NNLS.solve(ata, ne.atb, workspace)
      ne.reset()
      x.map(x => x.toFloat)
    }
```  

这里面就包括CholeskySolver与NNLSSolver。  

以CholeskySolver为例，里面有一行  

```
CholeskyDecomposition.solve(ne.ata, ne.atb)
```  

而CholeskyDecomposition在org.apache.spark.mllib.linalg包中  

```
package org.apache.spark.mllib.linalg

import com.github.fommil.netlib.LAPACK.{getInstance => lapack}
import org.netlib.util.intW

import org.apache.spark.ml.optim.SingularMatrixException

/**
 * Compute Cholesky decomposition.
 */
private[spark] object CholeskyDecomposition {

  /**
   * Solves a symmetric positive definite linear system via Cholesky factorization.
   * The input arguments are modified in-place to store the factorization and the solution.
   * @param A the upper triangular part of A
   * @param bx right-hand side
   * @return the solution array
   */
  def solve(A: Array[Double], bx: Array[Double]): Array[Double] = {
    val k = bx.length
    val info = new intW(0)
    lapack.dppsv("U", k, 1, A, bx, k, info)
    checkReturnValue(info, "dppsv")
    bx
  }
```  

最终真正求解就落在了这一行

```
lapack.dppsv("U", k, 1, A, bx, k, info)
```  

具体的底层矩阵运算过程，就不在本文的讨论范围。至此，spark中的ALS求解，就已经带大家完整分析了一遍。  


## 5.MatrixFactorizationModel
从第四部分可以知道，训练得到的最终结果是MatrixFactorizationModel类。  

```
/**
 * Model representing the result of matrix factorization.
 *
 * @param rank Rank for the features in this model.
 * @param userFeatures RDD of tuples where each tuple represents the userId and
 *                     the features computed for this user.
 * @param productFeatures RDD of tuples where each tuple represents the productId
 *                        and the features computed for this product.
 *
 * @note If you create the model directly using constructor, please be aware that fast prediction
 * requires cached user/product features and their associated partitioners.
 */
@Since("0.8.0")
class MatrixFactorizationModel @Since("0.8.0") (
    @Since("0.8.0") val rank: Int,
    @Since("0.8.0") val userFeatures: RDD[(Int, Array[Double])],
    @Since("0.8.0") val productFeatures: RDD[(Int, Array[Double])])
  extends Saveable with Serializable with Logging
```  

同样先关注一下注释部分的内容：  
1.这个模型代表了矩阵分解的最终结果  
2.参数包括：  
rank: 隐向量的维度。  
userFeatures:RDD数组，其中的元素由userid与对应的隐向量组成。  
productFeatures: RDD数组，其中的元素由itemid与对应的隐向量组成。  

里面主要的API包括两部分：predict与recommendUsersForProducts/recommendProductsForUsers  

```
  /** Predict the rating of one user for one product. */
  @Since("0.8.0")
  def predict(user: Int, product: Int): Double = {
    val userVector = userFeatures.lookup(user).head
    val productVector = productFeatures.lookup(product).head
    blas.ddot(rank, userVector, 1, productVector, 1)
  }
```  
由注释很容易看出，该方法是预测一个user对item的分数。  

```
  /**
   * Recommends top products for all users.
   *
   * @param num how many products to return for every user.
   * @return [(Int, Array[Rating])] objects, where every tuple contains a userID and an array of
   * rating objects which contains the same userId, recommended productID and a "score" in the
   * rating field. Semantics of score is same as recommendProducts API
   */
  @Since("1.4.0")
  def recommendProductsForUsers(num: Int): RDD[(Int, Array[Rating])] = {
    MatrixFactorizationModel.recommendForAll(rank, userFeatures, productFeatures, num).map {
      case (user, top) =>
        val ratings = top.map { case (product, rating) => Rating(user, product, rating) }
        (user, ratings)
    }
  }
```  
上面的方法则是向用户推荐topN的item，实际中该API的使用概率最高，也是我们最终希望达到的目的。  

## 6.movielens推荐实例

```
import org.apache.spark.SparkConf
import org.apache.spark.ml.evaluation.RegressionEvaluator
import org.apache.spark.ml.recommendation.ALS
import org.apache.spark.sql.SparkSession

/**
  * Created by wanglei on 2020/5/18.
  */
object AlsDemo {


    case class Rating(userId: Int, movieId: Int, rating: Float, timestamp: Long)

    def parseRating(str: String) = {
        val fields = str.split("\t")
        assert(fields.size == 4)
        Rating(fields(0).toInt, fields(1).toInt, fields(2).toFloat, fields(3).toLong)
    }

    def main(args: Array[String]): Unit = {
        val sparkConf = new SparkConf().setMaster("local[2]")
        sparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

        val spark = SparkSession.builder().config(sparkConf).getOrCreate()
        import spark.implicits._

        val ratings = spark.read.textFile("file:///xxx/ml-100k/ua.base")
            .map(parseRating)
            .toDF()
        println(ratings.take(3))

        val Array(training, test) = ratings.randomSplit(Array(0.8, 0.2))

        val als = new ALS()
            .setMaxIter(5)
            .setRegParam(0.01)
            .setUserCol("userId")
            .setItemCol("movieId")
            .setRatingCol("rating")

        val model = als.fit(training)

        // Evaluate the model by computing the RMSE on the test data
        model.setColdStartStrategy("drop")
        val predictions = model.transform(test)

        val evaluator = new RegressionEvaluator()
            .setMetricName("rmse")
            .setLabelCol("rating")
            .setPredictionCol("prediction")

        val rmse = evaluator.evaluate(predictions)
        println(s"Root-mean-square error = $rmse")

        val userRecs = model.recommendForAllUsers(10)
        val movieRecs = model.recommendForAllItems(10)

        val users = ratings.select(als.getUserCol).distinct().limit(3)
        val userSubsetRecs = model.recommendForUserSubset(users, 10)
        println("userSubsetRecs is: ")
        userSubsetRecs.show()
        println("-------------\n")

        val movies = ratings.select(als.getItemCol).distinct().limit(3)
        val movieSubSetRecs = model.recommendForItemSubset(movies, 10)
        println("movieSubSetRecs is: ")
        movieSubSetRecs.show()

    }

}
```  

上面代码就可以根据用户推荐排名靠前的电影，也可以根据电影选出得分最高的用户。


## 参考文献
1.https://blog.csdn.net/u011239443/article/details/51752904
