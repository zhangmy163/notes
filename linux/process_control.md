# if判断

```
if condition1
then
  command1
  ...
elif condition2
then
  command2 
  ... 
else
  command3
  ...
fi
```


# for循环

```
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done
```

# while循环

```
while condition
do
    command
done
```

# until循环

```
until condition
do
    command
done
```

# 跳出循环

`break`

break命令允许跳出所有循环（终止执行后面的所有循环）。

`continue`

continue命令与break命令类似，只有一点差别，它不会跳出所有循环，仅仅跳出当前循环。

# case

```
case 值 in
模式1)
    command1
    command2
    ...
    commandN
    ;;
模式2）
    command1
    command2
    ...
    commandN
    ;;
esac
```


