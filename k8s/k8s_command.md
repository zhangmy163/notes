# 对象

nginx-deployment.yaml
```
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```
使用上述.yaml文件创建Deployment，是通过在kubectl中使用kubectl create命令来实现。将该.yaml文件作为参数传递。如下例子：
```
$ kubectl create -f docs/user-guide/nginx-deployment.yaml --record
```
其输出于此类似
```
deployment "nginx-deployment" created
```

# Namespace(命名空间)

## 创建

```
(1) 命令行直接创建
$ kubectl create namespace new-namespace

(2) 通过文件创建
$ cat my-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: new-namespace

$ kubectl create -f ./my-namespace.yaml
```
注意：命名空间名称满足正则表达式`[a-z0-9]([-a-z0-9]*[a-z0-9])?`,最大长度为63位

## 删除

```
$ kubectl delete namespaces new-namespace
```
注意：

删除一个namespace会自动删除所有属于该namespace的资源。

default和kube-system命名空间不可删除。

PersistentVolumes是不属于任何namespace的，但PersistentVolumeClaim是属于某个特定namespace的。

Events是否属于namespace取决于产生events的对象。

## 查看

```
$ kubectl get namespaces
NAME          STATUS    AGE
default       Active    1d
kube-system   Active    1d
```

## Setting the namespace for a request

要临时设置Request的Namespace，请使用--namespace 标志。

例如：
```
$ kubectl --namespace=<insert-namespace-name-here> run nginx --image=nginx
$ kubectl --namespace=<insert-namespace-name-here> get pods
```

## Setting the namespace preference

可以使用kubectl命令创建的Namespace可以永久保存在context中。
```
$ kubectl config set-context $(kubectl config current-context) --namespace=<insert-namespace-name-here>
# Validate it
$ kubectl config view | grep namespace:
```

## 环境的清理

通过删除名字空间即可完成环境的清理：

```
kubectl delete namespace quota-pod-example
```

## [对于集群管理员要掌握](http://docs.kubernetes.org.cn/749.html#i-3)

## [对于应用开发这要掌握](http://docs.kubernetes.org.cn/749.html#i-4)