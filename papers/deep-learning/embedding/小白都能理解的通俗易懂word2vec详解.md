## 前言
自从Mikolov在他2013年的论文“Efficient Estimation of Word Representation in Vector Space”提出词向量的概念后，NLP领域仿佛一下子进入了embedding的世界，Sentence2Vec、Doc2Vec、Everything2Vec。词向量基于语言模型的假设——“一个词的含义可以由它的上下文推断得出“，提出了词的Distributed Representation表示方法。相较于传统NLP的高维、稀疏的表示法(One-hot Representation)，Word2Vec训练出的词向量是低维、稠密的。Word2Vec利用了词的上下文信息，语义信息更加丰富，目前常见的应用有：  
1. 使用训练出的词向量作为输入特征，提升现有系统，如应用在情感分析、词性标注、语言翻译等神经网络中的输入层。  
2. 直接从语言学的角度对词向量进行应用，如使用向量的距离表示词语相似度、query相关性等。  
注：前言部分内容来自参考文献1。  

## 1.什么是word2vec
如果用一句比较简单的话来总结，word2vec是用一个一层的神经网络(即CBOW)把one-hot形式的稀疏词向量映射称为一个n维(n一般为几百)的稠密向量的过程。为了加快模型训练速度，其中的tricks包括Hierarchical softmax，negative sampling, Huffman Tree等。  

在NLP中，最细粒度的对象是词语。如果我们要进行词性标注，用一般的思路，我们可以有一系列的样本数据(x,y)。其中x表示词语，y表示词性。而我们要做的，就是找到一个x -> y的映射关系，传统的方法包括Bayes,SVM等算法。但是我们的数学模型，一般都是数值型的输入。但是NLP中的词语，是人类的抽象总结，是符号形式的（比如中文、英文、拉丁文等等），所以需要把他们转换成数值形式，或者说——嵌入到一个数学空间里，这种嵌入方式，就叫词嵌入（word embedding)，而 Word2vec，就是词嵌入（ word embedding) 的一种。  

在 NLP 中，把 x 看做一个句子里的一个词语，y 是这个词语的上下文词语，那么这里的 f，便是 NLP 中经常出现的『语言模型』（language model），这个模型的目的，就是判断 (x,y) 这个样本，是否符合自然语言的法则，更通俗点说就是：词语x和词语y放在一起，是不是人话。  

Word2vec 正是来源于这个思想，但它的最终目的，不是要把 f 训练得多么完美，而是只关心模型训练完后的副产物——模型参数（这里特指神经网络的权重），并将这些参数，作为输入 x 的某种向量化的表示，这个向量便叫做——词向量。  
(上面部分内容来自参考文献2)  

## 2.CBOW与Skip-Gram
word2vec里面有两个重要的模型-CBOW模型(Continuous Bag-of-Words Model)与Skip-gram模型。在Tomas Mikolov的paper中给出了示意图。  

![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/deep-learning/embedding/word2vec/1.jpeg)  

由名字与图都很容易看出来，CBOW就是根据某个词前面的C个词或者前后C个连续的词，来计算某个词出现的概率。Skip-Gram Model相反，是根据某个词，然后分别计算它前后出现某几个词的各个概率。  

上一张图，可以比较清楚地看清楚CBOW的训练过程。  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/deep-learning/embedding/word2vec/2.jpeg)  
(图片来自网络)

把这张图看懂，基本word2vec就懂了一大半。下面来详细说说这张图。  
词向量最简单的方式是1-of-N的one-hot方式。onehot对于同学们来说都很熟悉了，也就是从很大的词库corpus里选V个频率最高的词(忽略其他的) ，V一般比较大，比如V＝10W，固定这些词的顺序，然后每个词就可以用一个V维的稀疏向量表示了，这个向量只有一个位置的元素是1，其他位置的元素都是0。One hot方式其实就是简单的直接映射，所以缺点也很明显，维数很大，也没啥计算上的意义。  
在上图中，  
1、Input layer输出层：是上下文单词的one hot。假设单词向量空间的维度为V，即整个词库corpus大小为V，上下文单词窗口的大小为C。  
2、假设最终词向量的维度大小为N，则图中的权值共享矩阵为W。W的大小为 $V * N$，并且初始化。  
3、假设语料中有一句话"我爱你"。如果我们现在关注"爱"这个词，令C=2，则其上下文为"我","你"。模型把"我" "你"的onehot形式作为输入。易知其大小为$1 * V$。C个$1*V$大小的向量分别跟同一个$V * N$大小的权值共享矩阵W相乘，得到的是C个$1 * N$大小的隐层hidden layer。    
4.C个$1 * N$大小的hidden layer取平均，得到一个$1*N$大小的向量，即图中的Hidden layer。  
5.输出权重矩阵W'为$N * V$，并进行相应的初始化工作。  
6.将得到的Hidden layer向量 $1 * N$与W'相乘，并且用softmax处理，得到$1*V$的向量，此向量的每一维代表corpus中的一个单词。概率中最大的index所代表的单词为预测出的中间词。    
7.与groud truth中的one hot比较，求loss function的的极小值。  

具体计算过程为：  
从input -> hidden: $W^T * x$， W为V*N矩阵，x为V * 1向量，最终隐层的结果为 N * 1  
从hidden -> output: $x^T * W^{'}$，其中x为$N * 1$向量，$W^{'}$为V * N，最终结果为$1 * V$  

## 3.word2vec其实不关注模型  
word2vec可以分为两部分：模型与通过模型获得的词向量。  
word2vec的思路与自编码器(auto-encoder)的思路比较相似。都是先基于训练数据构建一个神经网络。当这个网络训练好一有，我们并不会利用这个训练好的网络处理新任务，我们真正需要的是这个模型通过训练数据所学得的参数，例如隐层的权重矩阵——后面我们将会看到这些权重在Word2Vec中实际上就是我们试图去学习的“word vectors”。基于训练数据建模的过程，我们给它一个名字叫“Fake Task”，意味着建模并不是我们最终的目的。  

上面提到的这种方法实际上会在无监督特征学习（unsupervised feature learning）中见到，最常见的就是自编码器（auto-encoder）：通过在隐层将输入进行编码压缩，继而在输出层将数据解码恢复初始状态，训练完成后，我们会将输出层“砍掉”，仅保留隐层。  

## 4.tricks

1.hierarchical softmax  
最后预测输出向量时候，大小是1*V的向量，本质上是个多分类的问题。通过hierarchical softmax的技巧，把V分类的问题变成了log(V)次二分类。  

2.negative sampling  
本质上是对训练集进行了采样，从而减小了训练集的大小。  
每个词𝑤的概率由下式决定  
$$len(w) = \frac{count(w)^{3/4}}{\sum\limits_{u \in vocab} count(u)^{3/4}}$$  



## 参考文献：
1.https://zhuanlan.zhihu.com/p/28491088  
2.https://zhuanlan.zhihu.com/p/26306795  
3.http://alwa.info/2016/04/24/Autoencoder-%E8%AF%A6%E8%A7%A3/  
4.https://qrfaction.github.io/2018/03/20/%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9Btrick%E6%80%BB%E7%BB%93/ 数据竞赛trick总结  
