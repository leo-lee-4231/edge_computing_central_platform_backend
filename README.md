# edge_computing_central_platform_backend

The back end for Edge Computing Central Platform.

### 使用说明

* 测试环境：操作系统为ubuntu desktop 16.04.6，python版本为3.5.6

* 安装python依赖包，执行如下命令

  ```shell
  $ pip install -r 03.数据库操作/src/requirements.txt
  ```

* 数据库设置

  * 本项目使用mysql数据库
 
  * 通过配置环境变量来设置数据库连接信息：`DATABASE_HOST`，`DATABASE_PORT`，`DATABASE_USER`，`DATABASE_PASS`，`DATABASE_DATABASE`
  
  * 生产环境使用`platform`数据库，开发环境使用`platform_dev`数据库

* 必要设置的环境参数

  ```shell
  export FLASK_APP=flasky.py
  export DATABASE_USER=<你的数据库用户>
  export DATABASE_PASS=<你的数据库密码>
  ```
  
* 运行前首先部署数据库，创建book表，使用命令：

  ```shell
  /src$ flask deploy
  ```
  
* 改变服务端的运行状态，需要声明环境变量

  ```shell
  # 生产环境
  export FLASK_ENV=production
  # 开发环境
  export FLASK_ENV=development
  ```

* 服务端程序运行，运行如下命令，可选参数`-h`后接服务器ip地址，可选参数`-p`后接端口。（默认IP地址：127.0.0.1:80）

  ```shell
  /src$ flask run -h 0.0.0.0 -p 8089
  ```
