<div align="center">
  <h1 align="center">lzq</h3>
  <p align="center">A way to lazy quant. <p>
</div>

## 关于项目

本项目记录量化过程中学习的策略，使用到的工具等。项目使用akshare获取股票数据、mysql存储数据、backtrader用于回测。并提供了mysql的docker-compose.yml配置文件，便于直接部署。

---
## 如何使用

1. 克隆项目：

    ```bash
    git clone git@github.com:someu/lzq.git
    ```

2. 安装依赖，建议使用3.8版本的pyhton。

    ```bash
    pip install -r requirements.txt  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
    ```

3. 安装数据库，在docs/mysql目录下有mysql的docker-compose.yml的配置文件，提供了mysql的镜像和adminer作为数据库管理工具。（adminer访问docker启动的mysql时，需要注意数据库地址不是127.0.0.1）

    ```bash
    cd docs/mysql
    docker-compose up -d
    ```

4. 修改配置文件，复制一份example.config.ini为.config.ini文件，修改里面的数据库链接地址和其他配置参数。
    ```bash
    cp example.config.ini .config.ini
    vim .config.ini
    ```

5. 运行项目：

    ```bash
    # python run lzq.py command [...options]
    $ python lzq.py 
    NAME
        lzq.py - A way to lazy quant

    SYNOPSIS
        lzq.py COMMAND

    DESCRIPTION
        A way to lazy quant

    COMMANDS
        COMMAND is one of the following:

        download
          下载单个股票数据。period取值daily、weekly、monthly。adjust取值qfq、hfq或空

        downloadall
          下载所有数据：股票信息、股票历史行情

        list
          查看策略列表

        run
          运行策略
    ```

## 量化策略

- [x] [三均线策略](stragies/)
- [ ] 待续...

## 问题记录

1. `xlrd.biffh.XLRDError: Excel xlsx file; not supported`
    xlrd版本过高，使用`pip3 install xlrd==1.2.0`安装低版本的。

2. mysql创建的数据库编码错误。
    ```bash
    use stock;
    # 查看编码
    show variables like 'character_set_database';
    # 修改编码为utf8
    alter database stock CHARACTER SET utf8;
    ```