pre-receive

限制gitlab提交注释和分支名称

https://github.com/zhangmy163/custom_hooks/tree/master/gitlab

根据接收到的三个参数，再结合git的相关命令，来实现控制提交等。 oldrev=$(git rev-parse $1) newrev=$(git rev-parse $2) refname="$3"

文件放在/var/opt/gitlab/git-data/repositories/[devgit]/[demo.git]/custom_hooks/pre-receive

赋权sudo chown -R git:git xxxx/pre-receive

赋权sudo chmod +x xxxx/pre-receive


脚本里的一些git命令

`git rev-list $oldrev..$newrev`列出两个commit hash之间的所有hash   
`git cat-file commit $hash`展示该hash的提交信息   
`git cat-file commit $hash | sed '1,/^$/d'|sed '/^$/d'`简化提交信息，只展示commit的内容   

$oldrev为一串0时是新建分支   
$newrev为一串0时是删除分支