from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from lxml import etree
import csv

option = Options()
# option.add_argument('--headless')
# option.add_argument('--disable-gpu')
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument('--disable-blink-features=AutomationControlled')


def keji():
    # 点击科技栏
    WebDriverWait(web, 20, 1).until(EC.presence_of_element_located(
        (By.XPATH, '//div[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul/li[7]'))).click()
    time.sleep(5)


def info(page,file_writer):
    for i in range(page - 1):
        web.execute_script('document.documentElement.scrollTop=20000')
        time.sleep(3)

    html = etree.HTML(web.page_source)
    # list = html.xpath('//div[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]/div')

    list = html.xpath('//div[@class="ttp-feed-module"]/div[2]/div')

    x = 1  # 做统计

    for i in list:
        address = i.xpath('.//div[@class="feed-card-footer-cmp-author"]/a/text()')
        # print(address)
        if address == []:
            address = ''
        else:
            address = address[0]
        # print(address)

        if address == '':
            title = i.xpath('.//div[@class="feed-card-wtt-l"]/p/a/text()')
            # print(title)
            if title == []:
                title = '无标题'
            else:
                title = title[0][:20].replace('\n', ' ')
            # print(title)
        else:
            title = i.xpath('.//div[@class="feed-card-article-l"]/a/@aria-label')
            # print(title)
            if title == []:
                title = '无标题'
            else:
                title = title[0]
            # print(title)

        comment_count = i.xpath('.//div[@class="feed-card-footer-cmp"]/div/div[2]/a/@aria-label')
        # print(comment_count)
        if comment_count == []:
            comment_count = '无评论'
        else:
            comment_count = comment_count[0]
        # print(comment_count)

        file_writer.writerow([title, address, comment_count])
        print(f'--------第{x}条完成----------')
        x += 1


if __name__ == '__main__':
    web = webdriver.Chrome(options=option)
    web.maximize_window()
    web.set_page_load_timeout(10)  # 设置页面超时时间

    try:
        web.get("https://www.toutiao.com/")
        keji()

        file = open('ddatas.csv', mode='w', newline='')
        file_writer = csv.writer(file)
        file_writer.writerow(['标题', '出处', '评价数'])

        info(3, file_writer)  # 获取3页,也就是3*15=45条数据

        file.close()
        web.close()
        web.quit()
    except TimeoutException as e:
        web.execute_script('window.stop()')
        print("页面超时停止加载")
        web.close()
        web.quit()