# 命令行说明中的括号含义
1. `[]`：里面内容可写可不写
   
2. `{}`：必须在{}中选择一个写

3. `<>`：表示必填


命令行语法字符在命令行语法中，某些字符与格式有着特殊的意义与含义。

## 方括号[]

方括号 ( [ ] ) 表示里面的元素（参数、值或信息）是可选的。 您可以选择一个或多个条目，也可以不选。 不要将方括号本身也输入到命令行中。

> 示例：`[global options]、[source arguments]、[destination arguments]`

## 尖括号<>

尖括号 ( < > ) 表示里面的元素(参数、值或信息）是必需的。 您需要用相应的信息来替换尖括号里面的文本。 不要将尖括号本身也输入到命令行中。

> 示例：`-f <file name>、-printer <printer name>、-repeat <months> <days> <hours> <minutes>、date access <mm/dd/yyyy>`

## 斜体

斜体文本表示您必须通过相应的值提供的信息。 它是一个要用值来替换的选项或参数。

>    示例：`-sessionpassword `*session password*`、-f <file name>、-printer <printer name>`

