# Mysql升级手册
## 一、首先得备份数据库
通过 mysqldump 备份当前数据库，命令如下：

`mysqldump -uxxxx -p --events --ignore-table=mysql.events --all-databases > /root/alldb.sql`
# 二、查看并记录mysql相关运行参数
```
[root@xiaotieren1 ~]# ps -ef | grep mysql
root     4155    1  0  2017 ?       00:00:00 /bin/sh /usr/local/mysql/bin/mysqld_safe --datadir=/data/mysql --pid-file=/data/mysql/mysql.pid
mysql    4951  4155 0  2017 ?       10:45:52 /usr/local/mysql/bin/mysqld --basedir=/usr/local/mysql --datadir=/data/mysql --plugin-dir=/usr/local/mysql/lib/plugin --user=mysql --log-error=/data/mysql/mysql-error.log --open-files-limit=65535 --pid-file=/data/mysql/mysql.pid --socket=/tmp/mysql.sock --port=3306
root    32655 32635  0 10:43 pts/0    00:00:00 grep mysql
```
登录数据库查看显示数据库版本。
```
[root@xiaotieren1 ~]# mysql -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5998935
Server version: 5.7.14-log MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> exit
Bye
```

# 三、把下载下来的最新版免编译版本数据库解压。

下载最新版数据库 wget http://172.22.3.222:8000/package/mysql/5_7_28/mysql-5.7.28-linux-glibc2.12-x86_64.tar.gz

官网：https://dev.mysql.com/downloads/mysql/

解压缩压缩包：
```
[root@xiaotieren1 soft]# tar vxzf mysql-5.7.28-linux-glibc2.12-x86_64.tar.gz  
mysql-5.7.28-linux-glibc2.12-x86_64/bin/myisam_ftdump
mysql-5.7.28-linux-glibc2.12-x86_64/bin/myisamchk
mysql-5.7.28-linux-glibc2.12-x86_64/bin/myisamlog
mysql-5.7.28-linux-glibc2.12-x86_64/bin/myisampack
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_client_test_embedded
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_config_editor
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_embedded
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_install_db
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_plugin
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_secure_installation
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_ssl_rsa_setup
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_tzinfo_to_sql
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysql_upgrade
mysql-5.7.28-linux-glibc2.12-x86_64/bin/mysqladmin
………………
………………
………………
```
# 四、备份MySQL配置文件，以防万一
```
[root@xiaotieren1 soft]# cp /etc/my.cnf /etc/my.cnf.bak
```
# 五、把刚刚解压的最新版MySQL文件夹link到/usr/local下，并命名为MySQLxxxx（版本号）
```
[root@xiaotieren1 soft]# ln -s /soft/mysql-5.7.28-linux-glibc2.12-x86_64 /usr/local/mysql5722
把MySQL的配置文件复制到MySQL5722下，并修改basedir参数
[root@xiaotieren1 soft]# cp /etc/my.cnf /usr/local/mysql5722/
[root@xiaotieren1 soft]# cd /usr/local/mysql5722/
[root@xiaotieren1 mysql5722]# pwd
/usr/local/mysql5722

Vim  /usr/local/mysql5722/my.cnf

basedir = /usr/local/mysql5722 #安装目录
datadir=/var/lib/mysql	#数据库目录
```

**注：**
	show global variables like "%datadir%";


