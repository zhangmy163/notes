# Kubernetes组件

> http://docs.kubernetes.org.cn/230.html

## Master组件

Master组件提供集群的管理控制中心。

Master组件可以在集群中任何节点上运行。但是为了简单起见，通常在一台VM/机器上启动所有Master组件，并且不会在此VM/机器上运行用户容器。

### kube-apiserver

kube-apiserver用于暴露Kubernetes API。任何的资源请求/调用操作都是通过kube-apiserver提供的接口进行。请参阅构建高可用群集。

### ETCD

etcd是Kubernetes提供默认的存储系统，保存所有集群数据，使用时需要为etcd数据提供备份计划。

### kube-controller-manager

kube-controller-manager运行管理控制器，它们是集群中处理常规任务的后台线程。逻辑上，每个控制器是一个单独的进程，但为了降低复杂性，它们都被编译成单个二进制文件，并在单个进程中运行。

这些控制器包括：

* 节点（Node）控制器。
* 副本（Replication）控制器：负责维护系统中每个副本中的pod。
* 端点（Endpoints）控制器：填充Endpoints对象（即连接Services＆Pods）。
* Service Account和Token控制器：为新的Namespace 创建默认帐户访问API Token。

### cloud-controller-manager

云控制器管理器负责与底层云提供商的平台交互。云控制器管理器是Kubernetes版本1.6中引入的，目前还是Alpha的功能。

云控制器管理器仅运行云提供商特定的（controller loops）控制器循环。可以通过将--cloud-provider flag设置为external启动kube-controller-manager ，来禁用控制器循环。

cloud-controller-manager 具体功能：

* 节点（Node）控制器
* 路由（Route）控制器
* Service控制器
* 卷（Volume）控制器

### kube-scheduler

kube-scheduler 监视新创建没有分配到Node的Pod，为Pod选择一个Node。

### 插件 addons

插件（addon）是实现集群pod和Services功能的 。Pod由Deployments，ReplicationController等进行管理。Namespace 插件对象是在kube-system Namespace中创建。