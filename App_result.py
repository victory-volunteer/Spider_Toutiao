import json
import xlwt
import time
import mitmproxy.http

# 全局变量
line = 1

# 表头数据预处理
workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet("data1")
xls_head = ["标题", "摘要", "来源", "评论数", "原始url", "头条url", "播放量", "发布时间"]
for i, k in enumerate(xls_head):
    worksheet.write(0, i, k)
workbook.save("今日头条app.xls")


def top_5(data):
    list1 = []
    # 标题
    title = data.get('title', '无')
    list1.append(title)
    # 摘要
    abstract = data.get('abstract', '无')
    # 对个人在头条发文的特殊处理
    if abstract == '':
        abstract = data.get('content', '无')[:20]
    list1.append(abstract)
    # 来源
    source = data.get('source', '无')
    # 对个人在头条发文的特殊处理
    if source == '无':
        source = data.get('user', '无').get('screen_name', '无')
    list1.append(source)
    # 评论数
    comment_count = data.get('comment_count', '无')
    list1.append(comment_count)
    # 原始url
    original_url = data.get('url', '无')
    list1.append(original_url)
    # 头条url
    toutiao_share_url = data.get('share_url', '无')
    list1.append(toutiao_share_url)
    # 播放量
    read_count = data.get('read_count', '无')
    list1.append(read_count)
    # 发布时间
    publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get('publish_time', '0')))
    list1.append(publish_time)

    data_storage(list1)


def data_storage(list1):
    global line
    # 写入execl文件
    for m, n in enumerate(list1):
        worksheet.write(line, m, n)
    workbook.save("今日头条app.xls")
    line += 1


def response(flow: mitmproxy.http.HTTPFlow):
    if flow.request.host != 'api5-normal-hl.toutiaoapi.com' or not flow.request.path.startswith("/api/news/feed/v88/"):
        return

    file_data = flow.response.text
    result = json.loads(file_data)

    if result['has_more']:
        count = 0
        for c, i in enumerate(result['data']):
            count += 1
            json_data = json.loads(i['content'])
            # 判断类型
            if json_data.get('label', '') == '问答':
                print(f"第{count}条问答——不处理")
            elif json_data.get('action_list', '') == '':
                print(f"第{count}条是单纯视频——不处理")
            else:
                top_5(json_data)
                print(f"处理第{count}条")
                
# 启动方式: mitmdump -s 测试1.py -p 8889