线性回归与线性分类在实际工作中使用的频率非常高，mllib中对这两大类算法自然也有完整实现。现在我们就结合相关源码来对着两大类算法进行分析。本文先分析线性回归。  


二话不说，先上源码。看优秀项目的源码本身就是一种巨大的享受。为了控制篇幅，将一些注释以及import内容先行省略。  


## 1.GeneralizedLinearAlgorithm类源码
```
/**
 * :: DeveloperApi ::
 * GeneralizedLinearAlgorithm implements methods to train a Generalized Linear Model (GLM).
 * This class should be extended with an Optimizer to create a new GLM.
 *
 */
@Since("0.8.0")
@DeveloperApi
abstract class GeneralizedLinearAlgorithm[M <: GeneralizedLinearModel]
  extends Logging with Serializable {

  protected val validators: Seq[RDD[LabeledPoint] => Boolean] = List()

  /**
   * The optimizer to solve the problem.
   *
   */
  @Since("0.8.0")
  def optimizer: Optimizer

  /** Whether to add intercept (default: false). */
  protected var addIntercept: Boolean = false

  protected var validateData: Boolean = true

  /**
   * In `GeneralizedLinearModel`, only single linear predictor is allowed for both weights
   * and intercept. However, for multinomial logistic regression, with K possible outcomes,
   * we are training K-1 independent binary logistic regression models which requires K-1 sets
   * of linear predictor.
   *
   * As a result, the workaround here is if more than two sets of linear predictors are needed,
   * we construct bigger `weights` vector which can hold both weights and intercepts.
   * If the intercepts are added, the dimension of `weights` will be
   * (numOfLinearPredictor) * (numFeatures + 1) . If the intercepts are not added,
   * the dimension of `weights` will be (numOfLinearPredictor) * numFeatures.
   *
   * Thus, the intercepts will be encapsulated into weights, and we leave the value of intercept
   * in GeneralizedLinearModel as zero.
   */
  protected var numOfLinearPredictor: Int = 1

  /**
   * Whether to perform feature scaling before model training to reduce the condition numbers
   * which can significantly help the optimizer converging faster. The scaling correction will be
   * translated back to resulting model weights, so it's transparent to users.
   * Note: This technique is used in both libsvm and glmnet packages. Default false.
   */
  private var useFeatureScaling = false

  /**
   * The dimension of training features.
   *
   */
  @Since("1.4.0")
  def getNumFeatures: Int = this.numFeatures

  /**
   * The dimension of training features.
   */
  protected var numFeatures: Int = -1

  /**
   * Set if the algorithm should use feature scaling to improve the convergence during optimization.
   */
  private[mllib] def setFeatureScaling(useFeatureScaling: Boolean): this.type = {
    this.useFeatureScaling = useFeatureScaling
    this
  }

  /**
   * Create a model given the weights and intercept
   */
  protected def createModel(weights: Vector, intercept: Double): M

  /**
   * Get if the algorithm uses addIntercept
   *
   */
  @Since("1.4.0")
  def isAddIntercept: Boolean = this.addIntercept

  /**
   * Set if the algorithm should add an intercept. Default false.
   * We set the default to false because adding the intercept will cause memory allocation.
   *
   */
  @Since("0.8.0")
  def setIntercept(addIntercept: Boolean): this.type = {
    this.addIntercept = addIntercept
    this
  }

  /**
   * Set if the algorithm should validate data before training. Default true.
   *
   */
  @Since("0.8.0")
  def setValidateData(validateData: Boolean): this.type = {
    this.validateData = validateData
    this
  }

  /**
   * Run the algorithm with the configured parameters on an input
   * RDD of LabeledPoint entries.
   *
   */
  @Since("0.8.0")
  def run(input: RDD[LabeledPoint]): M = {
    if (numFeatures < 0) {
      numFeatures = input.map(_.features.size).first()
    }

    /**
     * When `numOfLinearPredictor > 1`, the intercepts are encapsulated into weights,
     * so the `weights` will include the intercepts. When `numOfLinearPredictor == 1`,
     * the intercept will be stored as separated value in `GeneralizedLinearModel`.
     * This will result in different behaviors since when `numOfLinearPredictor == 1`,
     * users have no way to set the initial intercept, while in the other case, users
     * can set the intercepts as part of weights.
     *
     * TODO: See if we can deprecate `intercept` in `GeneralizedLinearModel`, and always
     * have the intercept as part of weights to have consistent design.
     */
    val initialWeights = {
      if (numOfLinearPredictor == 1) {
        Vectors.zeros(numFeatures)
      } else if (addIntercept) {
        Vectors.zeros((numFeatures + 1) * numOfLinearPredictor)
      } else {
        Vectors.zeros(numFeatures * numOfLinearPredictor)
      }
    }
    run(input, initialWeights)
  }

  /**
   * Run the algorithm with the configured parameters on an input RDD
   * of LabeledPoint entries starting from the initial weights provided.
   *
   */
  @Since("1.0.0")
  def run(input: RDD[LabeledPoint], initialWeights: Vector): M = {

    if (numFeatures < 0) {
      numFeatures = input.map(_.features.size).first()
    }

    if (input.getStorageLevel == StorageLevel.NONE) {
      logWarning("The input data is not directly cached, which may hurt performance if its"
        + " parent RDDs are also uncached.")
    }

    // Check the data properties before running the optimizer
    if (validateData && !validators.forall(func => func(input))) {
      throw new SparkException("Input validation failed.")
    }

    /**
     * Scaling columns to unit variance as a heuristic to reduce the condition number:
     *
     * During the optimization process, the convergence (rate) depends on the condition number of
     * the training dataset. Scaling the variables often reduces this condition number
     * heuristically, thus improving the convergence rate. Without reducing the condition number,
     * some training datasets mixing the columns with different scales may not be able to converge.
     *
     * GLMNET and LIBSVM packages perform the scaling to reduce the condition number, and return
     * the weights in the original scale.
     * See page 9 in http://cran.r-project.org/web/packages/glmnet/glmnet.pdf
     *
     * Here, if useFeatureScaling is enabled, we will standardize the training features by dividing
     * the variance of each column (without subtracting the mean), and train the model in the
     * scaled space. Then we transform the coefficients from the scaled space to the original scale
     * as GLMNET and LIBSVM do.
     *
     * Currently, it's only enabled in LogisticRegressionWithLBFGS
     */
    val scaler = if (useFeatureScaling) {
      new StandardScaler(withStd = true, withMean = false).fit(input.map(_.features))
    } else {
      null
    }

    // Prepend an extra variable consisting of all 1.0's for the intercept.
    // TODO: Apply feature scaling to the weight vector instead of input data.
    val data =
      if (addIntercept) {
        if (useFeatureScaling) {
          input.map(lp => (lp.label, appendBias(scaler.transform(lp.features)))).cache()
        } else {
          input.map(lp => (lp.label, appendBias(lp.features))).cache()
        }
      } else {
        if (useFeatureScaling) {
          input.map(lp => (lp.label, scaler.transform(lp.features))).cache()
        } else {
          input.map(lp => (lp.label, lp.features))
        }
      }

    /**
     * TODO: For better convergence, in logistic regression, the intercepts should be computed
     * from the prior probability distribution of the outcomes; for linear regression,
     * the intercept should be set as the average of response.
     */
    val initialWeightsWithIntercept = if (addIntercept && numOfLinearPredictor == 1) {
      appendBias(initialWeights)
    } else {
      /** If `numOfLinearPredictor > 1`, initialWeights already contains intercepts. */
      initialWeights
    }

    val weightsWithIntercept = optimizer.optimize(data, initialWeightsWithIntercept)

    val intercept = if (addIntercept && numOfLinearPredictor == 1) {
      weightsWithIntercept(weightsWithIntercept.size - 1)
    } else {
      0.0
    }

    var weights = if (addIntercept && numOfLinearPredictor == 1) {
      Vectors.dense(weightsWithIntercept.toArray.slice(0, weightsWithIntercept.size - 1))
    } else {
      weightsWithIntercept
    }

    /**
     * The weights and intercept are trained in the scaled space; we're converting them back to
     * the original scale.
     *
     * Math shows that if we only perform standardization without subtracting means, the intercept
     * will not be changed. w_i = w_i' / v_i where w_i' is the coefficient in the scaled space, w_i
     * is the coefficient in the original space, and v_i is the variance of the column i.
     */
    if (useFeatureScaling) {
      if (numOfLinearPredictor == 1) {
        weights = scaler.transform(weights)
      } else {
        /**
         * For `numOfLinearPredictor > 1`, we have to transform the weights back to the original
         * scale for each set of linear predictor. Note that the intercepts have to be explicitly
         * excluded when `addIntercept == true` since the intercepts are part of weights now.
         */
        var i = 0
        val n = weights.size / numOfLinearPredictor
        val weightsArray = weights.toArray
        while (i < numOfLinearPredictor) {
          val start = i * n
          val end = (i + 1) * n - { if (addIntercept) 1 else 0 }

          val partialWeightsArray = scaler.transform(
            Vectors.dense(weightsArray.slice(start, end))).toArray

          System.arraycopy(partialWeightsArray, 0, weightsArray, start, partialWeightsArray.size)
          i += 1
        }
        weights = Vectors.dense(weightsArray)
      }
    }

    // Warn at the end of the run as well, for increased visibility.
    if (input.getStorageLevel == StorageLevel.NONE) {
      logWarning("The input data was not directly cached, which may hurt performance if its"
        + " parent RDDs are also uncached.")
    }

    // Unpersist cached data
    if (data.getStorageLevel != StorageLevel.NONE) {
      data.unpersist(false)
    }

    createModel(weights, intercept)
  }
}

```  

