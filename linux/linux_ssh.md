# 免密ssh连接

`ssh-keygen -t rsa -C "your_email@example.com"`

id_rsa : 生成的私钥文件  
id_rsa.pub ： 生成的公钥文件   
know_hosts : 已知的主机公钥清单   
　如果希望ssh公钥生效需满足至少下面两个条件：   
　　　　　1) .ssh目录的权限**必须是700**   
　　　　　2) .ssh/authorized_keys文件权限**必须是600**  

从A服务器要ssh或者scp到1B服务，则需要把A服务器的公钥内容粘贴到B服务器~/.ssh/authorized_keys文件里

也可以在A服务器执行`ssh-copy-id -i ~/.ssh/id_rsa.pub user@ip`，则会把A公钥自动发到B服务器的~/.ssh/authorized_keys文件里

`ssh-copy-id -i ~/.ssh/id_rsa.pub '-p port user@ip'` 如果使用其他端口，则需要单引号引起来

# 判断远程服务器是否有文件

```
ssh -i  $keyfile -p $port  $username@$ruip  [ -f /release/media/deploy/deploy.sh ]
if [ $? != 0 ];then
  echo "环境部署脚本不存在，scp初始化"
  scp -i $keyfile -P $port $deployfile  $username@$ruip:$deployfile
fi
```