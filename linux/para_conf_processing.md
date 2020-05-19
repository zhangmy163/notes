# 参数处理

1.对脚本传参形式为-a 123 -b 234 -c ddd的处理

```
#!/bin/bash
while getopts ":a:b:c:" opt
do
   case $opt in
        a)
        echo "参数a的值$OPTARG"
        ;;
        b) echo "参数b的值$OPTARG"
        ;;
        c) echo "参数c的值$OPTARG"
        ;;
        ?) echo "未知参数"
           exit 1;;
   esac
done
```



2.对脚本传参形式为-m 20191216 -c 20101 20202 20303 -s 30101 30202 -p 40401 40402 40403的处理

**注意**：xxx为数字，脚本中grep -q '^[1-9]'有处理，如果参数有其他情况，请修改

```
m=c=s=p=0
mp=()
cp=()
sp=()
pp=()

#处理参数,metadata存入mp[*],排期存入cp[*],媒体存入sp[*],展示位置存入pp[*]
until [ $# -eq 0 ]
do
    case "$1" in
        -h|--help) echo "-h or --help";
        exit 0;;
        -m|--metadata)
                while(`echo $2 |grep -q '^[1-9]'`)
                do
                mp[$m]=$2
                let m++
                shift
                done
                ;;
        -c|--campaign)
                while(`echo $2 |grep -q '^[1-9]'`)
                do
                cp[$c]=$2
                let c++
                shift
                done
                ;;
        -s|--site)
                while(`echo $2 |grep -q '^[1-9]'`)
                do
                sp[$s]=$2
                let s++
                shift
                done
                ;;
        -p|--placement)
                while(`echo $2 |grep -q '^[1-9]'`)
                do
                pp[$p]=$2
                let p++
                shift
                done
                ;;
        *) shift;;
    esac
done
echo "metadata目录 ${mp[*]}"
echo "排期变化id ${cp[*]}"
echo "媒体变化id ${sp[*]}"
echo "展示位置变化id ${pp[*]}"
```

# 配置文件处理

例子：

pipeline.conf

```
[nlp]
branch=nlp-1
hash=nlp123

[spark]
branch=spark-1
hash=spark123

[release_repo]
branch=release_repo-1
hash=release_repo123
```

读取：

```
$ source dealconf.sh pipeline.conf
[info]:iniSections size:-3- eles:-nlp spark release_repo-   #下面的脚本注释掉了[info]的输出，如果需要可以打开
$ echo ${iniSections[@]}
nlp spark release_repo

$ source dealconf.sh pipeline.conf nlp
[info]:iniOptions size:-2- eles:-branch=nlp-1 hash=nlp123-
$ echo ${iniOptions[@]}
branch=nlp-1 hash=nlp123

$ source dealconf.sh pipeline.conf nlp branch
[info]:iniValue value:-nlp-1-
$ echo ${iniValue}
nlp-1
```

写入：

```
$ source dealconf.sh -w pipeline.conf testItem testOption testValue   # shell脚本后跟的第一个参数要是-w，之后跟文件
[success] add [pipeline.conf][testItem][testOption][testValue]       #只能一条一条添加
$ cat pipeline.conf
...
[testItem]
testOption = testValue
$ source dealconf.sh -w pipeline.conf testItem  testOption2 testValue2
[success] add [pipeline.conf][testItem][testOption2][testValue2]
$ cat pipeline.conf
...
[testItem]
testOption2 = testValue2
testOption = testValue
$ source dealconf.sh -w pipeline.conf testItem  testOption2 testValue4   #重复的Option会更新
[success] update [pipeline.conf][testItem][testOption2][testValue4]
```

脚本代码：

**注意：** 目前脚本取变量时是模糊匹配，如果要精准，需将2处修改`/^${option}.*=`为`/^${option}=`

dealconf.sh