## 2.继承GeneralizedLinearAlgorithm的相关类
在IDE里查看一下类继承关系，可以查找出继承GeneralizedLinearAlgorithm的类有：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/mllib/GeneralizedLinearModel/1.png)    
在网上找了一张图，比较清晰地描述了各个类之间的关系：  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/traditional-algorithm/mllib/GeneralizedLinearModel/2.png)  


## 3.GeneralizedLinearAlgorithm源码分析  
源码中一上来的注释很重要，直接告诉了我们本类的用途与使用方式：  
GeneralizedLinearAlgorithm implements methods to train a Generalized Linear Model (GLM).  
这句话告诉我们，GeneralizedLinearAlgorithm是用来训练一个线性模型GML的。  
This class should be extended with an Optimizer to create a new GLM.  
这句话很重要，提示我们这个类必须被一个带有Optimizer的类继承并且得到一个新的GLM。其实从源码中我们也能很容易看出，因为这是个抽象类，抽象类的作用就是用来被继承然后实现的！  


一开始定义一些属性（选择一些重要的）：  
validators:注意输入是Seq[RDD[LabeledPoint] => Boolean]  
addIntercept:是否添加截距  
useFeatureScaling：是否进行FeatureScaling  
有关FeatureScaling的作用，请看这一行注释：  

