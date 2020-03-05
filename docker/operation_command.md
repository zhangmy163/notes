# 查看容器的详细信息

`docker inspect <container_name>`

# 以其他用户运行命令

`docker exec -it -u root <container_name> <command>`

# 查看容器的完整命令

`docker ps -a --no-trunc`

# 查看容器运行时的run参数

> https://blog.csdn.net/qq_35462323/article/details/101607062

`docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike <container_name>`

# 把容器打包成镜像

1.停止容器

`docker stop <container_name>`

2.commit该docker容器

`docker commit <container_name> <new_image:tag>`

# 给其他用户增加docker运行权限

```
sudo usermod -a -G docker ec2-user

newgrp docker
```


# 给运行中的容器追加端口映射

> https://www.cnblogs.com/shijf/p/10386193.html

方法一、删除原有容器，重新创建新容器

方法二、修改容器配置文件，重启docker服务

`/var/lib/docker/containers/[hash_of_the_container]/hostconfig.json`

方法三、利用容器重新构建镜像，再启动一个新的

# 给运行中的容器追加Volume

> https://www.cnblogs.com/rwxwsblog/p/5437478.html

# docker update

`docker update`可以更改一些运行中容器的参数

https://docs.docker.com/engine/reference/commandline/update/
