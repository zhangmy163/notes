# Linux标准输入输出

linux中有三种标准输入输出，分别是STDIN，STDOUT，STDERR，对应的数字是0，1，2。

`STDIN`是标准输入，默认从键盘读取信息；

`STDOUT`是标准输出，默认将输出结果输出至终端；

`STDERR`是标准错误，默认将输出结果输出至终端。

由于STDOUT与STDERR都会默认显示在终端上，为了区分，就有了编号的0，1，2的定义，用1表示STDOUT，2表示STDERR。

2>&1，指将标准输出、标准错误指定为同一输出路径

举例说明：

eg1:

`cat >>test.txt 2>&1 <<END   #----建立test.txt文件，当输入遇到END时，退出`

eg2:

1、以普通用户执行`find /etc -name passwd`命令，默认会将命令的执行结果（STDOUT）与错误信息（STDERR）都输出至终端显示器。

2、执行`find /etc -name passwd >find.out 2>find.err`，会将STDOUT与STDERR分别存放至find.out和find.err中。该命令也可以写成下面三种形式
```
  find /etc -name passwd 1>find.out 2>find.err

  find /etc -name passwd 2>find.err >find.out

  find /etc -name passwd 2>find.err 1>find.out
```
3、若要将所有标准输出及标准错误都输出至文件，可用&表示全部1和2的信息，eg：

`find /etc -name passwd &>find.all 或 find /etc -name passwd >find.all 2>&1`

4、`2>&1    #----标准错误重新定向到标准输出`

5、用法：`find /etc -name passwd & 2>&1 |less`

可分解成

find /etc -name passwd & 表示前面的命令放到后台执行。

2>&1 |less 表示将标准错误重定向至标准输出，并用less进行分页显示

**注意**:所以一条命令输出到终端的不一定都是STDOUT，比如`java -version`

```
$ java -version
java version "1.7.0_17"
Java(TM) SE Runtime Environment (build 1.7.0_17-b02)
Java HotSpot(TM) 64-Bit Server VM (build 23.7-b01, mixed mode)

$ java -version > v.txt  #发现v.txt是空的

$ java -version 2> v.txt  #此时v.txt才会有信息
```

# Linux重定向

1.1      重定向符号

`>`               输出重定向到一个文件或设备 覆盖原来的文件

`>!`              输出重定向到一个文件或设备 强制覆盖原来的文件

`>>`             输出重定向到一个文件或设备 追加原来的文件

`<`               输入重定向到一个程序

1.2标准错误重定向符号

`2>`             将一个标准错误输出重定向到一个文件或设备 覆盖原来的文件  b-shell

`2>>`           将一个标准错误输出重定向到一个文件或设备 追加到原来的文件

`2>&1`         将一个标准错误输出重定向到标准输出 注释:1 可能就是代表 标准输出

`>&`             将一个标准错误输出重定向到一个文件或设备 覆盖原来的文件  c-shell

`|&`              将一个标准错误 管道 输送 到另一个命令作为输入

1.3命令重导向示例

在 bash 命令执行的过程中，主要有三种输出入的状况，分别是：
1. 标准输入：代码为 0 ；或称为 stdin ；使用的方式为 <
2. 标准输出：代码为 1 ；或称为 stdout；使用的方式为 1>
3. 错误输出：代码为 2 ；或称为 stderr；使用的方式为 2>


[test @test test]# `ls -al > list.txt`
将显示的结果输出到 list.txt 文件中，若该文件以存在则予以取代！


[test @test test]# `ls -al >> list.txt`
将显示的结果累加到 list.txt 文件中，该文件为累加的，旧数据保留！


[test @test test]# `ls -al  1> list.txt   2> list.err`
将显示的数据，正确的输出到 list.txt 错误的数据输出到 list.err


[test @test test]# `ls -al 1> list.txt 2> &1`
将显示的数据，不论正确或错误均输出到 list.txt 当中！错误与正确文件输出到同一个文件中，则必须以上面的方法来写！不能写成其它格式！

[test @test test]# `ls -al 1> list.txt 2> /dev/null`
将显示的数据，正确的输出到 list.txt 错误的数据则予以丢弃！ **/dev/null ，可以说成是黑洞装置。为空，即不保存。**

1.4为何要使用命令输出重导向

• 当屏幕输出的信息很重要，而且我们需要将他存下来的时候；

• 背景执行中的程序，不希望他干扰屏幕正常的输出结果时；

• 一些系统的例行命令（例如写在 /etc/crontab 中的文件）的执行结果，希望他可以存下来时；

• 一些执行命令，我们已经知道他可能的错误讯息，所以想以 `2> /dev/null` 将他丢掉时；

• 错误讯息与正确讯息需要分别输出时。
