# 判断远程服务器是否有文件

```
ssh -i  $keyfile -p $port  $username@$ruip  [ -f /release/media/deploy/deploy.sh ]
if [ $? != 0 ];then
  echo "环境部署脚本不存在，scp初始化"
  scp -i $keyfile -P $port $deployfile  $username@$ruip:$deployfile
fi
```