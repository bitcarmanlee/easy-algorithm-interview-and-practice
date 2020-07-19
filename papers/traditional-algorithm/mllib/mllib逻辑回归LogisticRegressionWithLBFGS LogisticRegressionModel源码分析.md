前面一篇文章分析了mllib中的线性回归模型。线性回归一般是用来做拟合使用。实际工作中，分类也是与回归一样常见的需求，甚至可以说比回归分析的需求更大。本文结合mllib的源码，分析在spark中用得最多的一种分类模型：逻辑回归LogisticRegressionWithLBFGS。  


## 1.LogisticRegressionWithLBFGS源码
照惯例，先上源码  

```
/**
 * Train a classification model for Multinomial/Binary Logistic Regression using
 * Limited-memory BFGS. Standard feature scaling and L2 regularization are used by default.
 * NOTE: Labels used in Logistic Regression should be {0, 1, ..., k - 1}
 * for k classes multi-label classification problem.
 */
@Since("1.1.0")
class LogisticRegressionWithLBFGS
  extends GeneralizedLinearAlgorithm[LogisticRegressionModel] with Serializable {

  this.setFeatureScaling(true)

  @Since("1.1.0")
  override val optimizer = new LBFGS(new LogisticGradient, new SquaredL2Updater)

  override protected val validators = List(multiLabelValidator)

  private def multiLabelValidator: RDD[LabeledPoint] => Boolean = { data =>
    if (numOfLinearPredictor > 1) {
      DataValidators.multiLabelValidator(numOfLinearPredictor + 1)(data)
    } else {
      DataValidators.binaryLabelValidator(data)
    }
  }

  /**
   * Set the number of possible outcomes for k classes classification problem in
   * Multinomial Logistic Regression.
   * By default, it is binary logistic regression so k will be set to 2.
   */
  @Since("1.3.0")
  def setNumClasses(numClasses: Int): this.type = {
    require(numClasses > 1)
    numOfLinearPredictor = numClasses - 1
    if (numClasses > 2) {
      optimizer.setGradient(new LogisticGradient(numClasses))
    }
    this
  }

  override protected def createModel(weights: Vector, intercept: Double) = {
    if (numOfLinearPredictor == 1) {
      new LogisticRegressionModel(weights, intercept)
    } else {
      new LogisticRegressionModel(weights, intercept, numFeatures, numOfLinearPredictor + 1)
    }
  }
}
```  

## 2.源码分解
首先可以看到，LogisticRegressionWithLBFGS继承了GeneralizedLinearAlgorithm(GLA)类。所以显然他也是一个线性类的算法。  

另外需要注意的一点是，LogisticRegressionWithLBFGS的package信息是`org.apache.spark.mllib.classification`，大家一定要注意这是个分类算法有木有！  

```
  this.setFeatureScaling(true)

```  

首先一上来，LRWithLBFGS将FeatureScaling开关打开。所以如果直接调用LRWithLBFGS，默认是需要做FeatureScaling的。  

```
  override val optimizer = new LBFGS(new LogisticGradient, new SquaredL2Updater)
```  

这一行代码的信息量就大大的有了。optimizer是一个LBFGS对象，LBFGS位于`org.apache.spark.mllib.optimization`，后面肯定需要再单独说LBFGS。另外，LBFGS的构造函数里又包含两个类：LogisticGradient，SquaredL2Updater。这些东东都是需要单独再拎出来详细理解的。这里先略过不提。  

小结一下就是这行代码new出来一个LBFGS的优化方法用于求解模型参数！  

```
  override protected val validators = List(multiLabelValidator)

  private def multiLabelValidator: RDD[LabeledPoint] => Boolean = { data =>
    if (numOfLinearPredictor > 1) {
      DataValidators.multiLabelValidator(numOfLinearPredictor + 1)(data)
    } else {
      DataValidators.binaryLabelValidator(data)
    }
  }
```  

这一部分代码主要是用来check输入的数据的。具体的细节同学们钻进相应的方法查看即可。  

