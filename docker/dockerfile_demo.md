# 基础镜像

### java:1.8-centos

Dockerfile
```
FROM centos:6

COPY ["java_soft","/usr/src/soft"]   #java_soft在Dockerfile的当前目录，里面存放java的相关安装包

RUN cd /usr/src/soft && tar -zxf jdk-8u181-linux-x64.tar.gz \
  && mv jdk1.8.0_181 /usr/local/ && rm -rf /usr/src/soft

ENV JAVA_HOME="/usr/local/jdk1.8.0_181" \
  CLASSPATH=".:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar" 
ENV  PATH="$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/lib"

```
`docker build -t java:1.8-centos -f build_java_basefile .`


### python:2.7.9-centos

Dockerfile
```
FROM centos:6

RUN yum -y install gcc gcc-c++ make sqlite-devel mysql-devel git zlib* unzip \
  install libffi-devel python-devel python-pip python-wheel openssl-devel libsasl2-devel openldap-devel

COPY ["py_soft","/usr/src/soft"]

RUN cd /usr/src/soft && tar -xzf Python-2.7.9.tgz && tar -xzf pip-19.3.1.tar.gz && unzip setuptools-41.6.0.zip \
  && mv /usr/bin/python  /usr/bin/python.bak && sed -i "s/python/python2.6/" /usr/bin/yum\
  && cd /usr/src/soft/Python-2.7.9 && ./configure && make && make install \
  && cd /usr/src/soft/setuptools-41.6.0 && python setup.py install \
  && cd /usr/src/soft/pip-19.3.1 && python setup.py install \
  && rm -rf /usr/src/soft

```
`docker build -t python:2.7.9-centos -f Dockerfile .`

### node:6.11.0-centos

Dockerfile
```
FROM centos:6

ARG NODE_VERSION="6.11.0"
COPY ["node_soft","/usr/src/soft"]

RUN cd /usr/src/soft && tar -zxf node-v${NODE_VERSION}-linux-x64.tar.gz \
  && mv node-v${NODE_VERSION}-linux-x64 /usr/local/node-v${NODE_VERSION} && rm -rf /usr/src/soft

ENV NODE_HOME="/usr/local/node-v${NODE_VERSION}" 
ENV  PATH="$PATH:$NODE_HOME/bin"

```
`docker build --build-arg NODE_VERSION=6.11.0 -t node:test-centos -f Dockerfile .`

### maven:3.3.9-centos

Dockerfile
```
FROM java:1.8-centos

COPY ["maven_soft","/usr/src/soft"]

RUN cd /usr/src/soft && tar -zxf apache-maven-3.3.9-bin.tar.gz \
  && mv apache-maven-3.3.9 /usr/local/ && mkdir -p /root/.m2  \
  && cp settings.xml /root/.m2/ &&  rm -rf /usr/src/soft

ENV MAVEN_HOME="/usr/local/apache-maven-3.3.9" \
    MAVEN_CONFIG="/root/.m2"
ENV  PATH="$PATH:$MAVEN_HOME/bin"

```
`docker build -t maven:3.3.9-centos -f build_maven_basefile .`


# 多阶段构建

### example1：

Dockerfile
```
FROM node:10.15.1-centos as frontend

COPY ["./src/main/resources/public","/deploy/frontend/public"]
#运行要使用npm install --unsafe-perm,因为node-sass的安装有问题
RUN  mv /deploy/frontend/public/main/node_modules /deploy/frontend/ \
   && cd /deploy/frontend/public/main \
   && npm install --unsafe-perm \
   && cp -r /deploy/frontend/node_modules /deploy/frontend/public/main/ \
   && npm run build \
   && rm -rf /deploy/frontend/node_modules

FROM maven:3.3.9-centos as backend
COPY ["./","/deploy/backend/jindouyun/"]
RUN rm -rf /deploy/backend/jindouyun/src/main/resources/public 

COPY --from=frontend /deploy/frontend/public /deploy/backend/jindouyun/src/main/resources/public
WORKDIR /deploy/backend/jindouyun/
RUN  mvn clean package -DskipTests=true -P jindouyun

FROM java:1.8-centos as run
RUN mkdir -p /release/jindouyun
WORKDIR /release/jindouyun
COPY --from=backend /deploy/backend/jindouyun/target/jindouyun-1.0-SNAPSHOT.jar /release/jindouyun/jindouyun-1.0-SNAPSHOT.jar
COPY ["start.sh","/release/jindouyun/"]
RUN chmod +x /release/jindouyun/start.sh
ENTRYPOINT ["/release/jindouyun/start.sh"]
CMD ["dev"]

```
创建镜像

`docker build --target run -t run_jdy:$hashnum -f Dockerfile .`

运行容器

`docker run -d --name run_jdy -p 9521:9521 -t docker.cigdata.cn:5000/run_jdy:$hashnum $envtype $hostip`

### example2

Dockerfile
```
FROM node:6.11.0-centos as frontend
RUN yum -y install git
COPY ["./superset/assets","/deploy/frontend/assets"]
RUN cd /deploy/frontend/assets && npm install && npm run prod

FROM python:2.7.9-centos as backend
COPY ["./","/deploy/backend/media/"]
RUN rm -rf /deploy/backend/media/superset/assets/dist && pip install numpy==1.14.2

COPY --from=frontend /deploy/frontend/assets/dist /deploy/backend/media/superset/assets/dist

RUN cd /deploy/backend/media/ && python setup.py clean --all install

FROM python:2.7.9-centos as run
ARG PACKAGE_NAME="superset-0.18.5-py2.7.egg"
RUN mkdir -p /release/jindouyun
COPY --from=backend /deploy/backend/media/dist/${PACKAGE_NAME} /release/media/${PACKAGE_NAME}
WORKDIR /release/media
RUN pip install mysql-python && pip install numpy==1.14.2 && easy_install ${PACKAGE_NAME}
COPY ["start.sh","/release/media/"]
RUN chmod +x /release/media/start.sh
ENTRYPOINT ["/release/media/start.sh"]
CMD ["dev"]

```
创建镜像

`docker build --target run -t run_media:$hashnum -f Dockerfile .`

运行容器

`docker run -d --name run_media -p 8088:8088 -t docker.cigdata.cn:5000/run_media:$hashnum $envtype`

