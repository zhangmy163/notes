> https://kubernetes.io/zh/docs/tutorials/kubernetes-basics/

>http://docs.kubernetes.org.cn/230.html

# 安装

按文档 https://blog.51cto.com/3241766/2405624

安装K8s dashboard https://blog.csdn.net/zz_aiytag/article/details/103874977/

遇到的问题:

init时：[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get http://localhost:10248/healthz: dial tcp 127.0.0.1:10248: connect: connection refused.

解决：yum update systemd

# [k8s介绍](k8s_readme.md)

# [常用命令](k8s_command.md)