```
  def setNumClasses(numClasses: Int): this.type = {
    require(numClasses > 1)
    numOfLinearPredictor = numClasses - 1
    if (numClasses > 2) {
      optimizer.setGradient(new LogisticGradient(numClasses))
    }
    this
  }
```  

此部分代码是设置分类的类别数量。默认的是二分类问题！  

```
  override protected def createModel(weights: Vector, intercept: Double) = {
    if (numOfLinearPredictor == 1) {
      new LogisticRegressionModel(weights, intercept)
    } else {
      new LogisticRegressionModel(weights, intercept, numFeatures, numOfLinearPredictor + 1)
    }
  }
```  

最后一部分，则是通过createModel方法，来创建一个LogisticRegressionModel的模型。  

## 3.LogisticRegressionModel源码

二话不说，上源码  

```
class LogisticRegressionModel @Since("1.3.0") (
    @Since("1.0.0") override val weights: Vector,
    @Since("1.0.0") override val intercept: Double,
    @Since("1.3.0") val numFeatures: Int,
    @Since("1.3.0") val numClasses: Int)
  extends GeneralizedLinearModel(weights, intercept) with ClassificationModel with Serializable
  with Saveable with PMMLExportable {

  if (numClasses == 2) {
    require(weights.size == numFeatures,
      s"LogisticRegressionModel with numClasses = 2 was given non-matching values:" +
      s" numFeatures = $numFeatures, but weights.size = ${weights.size}")
  } else {
    val weightsSizeWithoutIntercept = (numClasses - 1) * numFeatures
    val weightsSizeWithIntercept = (numClasses - 1) * (numFeatures + 1)
    require(weights.size == weightsSizeWithoutIntercept || weights.size == weightsSizeWithIntercept,
      s"LogisticRegressionModel.load with numClasses = $numClasses and numFeatures = $numFeatures" +
      s" expected weights of length $weightsSizeWithoutIntercept (without intercept)" +
      s" or $weightsSizeWithIntercept (with intercept)," +
      s" but was given weights of length ${weights.size}")
  }

  private val dataWithBiasSize: Int = weights.size / (numClasses - 1)

  private val weightsArray: Array[Double] = weights match {
    case dv: DenseVector => dv.values
    case _ =>
      throw new IllegalArgumentException(
        s"weights only supports dense vector but got type ${weights.getClass}.")
  }

  /**
   * Constructs a [[LogisticRegressionModel]] with weights and intercept for binary classification.
   */
  @Since("1.0.0")
  def this(weights: Vector, intercept: Double) = this(weights, intercept, weights.size, 2)

  private var threshold: Option[Double] = Some(0.5)

  /**
   * Sets the threshold that separates positive predictions from negative predictions
   * in Binary Logistic Regression. An example with prediction score greater than or equal to
   * this threshold is identified as an positive, and negative otherwise. The default value is 0.5.
   * It is only used for binary classification.
   */
  @Since("1.0.0")
  def setThreshold(threshold: Double): this.type = {
    this.threshold = Some(threshold)
    this
  }

  /**
   * Returns the threshold (if any) used for converting raw prediction scores into 0/1 predictions.
   * It is only used for binary classification.
   */
  @Since("1.3.0")
  def getThreshold: Option[Double] = threshold

  /**
   * Clears the threshold so that `predict` will output raw prediction scores.
   * It is only used for binary classification.
   */
  @Since("1.0.0")
  def clearThreshold(): this.type = {
    threshold = None
    this
  }

  override protected def predictPoint(
      dataMatrix: Vector,
      weightMatrix: Vector,
      intercept: Double) = {
    require(dataMatrix.size == numFeatures)

    // If dataMatrix and weightMatrix have the same dimension, it's binary logistic regression.
    if (numClasses == 2) {
      val margin = dot(weightMatrix, dataMatrix) + intercept
      val score = 1.0 / (1.0 + math.exp(-margin))
      threshold match {
        case Some(t) => if (score > t) 1.0 else 0.0
        case None => score
      }
    } else {
      /**
       * Compute and find the one with maximum margins. If the maxMargin is negative, then the
       * prediction result will be the first class.
       *
       * PS, if you want to compute the probabilities for each outcome instead of the outcome
       * with maximum probability, remember to subtract the maxMargin from margins if maxMargin
       * is positive to prevent overflow.
       */
      var bestClass = 0
      var maxMargin = 0.0
      val withBias = dataMatrix.size + 1 == dataWithBiasSize
      (0 until numClasses - 1).foreach { i =>
        var margin = 0.0
        dataMatrix.foreachActive { (index, value) =>
          if (value != 0.0) margin += value * weightsArray((i * dataWithBiasSize) + index)
        }
        // Intercept is required to be added into margin.
        if (withBias) {
          margin += weightsArray((i * dataWithBiasSize) + dataMatrix.size)
        }
        if (margin > maxMargin) {
          maxMargin = margin
          bestClass = i + 1
        }
      }
      bestClass.toDouble
    }
  }

  @Since("1.3.0")
  override def save(sc: SparkContext, path: String): Unit = {
    GLMClassificationModel.SaveLoadV1_0.save(sc, path, this.getClass.getName,
      numFeatures, numClasses, weights, intercept, threshold)
  }

  override protected def formatVersion: String = "1.0"

  override def toString: String = {
    s"${super.toString}, numClasses = ${numClasses}, threshold = ${threshold.getOrElse("None")}"
  }
}

@Since("1.3.0")
object LogisticRegressionModel extends Loader[LogisticRegressionModel] {

  @Since("1.3.0")
  override def load(sc: SparkContext, path: String): LogisticRegressionModel = {
    val (loadedClassName, version, metadata) = Loader.loadMetadata(sc, path)
    // Hard-code class name string in case it changes in the future
    val classNameV1_0 = "org.apache.spark.mllib.classification.LogisticRegressionModel"
    (loadedClassName, version) match {
      case (className, "1.0") if className == classNameV1_0 =>
        val (numFeatures, numClasses) = ClassificationModel.getNumFeaturesClasses(metadata)
        val data = GLMClassificationModel.SaveLoadV1_0.loadData(sc, path, classNameV1_0)
        // numFeatures, numClasses, weights are checked in model initialization
        val model =
          new LogisticRegressionModel(data.weights, data.intercept, numFeatures, numClasses)
        data.threshold match {
          case Some(t) => model.setThreshold(t)
          case None => model.clearThreshold()
        }
        model
      case _ => throw new Exception(
        s"LogisticRegressionModel.load did not recognize model with (className, format version):" +
        s"($loadedClassName, $version).  Supported:\n" +
        s"  ($classNameV1_0, 1.0)")
    }
  }
}
```  

