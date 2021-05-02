# tg_bot_check 👻
tg_bot_check 是一个利用telegram bot做的域名检测和服务器检测的工具
## Usage
```
0、python3环境
1、创建telegram机器人 获取token
2、创建群组(如果需要)
3、修改check_server.py 里面的 token、chat_id 、mail等等内容
4、将域名一行一个 放入domains.txt
5、将服务器IP和端口 按照 IP:端口  的格式 一行一个放入 ip_port.txt
6、定时任务 python3 check_server.py 即可
```
## License

[The Unlicense](https://unlicense.org)