```
Whether to perform feature scaling before model training to reduce the condition numbers which can significantly help the optimizer converging faster. The scaling correction will be translated back to resulting model weights, so it's transparent to users.Note: This technique is used in both libsvm and glmnet packages. Default false.
```  

从这段注释可以看出，featurescaling的作用是为了减小条件数，使得优化求解过程更快更稳定。如果你不知道什么是条件数，请参看 http://blog.csdn.net/bitcarmanlee/article/details/51945271 一文。  

里面最重要的就是run方法了。  

```
    if (numFeatures < 0) {
      numFeatures = input.map(_.features.size).first()
    }
```  

此为获得特征的维度数量  

```
    if (input.getStorageLevel == StorageLevel.NONE) {
      logWarning("The input data is not directly cached, which may hurt performance if its"
        + " parent RDDs are also uncached.")
    }

    // Check the data properties before running the optimizer
    if (validateData && !validators.forall(func => func(input))) {
      throw new SparkException("Input validation failed.")
    }
```  

这都是检测输入的样本  

```
    val scaler = if (useFeatureScaling) {
      new StandardScaler(withStd = true, withMean = false).fit(input.map(_.features))
    } else {
      null
    }
```  

这部分是通过useFeatureScaling，达到样本标准化的目的！  

```
    val data =
      if (addIntercept) {
        if (useFeatureScaling) {
          input.map(lp => (lp.label, appendBias(scaler.transform(lp.features)))).cache()
        } else {
          input.map(lp => (lp.label, appendBias(lp.features))).cache()
        }
      } else {
        if (useFeatureScaling) {
          input.map(lp => (lp.label, scaler.transform(lp.features))).cache()
        } else {
          input.map(lp => (lp.label, lp.features))
        }
      }
```  