首先，LogisticRegressionModel自然也继承了GeneralizedLinearModel。同时，他还实现了ClassificationModel！  

```
class LogisticRegressionModel @Since("1.3.0") (
    @Since("1.0.0") override val weights: Vector,
    @Since("1.0.0") override val intercept: Double,
    @Since("1.3.0") val numFeatures: Int,
    @Since("1.3.0") val numClasses: Int)
```  

主构造方法中，有四个参数：weights为特征权重，intercept为截距权重，numFeatures为特征数量，numClasses为类别数量。  

```
  def this(weights: Vector, intercept: Double) = this(weights, intercept, weights.size, 2)
```  

辅助方法告诉我们，默认的model为二分类模型。  

```
  private var threshold: Option[Double] = Some(0.5)

```  

分类阈值，默认0.5。  
重点看看predictPoint方法里的代码：  

```
    if (numClasses == 2) {
      val margin = dot(weightMatrix, dataMatrix) + intercept
      val score = 1.0 / (1.0 + math.exp(-margin))
      threshold match {
        case Some(t) => if (score > t) 1.0 else 0.0
        case None => score
      }
    }
```  

针对咱们最常用的二分类的情况，这段代码就表示了最终的预测结果：使用logistic函数计算一个score。如果score大于threshold ,类别则为1；否则为0！  

代码中还包含有save方法，自然就是将模型的结果保存下来了！  