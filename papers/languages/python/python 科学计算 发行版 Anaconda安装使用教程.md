## 1.原生python的不方便
作为一个数据与算法工作者，python的使用频率很高。现阶段python做科学计算的标配是numpy+scipy+matplotlib+sklearn+pandas。可惜的是，原生的python是不带这些包的。于是，每次遇到一个新机器，需要安装这些包。更可气的是，昨晚本博主为了在新机器上安装sklearn，足足花了两小时，中间踩了无数之前没遇到过的天坑加上天朝坑爹的网络。。。作为一个搭建了无数次科学计算环境的老司机还遇到这种情况，估计新手们就更无比郁闷了。于是老司机就想，有没有一个东西把所有常用的科学计算工具都集成好，这样就省了每次搭环境的天坑。。。google一把，发现了今天文章的主角：Anaconda。  

## 2.先看看Anaconda是个什么鬼
Anaconda：蟒蛇，估计来源就是python logo里那条可爱的小蟒蛇吧。  
mac版下载地址： https://www.continuum.io/downloads#_macosx  
看看官网首页是怎么介绍的：  
Anaconda is the leading open data science platform powered by Python. The open source version of Anaconda is a high performance distribution of Python and R and includes over 100 of the most popular Python, R and Scala packages for data science. Additionally, you'll have access to over 720 packages that can easily be installed with conda, our renowned package, dependency and environment manager, that is included in Anaconda. Anaconda is BSD licensed which gives you permission to use Anaconda commercially and for redistribution. See the packages included with Anaconda and the Anaconda changelog.  

通过上面这段牛逼闪闪的介绍，我们知道Anaconda是一个基于python的科学计算平台，这个平台里包含有python,r,scala等绝大部分主流的用于科学计算的包。  

接下来自然就是开始下载了。因为集成有很多牛逼科学计算包的缘故，所以安装包自然也小不了，比如我下载的mac版就有360M。那就慢慢下着吧。还好网络虽然不是很快，好歹还是稳定的，能到一两百k，一个小时左右能下完。这段时间就先干点别的吧。  

## 3.安装配置
下载完成以后，跟mac里安装普通软件一样，双击安装即可。  
安装完以后，开始进行相应的配置。因为我平时使用eclipse开发，正好官网都贴心地给出了在IDE里怎么配置使用，里面就有eclipse，前提是eclipse已经安装了pydev插件。  

以下eclipse配置方法来自官网：  
After you have Eclipse, PyDev, and Anaconda installed, follow these steps to set Anaconda Python as your default by adding it as a new interpreter, and then selecting that new interpreter:  