```
#该脚本必须用 source 命令 而且结果获取为${var}获取，不是return 如：source readIni.sh 否则变量无法外传
# dealIni.sh iniFile section option
# read
# param : iniFile section option    return value --- a str    use: ${iniValue}
# param : iniFile section           return options (element: option = value) --- a str[]   use: arr_length=${#iniOptions[*]}}  element=${iniOptions[0]}
# param : iniFile                   returm sections (element: section ) --- a str[]   use: arr_length=${#iniSections[*]}}  element=${iniSections[0]}
# write
#param : -w iniFile section option value  add new element：section option    result:if not --->creat ,have--->update,exist--->do nothing
#option ,value can not be null
 
#params
iniFile=$1
section=$2
option=$3
#sun
mode="iniR"
echo $@ | grep "\-w" >/dev/null&&mode="iniW"
if [ "$#" = "5" ]&&[ "$mode" = "iniW" ];then
   iniFile=$2
   section=$3
   option=$4
   value=$5
   #echo $iniFile $section $option $value
fi
#resullt
iniValue='default'
iniOptions=()
iniSections=()
 
function checkFile()
{
    if [ "${iniFile}" = ""  ] || [ ! -f ${iniFile} ];then
        echo "[error]:file --${iniFile}-- not exist!"
    fi
}
 
function readInIfile()
{
    if [ "${section}" = "" ];then
        #通过如下两条命令可以解析成一个数组
        allSections=$(awk -F '[][]' '/\[.*]/{print $2}' ${iniFile})
        iniSections=(${allSections// /})
#        echo "[info]:iniSections size:-${#iniSections[@]}- eles:-${iniSections[@]}- "
    elif [ "${section}" != "" ] && [ "${option}" = "" ];then
        #判断section是否存在
        allSections=$(awk -F '[][]' '/\[.*]/{print $2}' ${iniFile})
        echo $allSections|grep ${section} > /dev/null
        if [ "$?" = "1" ];then
            echo "[error]:section --${section}-- not exist!"
            return 0
        fi
        #正式获取options
        #a=(获取匹配到的section之后部分|去除第一行|去除空行|去除每一行行首行尾空格|将行内空格变为@G@(后面分割时为数组时，空格会导致误拆))
        a=$(awk "/\[${section}\]/{a=1}a==1"  ${iniFile}|sed -e'1d' -e '/^$/d'  -e 's/[ \t]*$//g' -e 's/^[ \t]*//g' -e 's/[ ]/@G@/g' -e '/\[/,$d' )
        b=(${a})
        for i in ${b[@]};do
          #剔除非法字符，转换@G@为空格并添加到数组尾
          if [ -n "${i}" ]||[ "${i}" i!= "@S@" ];then
              iniOptions[${#iniOptions[@]}]=${i//@G@/ }
          fi
        done
#        echo "[info]:iniOptions size:-${#iniOptions[@]}- eles:-${iniOptions[@]}-"
    elif [ "${section}" != "" ] && [ "${option}" != "" ];then
 
       # iniValue=`awk -F '=' '/\['${section}'\]/{a=1}a==1&&$1~/'${option}'/{print $2;exit}' $iniFile|sed -e 's/^[ \t]*//g' -e 's/[ \t]*$//g'`
        iniValue=`awk -F '=' "/\[${section}\]/{a=1}a==1" ${iniFile}|sed -e '1d' -e '/^$/d' -e '/^\[.*\]/,$d' -e "/^${option}.*=.*/!d" -e "s/^${option}.*= *//"`
#        echo "[info]:iniValue value:-${iniValue}-"
        fi
}
 
function writeInifile()
{
    #检查文件
    checkFile
    allSections=$(awk -F '[][]' '/\[.*]/{print $2}' ${iniFile})
    iniSections=(${allSections// /})
    #判断是否要新建section
    sectionFlag="0"
    for temp in ${iniSections[@]};do
        if [ "${temp}" = "${section}" ];then
            sectionFlag="1"
            break
        fi
    done
 
    if [ "$sectionFlag" = "0" ];then
        echo "[${section}]" >>${iniFile}
    fi
    #加入或更新value
    awk "/\[${section}\]/{a=1}a==1" ${iniFile}|sed -e '1d' -e '/^$/d'  -e 's/[ \t]*$//g' -e 's/^[ \t]*//g' -e '/\[/,$d'|grep "${option}.\?=">/dev/null
    if [ "$?" = "0" ];then
        #更新
        #找到制定section行号码
        sectionNum=$(sed -n -e "/\[${section}\]/=" ${iniFile})
        sed -i "${sectionNum},/^\[.*\]/s/\(${option}.\?=\).*/\1 ${value}/g" ${iniFile}
        echo "[success] update [$iniFile][$section][$option][$value]"
    else
        #新增
        #echo sed -i "/^\[${section}\]/a\\${option}=${value}" ${iniFile}
        sed -i "/^\[${section}\]/a\\${option} = ${value}" ${iniFile}
        echo "[success] add [$iniFile][$section][$option][$value]"
    fi
}
 
#main
if [ "${mode}" = "iniR" ];then
    checkFile
    readInIfile
elif [ "${mode}" = "iniW" ];then
    writeInifile
fi

```