# 六、修改innodb_fast_shutdown=0，并检查。
```
[root@xiaotieren1 mysql5722]# mysql -pxxxx
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5999137
Server version: 5.7.14-log MySQL Community Server (GPL)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> set global innodb_fast_shutdown=0;


Query OK, 0 rows affected (0.00 sec)

mysql> show global variables like 'innodb_fast_shutdown';
+----------------------+-------+
| Variable_name       | Value |
+----------------------+-------+
| innodb_fast_shutdown | 0    |
+----------------------+-------+
1 row in set (0.03 sec)

mysql> exit
Bye
```
# 七、使用mysqladmin关闭MySQL
```
[root@xiaotieren1 mysql5722]# mysqladmin -pxxxx shutdown
mysqladmin: [Warning] Using a password on the command line interface can be insecure.
[root@xiaotieren1 mysql5722]# ps -ef | grep mysql
root    32727 32635  0 10:59 pts/0    00:00:00 grep mysql
```
使用新修改的my.cnf启动MySQL
```
[root@xiaotieren1 mysql5722]# bin/mysqld_safe --defaults-file=my.cnf  --socket=/tmp/mysql.sock &
[1] 32735
[root@xiaotieren1 mysql5722]# 2018-06-29T03:00:40.489471Z mysqld_safe Logging to '/data/mysql/mysql-error.log'.
2018-06-29T03:00:40.531231Z mysqld_safe Starting mysqld daemon with databases from /data/mysql

[root@xiaotieren1 mysql5722]# ps -ef | grep mysql
mysql    1075 32735  4 11:00 pts/0    00:00:00 /usr/local/mysql5722/bin/mysqld --defaults-file=my.cnf --basedir=/usr/local/mysql5722 --datadir=/data/mysql --plugin-dir=/usr/local/mysql5722/lib/plugin --user=mysql --log-error=/data/mysql/mysql-error.log --open-files-limit=65535 --pid-file=/data/mysql/mysql.pid --socket=/tmp/mysql.sock --port=3306
root     1111 32635  0 11:00 pts/0   00:00:00 grep mysql
root    32735 32635  0 11:00 pts/0    00:00:00 /bin/sh bin/mysqld_safe --defaults-file=my.cnf --socket=/tmp/mysql.sock
```
进入mysql查看版本
```
[root@xiaotieren1 mysql5722]# mysql -pxxxx
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 5.7.22-log MySQL Community Server (GPL)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> exit
Bye
```
进行MySQL 升级             
```
[root@xiaotieren1 mysql5722]# bin/mysql_upgrade -uroot -p --socket=/tmp/mysql.sock
Enter password: 
Checking if update is needed.
Checking server version.
Running queries to upgrade MySQL server.
Checking system database.
mysql.columns_priv                            OK
mysql.db                                    OK
mysql.engine_cost                             OK
mysql.event                                  OK
mysql.func                                  OK
mysql.general_log                             OK
mysql.gtid_executed                           OK
mysql.help_category                           OK
mysql.help_keyword                            OK
mysql.help_relation                           OK
mysql.help_topic                             OK
mysql.innodb_index_stats                       OK
mysql.innodb_table_stats                       OK
mysql.ndb_binlog_index                        OK
mysql.plugin                                 OK
mysql.proc                                  OK
mysql.procs_priv                             OK
mysql.proxies_priv                            OK
mysql.server_cost                             OK
mysql.servers                                OK
mysql.slave_master_info                        OK
mysql.slave_relay_log_info                     OK
mysql.slave_worker_info                        OK
mysql.slow_log                               OK
mysql.tables_priv                             OK
mysql.time_zone                              OK
mysql.time_zone_leap_second                    OK
mysql.time_zone_name                          OK
mysql.time_zone_transition                     OK
mysql.time_zone_transition_type                 OK
mysql.user                                  OK
The sys schema is already up to date (version 1.5.1).
Checking databases.
sys.sys_config                               OK
xtrmh.t_campphoto_info                        OK
xtrmh.t_campvideo_info                        OK
xtrmh.t_competitionphoto_info                  OK
xtrmh.t_competitionvideo_info                  OK
xtrmh.t_content_info                          OK
xtrmh.t_custom_info                           OK
xtrmh.t_member                               OK
xtrmh.t_member_player                         OK
xtrmh.t_menu_info                             OK
xtrmh.t_organization_info                      OK
xtrmh.t_player_camp                           OK
xtrmh.t_programa_info                         OK
xtrmh.t_role_info                             OK
xtrmh.t_role_menu                             OK
xtrmh.t_site_group                            OK
xtrmh.t_site_playing                          OK
xtrmh.t_slide_info                            OK
xtrmh.t_sponsor_info                          OK
xtrmh.t_summer_camp                           OK
xtrmh.t_user_info                             OK
xtrmh.t_user_organization                      OK
xtrmh.t_user_role                             OK
xtrmh2.t_campphoto_info                        OK
xtrmh2.t_campvideo_info                        OK
xtrmh2.t_competitionphoto_info                 OK
xtrmh2.t_competitionvideo_info                 OK
xtrmh2.t_content_info                         OK
xtrmh2.t_custom_info                          OK
xtrmh2.t_menu_info                            OK
xtrmh2.t_organization_info                     OK
xtrmh2.t_programa_info                        OK
xtrmh2.t_role_info                            OK
xtrmh2.t_role_menu                            OK
xtrmh2.t_site_group                           OK
xtrmh2.t_site_playing                         OK
xtrmh2.t_slide_info                           OK
xtrmh2.t_sponsor_info                         OK
xtrmh2.t_user_info                            OK
xtrmh2.t_user_organization                     OK
xtrmh2.t_user_role                            OK
xtrmh3.t_campphoto_info                        OK
xtrmh3.t_campvideo_info                        OK
xtrmh3.t_competitionphoto_info                 OK
xtrmh3.t_competitionvideo_info                 OK
xtrmh3.t_content_info                         OK
xtrmh3.t_custom_info                          OK
xtrmh3.t_menu_info                            OK
xtrmh3.t_organization_info                     OK
xtrmh3.t_programa_info                        OK
xtrmh3.t_role_info                            OK
xtrmh3.t_role_menu                            OK
xtrmh3.t_site_group                           OK
xtrmh3.t_site_playing                         OK
xtrmh3.t_slide_info                           OK
xtrmh3.t_sponsor_info                         OK
xtrmh3.t_user_info                            OK
xtrmh3.t_user_organization                     OK
xtrmh3.t_user_role                            OK
Upgrade process completed successfully.
Checking if update is needed.
#出现声明提示表明升级成功。
```
关闭数据库
```
[root@xiaotieren1 mysql5722]# bin/mysqladmin -uroot -p shutdown --socket=/tmp/mysql.sock
Enter password: 
2018-06-29T03:03:11.982357Z mysqld_safe mysqld from pid file /data/mysql/mysql.pid ended
[1]+  Done                bin/mysqld_safe --defaults-file=my.cnf --socket=/tmp/mysql.sock
[root@xiaotieren1 mysql5722]# ps -ef | grep mysql
root     1140 32635  0 11:03 pts/0   00:00:00 grep mysql
```
把mysql5722文件夹内修改并验证可正常启动的my.cnf覆盖/etc/my.cnf
```
[root@xiaotieren1 mysql5722]# cp my.cnf /etc/my.cnf
cp: overwrite `/etc/my.cnf'? y
```
重新启动数据库
```
[root@xiaotieren1 mysql5722]# service mysql start
Starting MySQL.                                     [ OK  ]
[root@xiaotieren1 mysql5722]# mysql -pxxxx
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 5.7.22-log MySQL Community Server (GPL)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> \s
--------------
mysql  Ver 14.14 Distrib 5.7.14, for linux-glibc2.5 (x86_64) using  EditLine wrapper

