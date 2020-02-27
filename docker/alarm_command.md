
docker自待的监控子命令

>https://www.cnblogs.com/chenjin2018/p/9928244.html

# ps

`docker  ps` 用来查看当前运行的容器

# top

`docker top [container_name]命令` 查看容器中运行哪些程序

```
docker top test

docker top test -au
```

# stats

`docker stats` 显示每个容器的各种资源情况

默认会显示一个实时变化的列表，展示每个容器的CPU使用率，内存使用量和可用量

**注意**：容器启动时如果没有特别指定内存limit，stats命令会显示host的内存总量，但这并不意味着每个container都能使用到这么多的内存

除此之外docker container stats命令还会显示容器网络和磁盘的IO数据

默认的输出有个缺点，显示的是容器ID而非名字。我们可以在stats命令后面指定容器的名称只显示某些容器的数据。


# 监控利器sysdig

```
sudo docker run -it --name sysdig --privileged=true --volume=/var/run/docker.sock:/host/var/run/docker.sock --volume=/dev:/host/dev --volume=/proc:/host/proc:ro --volume=/boot:/host/boot:ro --volume=/lib/modules:/host/lib/modules:ro --volume=/usr:/host/usr:ro sysdig/sysdig
```



