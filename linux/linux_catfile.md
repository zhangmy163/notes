```
$line=($(cat test.txt))
```

```
while read line命令从grep的输出中读取数据
  cat $mappingfilename | while read line;
  do
    linearr=($line);              #把line赋给linearr数组，前提是line的值是用tab分割
    interfaceno=${linearr[0]};
    echo $line
    echo $interfaceno
  done
```

```
IFS=$'\n'    #避免文件有空格

for $f in `ls`
do
  echo $f
done
```
