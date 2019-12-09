# 镜像

拉取镜像

`docker pull <name>:<tag>`

查看本地镜像

`docker images`

删除镜像

`docker rmi <id>或<name>:<tag>`

查看镜像的历史信息

`docker history <id>或<name>:<tag>`

Dockerfile制作镜像

`docker build –t <name>:<tag> –f Dockerfile .`

# 容器

查看容器

`docker ps [-a]`

停止容器

`docker stop <name>或<id>`

进入运行中的容器

`docker exec –it <name>或<id> bash`

容器与主机之间的文件拷贝

```
将主机/www/runoob目录拷贝到容器test的/www目录下

docker cp /www/runoob test:/www/

将主机/www/runoob目录拷贝到容器test中，目录重命名为www。

docker cp /www/runoob test:/www

将容器test的/www目录拷贝到主机的/tmp目录中。

docker cp test:/www /tmp/
```

查看容器日志

`docker logs [-f] <name>或<id>`

启动容器：

`docker run –-name test –it <name>:<tag> bash`
