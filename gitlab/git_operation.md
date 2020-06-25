`git rev-list $oldrev..$newrev`列出两个commit hash之间的所有hash   
`git cat-file commit $hash`展示该hash的提交信息   
`git cat-file commit $hash | sed '1,/^$/d'|sed '/^$/d'`简化提交信息，只展示commit的内容    
`git diff --name-only $oldrev $newrev`列出两次提交之间的变换文件
