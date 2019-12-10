# 镜像

### 拉取镜像

`docker pull <name>:<tag>`

### 查看本地镜像

`docker images`

### 删除镜像

`docker rmi <id>或<name>:<tag>`

### 查看镜像的历史信息

`docker history <id>或<name>:<tag>`

### Dockerfile制作镜像

`docker build –t <name>:<tag> –f Dockerfile .`

# 容器

### 查看容器

`docker ps [-a]`

### 停止容器

`docker stop <name>或<id>`

### 进入运行中的容器

`docker exec –it <name>或<id> bash`

### 容器与主机之间的文件拷贝

```
将主机/www/runoob目录拷贝到容器test的/www目录下

docker cp /www/runoob test:/www/

将主机/www/runoob目录拷贝到容器test中，目录重命名为www。

docker cp /www/runoob test:/www

将容器test的/www目录拷贝到主机的/tmp目录中。

docker cp test:/www /tmp/
```

### 查看容器日志

`docker logs [-f] <name>或<id>`

### 启动容器：

`docker run –-name test –it <name>:<tag> bash`

### docker run

`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

OPTIONS说明：

* `-d`：后台运行容器，并返回容器ID
* `-i`：以交互模式运行容器，通常与 -t 同时使用
* `-p`：指定端口映射，格式为：`主机(宿主)端口:容器端口`
* `-t`：为容器重新分配一个伪输入终端，通常与 -i 同时使用
* `--name="tmp_test"`：为容器指定一个名称
* `-v`：绑定一个卷,或者文件夹`主机(宿主)文件夹:容器文件夹`
* `--restart=always`：容器自动重启
* `-m`：设置容器使用内存最大值
* `--rm`：停止容器后删除该容器，测试或临时使用时很方便

> 其他详细命令可参考[官方文档](http://docs.docker.com/engine/reference/commandline/run/)

# Dockerfile

### FROM

### ADD

### COPY

### WORKDIR

### ENV

### RUN

### CMD

### ENTRYPOINT

### VOLUM


> 其他详细命令可参考[官方文档](https://docs.docker.com/engine/reference/builder/)，
 也可以参考[他人整理的文档](https://www.jianshu.com/p/e37225134adf)


 # Registry

 Docker hub： https://hub.docker.com

DockerHub 是一个由 Docker 公司运行和管理的基于云的存储库。

个人账号，免费的可以创建一个私有存储库，

自己搭建私有仓库：https://docker.cigdata.cn:5000

查看镜像： https://docker.cigdata.cn:5000/v2/_catalog

查看镜像版本： https://docker.cigdata.cn:5000/v2/test_jdy/tags/list

登录私有仓库：`docker login docker.cigdata.cn:5000`

登出：`docker logout docker.cigdata.cn:5000`

拉取镜像：`docker pull docker.cigdata.cn:5000/centos:6`

提交镜像：

先打标记，`docker image tag centos:6 docker.cigdata.cn:5000/centos:6`

再push，`docker push docker.cigdata.cn:5000/centos:6`

搭建私服参考文档： https://docs.docker.com/registry/deploying/