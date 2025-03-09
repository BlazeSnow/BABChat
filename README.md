# BABChat

## 使用```Docker```运行

1. 安装```Docker```：<https://www.docker.com/>
2. 复制本仓库的```compose.yml```和```config_example.toml```文件到空位置，如```C:\BABChat\```
3. 根据```config_example.toml```的内容，新建并编辑```config.toml```
4. 拉取镜像：```docker compose pull```
5. 运行容器：```docker compose up```

## 使用```Python```运行

1. 安装```Python```：<https://www.python.org/>
2. 安装```Git```：<https://git-scm.com/>
3. 找到一个空位置：```cd C:\```
4. 克隆此仓库：```git clone https://github.com/BABChat/BABChat```
5. 进入```BABChat```文件夹：```cd BABChat```
6. 安装```Python```库：```pip install -r requirements.txt```
7. 根据```config_example.toml```的内容，新建并编辑```config.toml```
8. 运行```Python```文件：```.\run.cmd```
