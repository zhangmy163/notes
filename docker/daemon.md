docker安装后默认没有daemon.json这个配置文件，需要进行手动创建。配置文件的默认路径：/etc/docker/daemon.json

一般情况，配置文件 daemon.json中配置的项目参数，在启动参数中同样适用，有些可能不一样（具体可以查看官方文档），但需要注意的一点，配置文件中如果已经有某个配置项，则无法在启动参数中增加，会出现冲突的错误。

>如果在daemon.json文件中进行配置，需要docker版本高于1.12.6(在这个版本上不生效，1.13.1以上是生效的)

官方的配置地址：https://docs.docker.com/engine/reference/commandline/dockerd/#/configuration-reloading。

官方的配置地址：https://docs.docker.com/engine/reference/commandline/dockerd/#options

官方的配置地址：https://docs.docker.com/engine/reference/commandline/dockerd/#/linux-configuration-file

### 如何配置 registry 私库相关的参数

涉及以下两个参数

```
"insecure-registries": [],  #这个私库的服务地址
"registry-mirrors": [],    #私库加速器
```

### 创建并修改完daemon.json文件后，需要让这个文件生效


`sudo systemctl daemon-reload`

或者重启docker服务

`sudo systemctl restartdocker.service`