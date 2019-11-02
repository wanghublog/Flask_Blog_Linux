# Flask_Blog_Linux
服务器端的flask_blog

1.安装Flask-Bcrypt失败的问题# Bcrypt 哈希算法

  No package 'libffi' found
  系统没有安装必须的开发包的缘故。一般多见于Debian系系统.
  解决方案:
  apt-cache search libffi | grep dev
  apt-get install libffi-dev

  ...
  还是没有相关依赖包,应该只用安装一个就可以了
  apt-get install python3-dev


2.pillow 安装问题
  $sudo apt-get install python-dev python-setuptools
  $ sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
  $ sudo pip install pillow


3.python3中引用HTMLParser后，运行程序出现如图所示的错误

 ModuleNotFoundError: No module named 'markupbase'
 下载的_markupbase.py文件复制到python安装路径下的C:\Users\admin\AppData\Local\Programs\Python\Python36-32\Lib\site-packages（路径替换成自己的）
 更改步骤4中复制的.py文件的名称为：markupbase.py

4.MYSQL:默认引擎原因
  查询引擎：show variables like '%storage_engine%';//show create table table_name;
  设置sql 默认引擎：# vi /etc/mysql/mysql.conf.d/mysqld.cnf    default-storage-engine=InnoDB
                      单表; alter table xxx engine MyISAM
  端口权限问题见：http://www.chenxm.cc/article/482.html

5，pillow 没有安装相关字体：
   $ sudo apt install ttf-mscorefonts-installer # 安装
   $ sudo fc-cache # 生效
   $ fc-match Arial # 查看Arial