Open the Eclipse Preferences window:  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/python/anaconda/1.png)    
Go to PyDev -> Interpreters -> Python Interpreter.  
Click the New button:  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/python/anaconda/2.png)  
In the “Interpreter Name” box, type “Anaconda Python”.  
Browse to ~/anaconda/bin/python or wherever your Anaconda Python is installed.  
Click the OK button.  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/python/anaconda/3.png)    
In the next window, select all the folders and click the OK button again to select the folders to add to the SYSTEM python path.  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/python/anaconda/4.png)    
The Python Interpreters window will now display Anaconda Python. Click OK.  
![这里写图片描述](https://github.com/bitcarmanlee/easy-algorithm-interview-photo/blob/master/languages/python/anaconda/5.png)  
You are now ready to use Anaconda Python with your Eclipse and PyDev installation.  

如果是其他IDE，可以上官网查看其他配置方法。具体地址：  
https://docs.continuum.io/anaconda/ide_integration#id8  

## 4.查看Anaconda的基本用法
配置完成以后，查看一下此时系统的python：  

```
lei.wang ~ $ which python
/Users/lei.wang/anaconda/bin/python
lei.wang ~ $ python --version
Python 2.7.12 :: Anaconda 4.1.1 (x86_64)
```  

此时，系统默认的python已经变成了Anaconda的版本！  
为什么会这样呢？原来是安装过程中，偷偷给我们在home目录下生成了一个.bashrc_profile文件，并在里面加入了PATH：  

```
# added by Anaconda2 4.1.1 installer
export PATH="/Users/wanglei/anaconda/bin:$PATH"
```  

所以这个时候我们的bash里使用python的话，已经指向了anaconda里的python解释器。  
如果使用的不是mac的标准bash，而是zsh，不用着急，将上面一行配置复制粘贴到.zshrc文件中，然后source一下.zshrc文件即可！  


执行一下conda命令：  

```
lei.wang ~ $ conda
usage: conda [-h] [-V] [--debug] command ...

conda is a tool for managing and deploying applications, environments and packages.

Options:

positional arguments:
  command
    info         Display information about current conda install.
    help         Displays a list of available conda commands and their help
                 strings.
    list         List linked packages in a conda environment.
    search       Search for packages and display their information. The input
                 is a Python regular expression. To perform a search with a
                 search string that starts with a -, separate the search from
                 the options with --, like 'conda search -- -h'. A * in the
                 results means that package is installed in the current
                 environment. A . means that package is not installed but is
                 cached in the pkgs directory.
    create       Create a new conda environment from a list of specified
                 packages.
    install      Installs a list of packages into a specified conda
                 environment.
    update       Updates conda packages to the latest compatible version. This
                 command accepts a list of package names and updates them to
                 the latest versions that are compatible with all other
                 packages in the environment. Conda attempts to install the
                 newest versions of the requested packages. To accomplish
                 this, it may update some packages that are already installed,
                 or install additional packages. To prevent existing packages
                 from updating, use the --no-update-deps option. This may
                 force conda to install older versions of the requested
                 packages, and it does not prevent additional dependency
                 packages from being installed. If you wish to skip dependency
                 checking altogether, use the '--force' option. This may
                 result in an environment with incompatible packages, so this
                 option must be used with great caution.
    upgrade      Alias for conda update. See conda update --help.
    remove       Remove a list of packages from a specified conda environment.
    uninstall    Alias for conda remove. See conda remove --help.
    config       Modify configuration values in .condarc. This is modeled
                 after the git config command. Writes to the user .condarc
                 file (/Users/lei.wang/.condarc) by default.
    init         Initialize conda into a regular environment (when conda was
                 installed as a Python package, e.g. using pip). (DEPRECATED)
    clean        Remove unused packages and caches.
    package      Low-level conda package utility. (EXPERIMENTAL)
    bundle       Create or extract a "bundle package" (EXPERIMENTAL)
...
```  

信息太长了，后面的部分就不列举了。不过看到前面这部分选项，就已经足够让我们兴奋了：基本的list，search，install，upgrade，uninstall等功能都包含，说明我们可以向apt-get一样方便管理python的各种依赖了。。。  

先list一下，查看里面都带了哪些牛逼闪闪的科学计算包：  

```
ei.wang ~ $ conda list
# packages in environment at /Users/lei.wang/anaconda:
#
_nb_ext_conf              0.2.0                    py27_0
alabaster                 0.7.8                    py27_0
anaconda                  4.1.1               np111py27_0
anaconda-client           1.4.0                    py27_0
anaconda-navigator        1.2.1                    py27_0
appnope                   0.1.0                    py27_0
appscript                 1.0.1                    py27_0
argcomplete               1.0.0                    py27_1
astropy                   1.2.1               np111py27_0
babel                     2.3.3                    py27_0
backports                 1.0                      py27_0
backports_abc             0.4                      py27_0
beautifulsoup4            4.4.1                    py27_0
bitarray                  0.8.1                    py27_0
blaze                     0.10.1                   py27_0
bokeh                     0.12.0                   py27_0
boto                      2.40.0                   py27_0
bottleneck                1.1.0               np111py27_0
cdecimal                  2.3                      py27_2
cffi                      1.6.0                    py27_0
chest                     0.2.3                    py27_0
click                     6.6                      py27_0
cloudpickle               0.2.1                    py27_0
clyent                    1.2.2                    py27_0
colorama                  0.3.7                    py27_0
conda                     4.1.6                    py27_0
conda-build               1.21.3                   py27_0
conda-env                 2.5.1                    py27_0
configobj                 5.0.6                    py27_0
configparser              3.5.0b2                  py27_1
contextlib2               0.5.3                    py27_0
cryptography              1.4                      py27_0
curl                      7.49.0                        0
cycler                    0.10.0                   py27_0
cython                    0.24                     py27_0
cytoolz                   0.8.0                    py27_0
dask                      0.10.0                   py27_0
datashape                 0.5.2                    py27_0
decorator                 4.0.10                   py27_0
dill                      0.2.5                    py27_0
docutils                  0.12                     py27_2
dynd-python               0.7.2                    py27_0
entrypoints               0.2.2                    py27_0
enum34                    1.1.6                    py27_0
et_xmlfile                1.0.1                    py27_0
fastcache                 1.0.2                    py27_1
flask                     0.11.1                   py27_0
flask-cors                2.1.2                    py27_0
freetype                  2.5.5                         1
funcsigs                  1.0.2                    py27_0
functools32               3.2.3.2                  py27_0
futures                   3.0.5                    py27_0
get_terminal_size         1.0.0                    py27_0
gevent                    1.1.1                    py27_0
greenlet                  0.4.10                   py27_0
grin                      1.2.1                    py27_3
h5py                      2.6.0               np111py27_1
hdf5                      1.8.16                        0
heapdict                  1.0.0                    py27_1
idna                      2.1                      py27_0
imagesize                 0.7.1                    py27_0
ipaddress                 1.0.16                   py27_0
ipykernel                 4.3.1                    py27_0
ipython                   4.2.0                    py27_1
ipython_genutils          0.1.0                    py27_0
ipywidgets                4.1.1                    py27_0
itsdangerous              0.24                     py27_0
jbig                      2.1                           0
jdcal                     1.2                      py27_1
jedi                      0.9.0                    py27_1
jinja2                    2.8                      py27_1
jpeg                      8d                            1
jsonschema                2.5.1                    py27_0
jupyter                   1.0.0                    py27_3
jupyter_client            4.3.0                    py27_0
jupyter_console           4.1.1                    py27_0
jupyter_core              4.1.0                    py27_0
libdynd                   0.7.2                         0
libpng                    1.6.22                        0
libtiff                   4.0.6                         2
libxml2                   2.9.2                         0
libxslt                   1.1.28                        2
llvmlite                  0.11.0                   py27_0
locket                    0.2.0                    py27_1
lxml                      3.6.0                    py27_0
markupsafe                0.23                     py27_2
matplotlib                1.5.1               np111py27_0
mistune                   0.7.2                    py27_1
mkl                       11.3.3                        0
mkl-service               1.1.2                    py27_2
mpmath                    0.19                     py27_1
multipledispatch          0.4.8                    py27_0
nb_anacondacloud          1.1.0                    py27_0
nb_conda                  1.1.0                    py27_0
nb_conda_kernels          1.0.3                    py27_0
nbconvert                 4.2.0                    py27_0
nbformat                  4.0.1                    py27_0
nbpresent                 3.0.2                    py27_0
networkx                  1.11                     py27_0
nltk                      3.2.1                    py27_0
nose                      1.3.7                    py27_1
notebook                  4.2.1                    py27_0
numba                     0.26.0              np111py27_0
numexpr                   2.6.0               np111py27_0
numpy                     1.11.1                   py27_0
odo                       0.5.0                    py27_1
openpyxl                  2.3.2                    py27_0
openssl                   1.0.2h                        1
pandas                    0.18.1              np111py27_0
partd                     0.3.4                    py27_0
path.py                   8.2.1                    py27_0
pathlib2                  2.1.0                    py27_0
patsy                     0.4.1                    py27_0
pep8                      1.7.0                    py27_0
pexpect                   4.0.1                    py27_0
pickleshare               0.7.2                    py27_0
pillow                    3.2.0                    py27_1
pip                       8.1.2                    py27_0
ply                       3.8                      py27_0
psutil                    4.3.0                    py27_0
ptyprocess                0.5.1                    py27_0
py                        1.4.31                   py27_0
pyasn1                    0.1.9                    py27_0
pyaudio                   0.2.7                    py27_0
pycosat                   0.6.1                    py27_1
pycparser                 2.14                     py27_1
pycrypto                  2.6.1                    py27_4
pycurl                    7.43.0                   py27_0
pyflakes                  1.2.3                    py27_0
pygments                  2.1.3                    py27_0
pyopenssl                 0.16.0                   py27_0
pyparsing                 2.1.4                    py27_0
pyqt                      4.11.4                   py27_3
pytables                  3.2.2               np111py27_4
pytest                    2.9.2                    py27_0
python                    2.7.12                        1
python-dateutil           2.5.3                    py27_0
python.app                1.2                      py27_4
pytz                      2016.4                   py27_0
pyyaml                    3.11                     py27_4
pyzmq                     15.2.0                   py27_1
qt                        4.8.7                         3
qtconsole                 4.2.1                    py27_0
qtpy                      1.0.2                    py27_0
readline                  6.2                           2
redis                     3.2.0                         0
redis-py                  2.10.5                   py27_0
requests                  2.10.0                   py27_0
rope                      0.9.4                    py27_1
ruamel_yaml               0.11.7                   py27_0
scikit-image              0.12.3              np111py27_1
scikit-learn              0.17.1              np111py27_2
scipy                     0.17.1              np111py27_1
setuptools                23.0.0                   py27_0
simplegeneric             0.8.1                    py27_1
singledispatch            3.4.0.3                  py27_0
sip                       4.16.9                   py27_0
six                       1.10.0                   py27_0
snowballstemmer           1.2.1                    py27_0
sockjs-tornado            1.0.3                    py27_0
sphinx                    1.4.1                    py27_0
sphinx_rtd_theme          0.1.9                    py27_0
spyder                    2.3.9                    py27_0
sqlalchemy                1.0.13                   py27_0
sqlite                    3.13.0                        0
ssl_match_hostname        3.4.0.2                  py27_1
statsmodels               0.6.1               np111py27_1
sympy                     1.0                      py27_0
terminado                 0.6                      py27_0
tk                        8.5.18                        0
toolz                     0.8.0                    py27_0
tornado                   4.3                      py27_1
traitlets                 4.2.1                    py27_0
unicodecsv                0.14.1                   py27_0
werkzeug                  0.11.10                  py27_0
wheel                     0.29.0                   py27_0
xlrd                      1.0.0                    py27_0
xlsxwriter                0.9.2                    py27_0
xlwings                   0.7.2                    py27_0
xlwt                      1.1.2                    py27_0
xz                        5.2.2                         0
yaml                      0.1.6                         0
zlib                      1.2.8                         3
```  

好吧，至少我常用的都已经在这了。太方便了。  

## 5.写个demo测试一下sklearn
为了测试一下是不是真像传说中那么好用，从网络上现找了部分简单的测试代码：  

```
#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年7月15日

@author: lei.wang
'''

import numpy as np
import urllib
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression


def t1():
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
    raw_data = urllib.urlopen(url)
    dataset = np.loadtxt(raw_data,delimiter=",")
    X = dataset[:,0:7]
    y = dataset[:,8]
    
    # normalize the data attributes
    normalized_X = preprocessing.normalize(X)
    # standardize the data attributes
    standardized_X = preprocessing.scale(X)

    model = ExtraTreesClassifier()
    model.fit(X, y)
    # display the relative importance of each attribute
    print model.feature_importances_
    
    model = LogisticRegression()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

t1()
```  

让代码run起来，得到如下结果：  

```
[ 0.13697671  0.26771573  0.11139943  0.08658428  0.079841    0.16862413
  0.1488587 ]
LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)
             precision    recall  f1-score   support

        0.0       0.79      0.89      0.84       500
        1.0       0.74      0.55      0.63       268

avg / total       0.77      0.77      0.77       768

[[447  53]
 [120 148]]

```  

好吧，sklearn表现正常，能正常输出预期结果。看来，Anaconda确实是为搞算法与数据的同志们提供了一个非常好的工具，省去了我们各种搭环境找依赖包的烦恼！向开发了这么好用工具的程序猿们致敬！  