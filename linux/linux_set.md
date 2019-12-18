Linux set命令用于设置shell。

set指令能设置所使用shell的执行方式，可依照不同的需求来做设置。

我只用过set -e、set -u

> 其他详细命令可参考[菜鸟教程](https://www.runoob.com/linux/linux-comm-set.html)

  * `-e`：若指令传回值不等于0，则立即退出shell。
  * `-u`：当执行时使用到未定义过的变量，则显示错误信息。

例子：

`-e`

test.sh  
```
#! /bin/bash
set -e
echo "输出第一条信息"
cat null
echo "输出第二条信息"
```
执行结果：
```
$ bash test.sh
输出第一条信息
cat: null: No such file or directory
#---null不存在，停止运行，没有输出后面的信息
```

`-u`

test.sh
```
#! /bin/bash
set -u
echo "输出第一条信息"
echo $name
echo "输出第二条信息"
```
执行结果：
```
$ bash test.sh
输出第一条信息
test.sh: line 4: name: unbound variable
```