Connection id: 12
Current database:
Current user: root@localhost
SSL: Not in use
Current pager: stdout
Using outfile: ''
Using delimiter: ;
Server version: 5.7.22-log MySQL Community Server (GPL)
Protocol version: 10
Connection: Localhost via UNIX socket
Server characterset: latin1
Db    characterset: latin1
Client characterset: utf8
Conn.  characterset: utf8
UNIX socket: /tmp/mysql.sock
Uptime: 11 sec

Threads: 11  Questions: 85 Slow queries: 0  Opens: 120 Flush tables: 1  Open tables: 18 Queries per second avg: 7.727
--------------

mysql> select version();
+------------+
| version()  |
+------------+
| 5.7.22-log |
+------------+
1 row in set (0.00 sec)

mysql> exit
Bye
[root@xiaotieren1 mysql5722]# ps -ef | grep mysql
root     1171    1  0 11:04 pts/0    00:00:00 /bin/sh /usr/local/mysql5722/bin/mysqld_safe --datadir=/data/mysql --pid-file=/data/mysql/mysql.pid
mysql    2707  1171  0 11:04 pts/0    00:00:00 /usr/local/mysql5722/bin/mysqld --basedir=/usr/local/mysql5722 --datadir=/data/mysql --plugin-dir=/usr/local/mysql5722/lib/plugin --user=mysql --log-error=/data/mysql/mysql-error.log --open-files-limit=65535 --pid-file=/data/mysql/mysql.pid --socket=/tmp/mysql.sock --port=3306
root     2756 32635  0 11:06 pts/0   00:00:00 grep mysql

[END] 2018/6/29 11:06:52
```