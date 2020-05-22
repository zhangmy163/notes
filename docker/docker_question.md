# docker bash 中文问题

>https://zhuanlan.zhihu.com/p/31078295

1.之前线上使用docker，启动时运行脚本来启动`superset runserver -w 5`

测试如下情况：
```
a)容器直接启动：产品手册打开报错
b)进入容器运行superset runserver -w5启动：产品手册可以打开
c)在宿主机运行docker exec -it run_imedia superset runserver -w5启动：产品手册打开报错
```


2.准备上线的docker supervisor，启动时supervisor运行`gunicogunicorn -w 5`

测试如下情况：
```
a)容器直接启动：产品手册打开报错
b)进入容器运行supervisorctl update启动：产品手册打开报错
c)进入容器运行gunicogunicorn -w 5启动：产品手册可以打开
```

修改pdf不带中文，以上容器直接启动均可打开

已经找到解决方案。

需要在Dockerfile中这只LANG，否则docker bashde locale都是POSIX。而进入容器后的locale是en_US.UTF-8

```
$ docker exec -it centos:6 locale
LANG=
LC_CTYPE="POSIX"
LC_NUMERIC="POSIX"
LC_TIME="POSIX"
LC_COLLATE="POSIX"
LC_MONETARY="POSIX"
LC_MESSAGES="POSIX"
LC_PAPER="POSIX"
LC_NAME="POSIX"
LC_ADDRESS="POSIX"
LC_TELEPHONE="POSIX"
LC_MEASUREMENT="POSIX"
LC_IDENTIFICATION="POSIX"
LC_ALL=
```

在Dockerfile中增加
```
# Set the locale
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8
```

# 容器中火狐浏览器中文显示方框文字问题

>http://wenda.chinahadoop.cn/question/127
>https://www.zhihu.com/question/35731746

```
#解决火狐浏览器中文展示方框数字问题
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

RUN yum groupinstall -y fonts && echo 'LANG="zh_CN.UTF-8"' > /etc/locale.conf && localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
```