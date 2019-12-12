# 创建账号

`create user <username> identified by '<password>';`

# GRANT授权

`grant <permissions> on <datebase>.<table> to '<username>'@'<host>' identified by '<password>';`

  * permissions 要加的权限
  * datebase    指定数据库，*代表所有库
  * table       指定表，*代表所有表
  * username    指定要加权限的用户
  * host        指定该用户可以访问的ip范围，%代表所有（但是不包括localhost），localhost代表mysql服务器本机
  * password    用户的密码

**注意** ：赋权后记得使用命令`flush privileges;`生效权限。

权限可以分三种：

### 数据库/数据表/数据列权限

`alter`: 修改已存在的数据表(例如增加/删除列)和索引

`create`: 建立新的数据库或数据表

`delete`: 删除表的记录

`drop`: 删除数据表或数据库

`index`: 建立或删除索引

`insert`: 增加表的记录

`select`: 显示/搜索表的记录

`update`: 修改表中已存在的记录

### 全局管理MySQL用户权限

`file`: 在MySQL服务器上读写文件

`PROCESS`: 显示或杀死属于其它用户的服务线程

`RELOAD`: 重载访问控制表，刷新日志等

`SHUTDOWN`: 关闭MySQL服务


### 特别的权限

`ALL`: 允许做任何事(和root一样)

`USAGE`: 只允许登录--其它什么也不允许做

# 查看用户权限

`show grants for '<username>'@'localhost'`

`show grants for <username>;`

`show grants for '<username>'@'%'`

# 回收权限

`REVOKE <permissions> on <datebase>.<table> from '<username>'@'<host>';`