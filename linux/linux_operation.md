# 获取服务器公网出口IP

`curl https://tool.chinaz.com/|grep IP：|awk -F"IP：" '{print $2}'|awk -F"<" '{print "该服务器的公网出口IP为:"$1}'`

# 获取服务器CPU内存等信息

getinfo.sh
```
#! /bin/bash
echo "======Linux版本======"
head -1 /etc/issue

echo -e "\r\n======CPU信息：======"
cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c

echo -e "\r\n======内存信息：======"
cat /proc/meminfo|grep Total

echo -e "\r\n======内核信息：======"
uname -r
#cat /proc/version

echo -e "\r\n======磁盘信息：======"
df -h
```