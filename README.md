# toutiao
今日头条网页端及APP信息爬取（含逆向js）

项目介绍: 对于网页端使用selenium和requests分别实现，APP端使用mitmdump实现。


Selenium：通过其模拟点击和滑动，以自动化的方式来逐页通过xpath解析爬取信息，并保存到csv文件中。


Requests：头条中主要信息位于二次请求中，部分参数通过执行逆向得到的js代码来获取，响应内容通过xpath和json解析，最终存入execl文件。并通过协程和url队列来提高爬取速度。


Mitmdump：手机APP中的请求响应信息大多为json数据，解析其中参数即可，对于请求参数，这里使用Mitmdump来实现实时爬取，避免了请求参数解析的复杂。爬取时需要PC使用Mitmdump监听端口请求，手机端使用autojs脚本来实现自动滑动，最终信息被收集到execl文件中。