这一段很明显，是添加偏置项！  

```
    val initialWeightsWithIntercept = if (addIntercept && numOfLinearPredictor == 1) {
      appendBias(initialWeights)
    } else {
      /** If `numOfLinearPredictor > 1`, initialWeights already contains intercepts. */
      initialWeights
    }
```  

由变量命名就可以看出，这是初始化权重，  

```
    val weightsWithIntercept = optimizer.optimize(data, initialWeightsWithIntercept)
```  

请注意：真正的求解，就是这一行代码！通过optimizer里的optmize方法求解各特征的权重！  
重要的事情再强调一下：真正的求解就这一行代码！  

后续的代码就是对求解以后各特征权重的处理了！获取偏置项权重，获取各维度的权重！如果进行了useFeatureScaling，需要将得到的权重进行还原！  

看看最后一行代码：  

```
    createModel(weights, intercept)

```  

调用createModel方法返回模型！是不是我们一上来就说了，GLA是用来返回一个新的GLM(GeneralizedLinearModel)的！  

再具体一点，到底怎么得到一个GLM呢？  
很简单，看看createModel方法就行了  

```
  protected def createModel(weights: Vector, intercept: Double): M
```  

是不是特别简单？只需要将各特征的权重以及截距的权重输入，然后调用createModel方法，就可以得到一个GLM了！  

## 4、GeneralizedLinearModel

```
/**
 * :: DeveloperApi ::
 * GeneralizedLinearModel (GLM) represents a model trained using
 * GeneralizedLinearAlgorithm. GLMs consist of a weight vector and
 * an intercept.
 *
 * @param weights Weights computed for every feature.
 * @param intercept Intercept computed for this model.
 *
 */
abstract class GeneralizedLinearModel @Since("1.0.0") (
    @Since("1.0.0") val weights: Vector,
    @Since("0.8.0") val intercept: Double)
  extends Serializable {

  /**
   * Predict the result given a data point and the weights learned.
   *
   * @param dataMatrix Row vector containing the features for this data point
   * @param weightMatrix Column vector containing the weights of the model
   * @param intercept Intercept of the model.
   */
  protected def predictPoint(dataMatrix: Vector, weightMatrix: Vector, intercept: Double): Double

  /**
   * Predict values for the given data set using the model trained.
   *
   * @param testData RDD representing data points to be predicted
   * @return RDD[Double] where each entry contains the corresponding prediction
   *
   */
  @Since("1.0.0")
  def predict(testData: RDD[Vector]): RDD[Double] = {
    // A small optimization to avoid serializing the entire model. Only the weightsMatrix
    // and intercept is needed.
    val localWeights = weights
    val bcWeights = testData.context.broadcast(localWeights)
    val localIntercept = intercept
    testData.mapPartitions { iter =>
      val w = bcWeights.value
      iter.map(v => predictPoint(v, w, localIntercept))
    }
  }

  /**
   * Predict values for a single data point using the model trained.
   *
   * @param testData array representing a single data point
   * @return Double prediction from the trained model
   *
   */
  @Since("1.0.0")
  def predict(testData: Vector): Double = {
    predictPoint(testData, weights, intercept)
  }

  /**
   * Print a summary of the model.
   */
  override def toString: String = {
    s"${this.getClass.getName}: intercept = ${intercept}, numFeatures = ${weights.size}"
  }
}
```  

GeneralizedLinearModel也是一个抽象类，相对来说比较简单一些。  
要明白GeneralizedLinearModel，只需要读懂最开始的注释就OK了。  

```
 GeneralizedLinearModel (GLM) represents a model trained using
 GeneralizedLinearAlgorithm. GLMs consist of a weight vector and
 an intercept.
```  
两点信息：  
1.GLM是一个用GLA训练得到的模型。  
2.GLM模型由一个截距的权重与特征权重组成。  

## 5.后记
要想了解算法的来龙去脉，还是得仔细看源码。看优秀的源码，还是挺有收获的。加油！
