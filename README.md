# Crawling-the_People-s_Daily_Graphic_Database
## 前言


朋友要写论文，需要爬取**人民日报图文数据库**的内容，按某一关键词搜索，爬取该关键词相关的全部文章，将文章内容放到一个文件。网址在这里，[人民日报图文数据库](http://data.people.com.cn/rmrb)，失效了按照下图找一下。
![人民日报图文数据库网址](https://img-blog.csdnimg.cn/7a5564c00536450ba53b690022f325e6.png)


---


## 一、爬取思路分析
> - 进入搜索页面，我们要的是每一篇文章的链接，以及进入链接之后本篇文章的内容。
![页面展示](https://img-blog.csdnimg.cn/5298fad27c4540b39ca585c7ac97be6d.png)

> - 当然没有登录的话，无法查看文章内容，只能看到搜索页面的内容。如下图。
![登录页面](https://img-blog.csdnimg.cn/b7f840bb53124fd4b37864ae4bd7e914.png)

> - F12打开开发者工具，查看当前页面的请求信息。
![f12](https://img-blog.csdnimg.cn/b5990208b99a495dba4d2c00a31975e0.png)

> - 观察Headers中的General、Request Headers和Query String Parameters中的内容，可以得到以下几点：
> 1. 请求方法是GET请求；
> 2. 有cookie；
> 3. 链接中包含许多可调的参数。![瀑布图](https://img-blog.csdnimg.cn/1118762c982d4e39a1fad384acc83d21.png)
> - 就上面第3点举个例子，下图一个是将搜索结果按照时间倒序排序，一个是按时间正序排序，Query String Parameters中的DESC，就变成了ASC。其他的参数可以自己尝试。
> ![倒叙](https://img-blog.csdnimg.cn/cccf6c0d151b41618849c35a5f95282d.png)
 ![正序](https://img-blog.csdnimg.cn/76ba8c39c9a042b6bcf1bf6f4ffef250.png)


> - 综合以上几点，想要实现同学的需求，需要一个**登录的账户**，当然这看个人需求，因为同学并不需要搜索页面的内容，他需要详情页的内容。
![搜索页面内容](https://img-blog.csdnimg.cn/f09b0e1e26fe4997929a45d58aa84e73.png)
![详情页](https://img-blog.csdnimg.cn/015b3165536e48299a846817a9e90f26.png)
> - 尝试使用学校的vpn，发现学校购买了该数据库，故解决登录问题；接下来，尝试解析需要获取的页面数据。
> 1. 搜索页面主要要每个搜索结果的链接。
> ![搜索页面链接](https://img-blog.csdnimg.cn/8065d827d5524230a03aeada294ca894.png)
> 2. 接下来依此访问详情页面，获取详情页的标题、子标题、日期版号以及正文。![详情页内容](https://img-blog.csdnimg.cn/f6bcc34830b140d68054767725dfacf5.png)

> - 最终尝试将解析得到的内容保存，存储的情况如下。
> ![爬取数据展示](https://img-blog.csdnimg.cn/56bfb28f6f6945a999608257226d85b8.png)

# 总结
代码比较简陋，完成了同学的基本需求。实测当中，只爬取了不到一半的文章数据（检索雄安，共1343篇文章，最终只爬取了640篇文章，然后就被反爬了，需要突破验证码），由于数据已经够用，就没有在此项目上继续钻研。
![验证码](https://img-blog.csdnimg.cn/5e80909998a84375b62817e1cc9f5f1c.png)

最后，记录一些突破验证码的心得体会：

- 在请求详情页的地方增加0-9秒的随机暂停，可以适当欺骗对方服务器，延后验证码的到来；
- 尝试更换同学vpn账号，发现cookie值没有改变，估计同一个学校的共用一个账户；
- 道高一尺，魔高一丈。做事不要太过分，今天不行明天再来。对方服务器在前几次会给验证码，突破一定次数，对方会显示另一个页面（即封号），不过一般几小时后就会解封，但也得输入验证码，实在不行就明天再来。
- ![封号](https://img-blog.csdnimg.cn/8108e2c0cc1047b296c14e3aa1adf807.png)
