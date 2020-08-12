## 1.item2vec的兴起
自从word2vec被证明效果不错以后，掀起了一股embedding的热潮。item2vec, doc2vec，总结起来就是everything2vec。在实际工作中，embedding的使用也非常广泛，今天我们就来说说常用的item2vec。  

word2vec构建样本时，句子分词以后就构成了一个天然的序列。那么在推荐的应用场景下，如何生成这个序列，或者说如何生成训练样本，成为了一个必须要解决的问题。  

一般来说，有如下两种方式构建训练样本  

1.基于时序的关系  
我们会认为item之间存在时序关系，相当于我们将各个不同的item类比为word2vec的单词，那么将这些item串联起来就相当于将word连起来组成一个句子，这样不管是构造训练集的方式或者训练的方式都可以按照word2vec的方式来进行了。  
比如视频网站的用户观看的视频序列，音乐网站用户听的歌曲序列，我们都可以认为是这种方式。  

2.基于集合的关系  
认为 item 之间存在非常弱的时序关系，或者因为某种原因，我们无法获得 item 的序列。那么这种情况只能放弃考虑 item 间的时空信息，转而使用 item 集合来取代序列。通常我们把用户的行为序列视为一个集合（当然还有其他集合构造方式），我们假定一个静态的环境，在这个环境中，共现在同一个集合的 item 就可以认为它们是相似的，然后视为正样本，不管它们是以什么样的顺序产生的，如果某两个 item 频繁共现，二者的 Embedding 则可能也很相似。很明显，这种利用集合共现性构建样本的方式与 Word2Vec 的输入样本还是不一样的，因此无法直接应用 Word2Vec 的算法，这就需要对 Word2Vec 的过程进行调整。另外还需要注意的是，上面的这种的假设是有局限性的，不一定适用于其它场景。  
基于集合的示例比如电商网站订单中的商品集合， 另外比如用户的浏览物料item的集合。  

## 2.常用的Embedding方式
1.以SVD为代表的MF方式。通过对user-item-score矩阵的分解，或者user-item的隐式矩阵分解，可以获取user与item的隐向量，该向量可以作为embedding向量使用。  
2.FM算法。FM学习了各个特征的隐向量表示，从而可以将这些学习到的隐向量作为特征的embedding使用。  
3.DNN-Embedding 通过神经网络，利用接入Embedding层与目标loss进行joint train，从而学习其特征表达，这是一种端到端的embedding训练方式(end-to-end)。  
4.item2vec 与word2vec类似的方式。  
5.graph embedding，是基于图模型的方法，包括deep walk, node2vec, eges等方法。  

## 3.item2vec与MF的区别
首先，二者都应用了隐向量来表征实体特征，不同的是，传统的 MF 通常是 user-item 矩阵，而 Item2Vec 通过滑动窗口样本生成的方式构造出的则更像是 item-item 矩阵；另外，二者得到隐向量的方式也不同，MF 利用均方差损失，使预测得分与已有得分之间的误差尽可能地小，而 Item2Vec 则是利用空间信息并借助了最大似然估计的思想，使用对数损失，使上下文关系或者共现关系构造出的正样本的 item Pair 出现的概率可能地大；此外训练 Item2Vec 的时候还要引入负样本，这也是与 MF 不同的地方。  

对于二者在推荐效果上的差异，一个经验是传统 MF 推荐会让热门内容经常性排在前面，而 Item2vec 能更好的学到中频内容的相似性。Iterm2Vec 加上较短的时间窗口，相似推荐会比 MF 好很多。  

## 4.原理  
对于出现在同一个集合的item对我们视为正样本，对于集合$\omega_1, \omega_2, \cdots, \omega_K$，目标函数为  
$$\frac{1}{K} \sum_{i=1}^{K}\sum_{j \neq i}^{K} \log p(w_j | w_i)$$  

利用负采样，将$p(w_j | w_i)$可以定义为  
$$p(w_j | w_i) = \frac{exp(u_i ^T v_j)}{\sum_{k \in I_W} exp(u_k ^T v_j)}$$  

简单而言，对于给定的item序列，选择窗口大小为c，skip-gram通过当前item来预测前后c个item的概率，从而使得其后验概率最大，通过极大似然进行优化整体损失。  

负采样的词频计算方式跟word2vec一样。  

## 参考文献
1.https://lumingdong.cn/application-practice-of-embedding-in-recommendation-system.html