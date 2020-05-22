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

如果调试时想不按ENTRYPOINT设置的启动，则可以在启动容器时增加参数

```
$ docker run -it --entrypoint /bin/bash example/redis

或两个如何将更多参数传递给该ENTRYPOINT的示例：
$ docker run -it --entrypoint /bin/bash example/redis -c ls -l
$ docker run -it --entrypoint /usr/bin/redis-cli example/redis --help

您可以通过传递空字符串来重置容器入口点，例如：
$ docker run -it --entrypoint="" mysql bash
```

### VOLUM

### EXPOSE

功能为暴漏容器运行时的监听端口给外部，但是EXPOSE并不会使容器访问主机的端口，如果想使得容器与主机的端口有映射关系，必须在容器启动的时候加上 -P参数。

-P：大写P为自动映射，会将EXPOSE暴露出来的端口随机映射到宿主机的端口上，如果没有暴露端口，就不会有映射。

-p：小写p为手动映射，需要自己指定宿主机的端口和容器的端口，形式为：
-p 宿主机端口：容器端口

参考[样例](dockerfile_demo.md)

> 其他详细命令可参考[官方文档](https://docs.docker.com/engine/reference/builder/)，
 也可以参考[他人整理的文档](https://www.jianshu.com/p/e37225134adf)


 # Registry

Docker hub： https://hub.docker.com

DockerHub 是一个由 Docker 公司运行和管理的基于云的存储库。

个人账号，免费的可以创建一个私有存储库，执行`docker login`登录

自己搭建私有仓库：https://自己的域名:5000

查看镜像： https://自己的域名:5000/v2/_catalog

查看镜像版本： https://自己的域名:5000/v2/test_jdy/tags/list

登录私有仓库：`docker login 自己的域名:5000`

登出：`docker logout 自己的域名:5000`

拉取镜像：`docker pull 自己的域名:5000/centos:6`

提交镜像：

先打标记，`docker image tag centos:6 自己的域名:5000/centos:6`

再push，`docker push 自己的域名:5000/centos:6`

### 私服搭建过程

配置有身份验证的docker私服

前提把颁发的证书放在/etc/keys下（keys权限700）

```
$ cd ~
$ mkdir auth
$ docker run \
  --entrypoint htpasswd \
  registry:2 -Bbn <username> <password> > auth/htpasswd
$ docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  -v "$(pwd)"/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  -v /etc/keys:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/server.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/server.key \
  registry:2
```

外网浏览器访问：https://自己的域名:5000/v2/_catalog ， 账号：xxx，密码：xxx

查看某个镜像的版本：https://自己的域名:5000/v2/ubuntu/tags/list

本机登录私服并操作：

本机不能直接docker login 域名，如果想域名登录，可以在hosts文件配置该域名

```
$ docker login 127.0.0.1:5000
$ xxx_username
$ xxx_password
$ docker image tag centos:6 127.0.0.1:5000/centos:6
$ docker push 127.0.0.1:5000/centos:6
```

外部服务器登录私服并操作：

```
$ docker login 自己的域名:5000
$ docker pull 自己的域名:5000/centos:6
$ docker image tag ubuntu:latest 自己的域名:5000/ubuntu:14
$ docker push 自己的域名:5000/ubuntu:14
```

### 删除私服镜像

Registry上传的时候如果断网，就会出现镜像无法重新上传的bug，为了解决此问题，只能删除私服里的镜像了

删除镜像其实有个讨巧的方法，总共两步即可

第一步删除repo
docker exec <容器名> rm -rf /var/lib/registry/docker/registry/v2/repositories/<镜像名>

第二部清楚掉blob
docker exec registry bin/registry garbage-collect /etc/docker/registry/config.yml

如此就可继续重新上传镜像了

以上步骤是删除整个私服镜像的，如果删除某个版本有些复杂，后续整理。

搭建私服参考文档： https://docs.docker.com/registry/deploying/