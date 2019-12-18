一般执行脚本，先判断参数是否符合要求，如果不符合则退出。

如何判断参数是否符合要求？

### 一、要求脚本必须传入参数

`if [ -n "$1" ]`

`if [ -z "$1" ]`

  * `-n <string>` ：如果 string长度非零，则为真 
  * `-z <string>` ：如果 string长度为零，则为真

#### 先看一下`-n`的使用：

test.sh

```
#！ /bin/bash
echo 'if -n 加引号"$1"'
if [ -n "$1" ]; then
    echo "包含第一个参数"
else
    echo "没有包含第一参数"
fi
echo "========"

echo "if -n 不加引号\$1"
if [ -n $1 ]; then
    echo "包含第一个参数"
else
    echo "没有包含第一参数"
fi
```
运行结果：
```
$ bash test.sh
if -n 加引号"$1"
没有包含第一参数
========
if -n 不加引号$1
包含第一个参数

$ bash test.sh 1
if -n 加引号"$1"
包含第一个参数
========
if -n 不加引号$1
包含第一个参数
```

从运行结果可以看出，如果$1不加引号，在不输入参数时，则-n $1为真，**原因**：因为不加""时该if语句等效于if [ -n ]，shell 会把它当成if [ str1 ]来处理，-n自然不为空，所以为真，验证步骤见下方。所以此处需**注意**，如果想使用-n来判断参数，$1**一定**要加引号

#### `-z`的使用

test.sh

```
#! /bin/bash
echo 'if -z 加引号"$1"'
if [ -z "$1" ]; then
    echo "没有包含第一个参数"
else
    echo "包含第一参数"
fi
echo "========"

echo "if -z 不加引号\$1"
if [ -z $1 ]; then
    echo "没有包含第一个参数"
else
    echo "包含第一参数"
fi
```

运行结果：
```
$ bash test.sh
if -z 加引号"$1"
没有包含第一个参数
========
if -z 不加引号$1
没有包含第一个参数

$ bash test.sh 1
if -z 加引号"$1"
包含第一参数
========
if -z 不加引号$1
包含第一参数
```
从运行结果可以看出，对-z $1来说，加引号与不加引号运行结果一样，所以对比-n的运行结果，所以建议不论-n还是-z，$1最好都加引号。

#### 验证[ -n ] [ -z ]
```
#! /bin/bash
if [ -n ]; then
    echo '-n什么都没有为真'
else
    echo '-n什么都没有为假'
fi
echo "========"
if [ -n "" ]; then
    echo '-n ""为真'
else
    echo '-n ""为假'
fi
echo "========"
if [ -z  ]; then
    echo "-z什么都没有为真"
else
    echo "-z什么都没有为假"
fi
echo "========"
if [ -z "" ]; then
    echo '-z ""为真'
else
    echo '-z ""为假'
fi
echo "========"
if [ "abc" ]; then
    echo '[ "abc" ]为真'
else
    echo '[ "abc" ]为假'
fi

```
运行结果
```
$ bash test.sh
-n什么都没有为真
========
-n ""为假
========
-z什么都没有为真
========
-z ""为真
========
[ "abc" ]为真

```


### 二、对参数个数的判断

`if [ "$#" -lt <n> ]` #n为整数，-lt小于,-eq等于，其他判断可以参考if的相关判断,$#加不加引号都可以，建议和-n统一，都带上引号

test.sh

```
#! /bin/bash
if [ "$#" -lt 3 ]
then
  echo "参数少于3个，错误"
  exit 1
else
  echo "参数数量大于等于3个，正确"
fi
```

运行结果：

```
$ bash test.sh 1
参数少于3个，错误

$ bash test.sh 1 2 3
参数数量大于等于3个，正确
```

