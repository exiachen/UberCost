# UberCost
通过在Uber官网爬取自己乘车信息来获取乘车花费的一个小爬虫。

#依赖
- 爬虫使用request和pyquery，登录验证还没有实现直接使用用户名和密码，还是使用COOKIE（在setting.py中设置，COOKIE可以通过浏览器开发工具获取）。
- 对爬取的数据会使用pycha画一个简单的数据图（一年中每个月使用Uber的花费）。

#使用方式
- 手动设置COOKIE
- python spider.py
