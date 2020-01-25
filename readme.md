# wuhan_bot

这是一个能够自动将2019-ncov的最新信息发送到qq群的机器人程序，使用cqhttp和python-aiocqhttp库

更多信息请看这里

[这里](https://github.com/richardchien/python-aiocqhttp?tdsourcetag=s_pctim_aiomsg)
[这里](https://github.com/richardchien/coolq-http-api)

目前有三个命令 分别是 `test` `地区` `查询`

详细请看代码

main.py为机器人主程序
timer.py为定时任务程序，可配合任务计划来实现抓取并播报最新信息