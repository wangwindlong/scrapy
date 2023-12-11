import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://adopt.spca.bc.ca/type/cat/'
headers = {
    'Authorization': 'adopt.spca.bc.ca',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

# 创建Chrome浏览器对象
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式，不打开浏览器窗口
chrome_service = ChromeService()
browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

browser.get(url)
# 设置超时时间为10秒
wait = WebDriverWait(browser, 300)
# wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "ybd-sb-pet-card-container")]')))

# 示例：等待页面上的某个元素加载完成
try:
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ybd-sb-pet-card-container')))
    print('元素已经加载完成:', element.text)
    # 获取页面内容
    page_source = browser.page_source
    # 关闭浏览器
    browser.quit()
    response = page_source
    # response = requests.get(url, headers=headers)
    if response:
        soup = BeautifulSoup(response, 'lxml')
        content = soup.find('div', {'id': 'primary', 'class': 'content-area'})

        # 判断元素是否存在
        if content:
            print('找到符合条件的元素 执行下一步，遍历每一行')
            row = content.find('div', {'id': 'query-pets', 'class': 'row'})
            items = row.find_all('div', {'class': 'ybd-sb-pet-card-container'})
            if items:
                # 打印找到的元素
                for element in items:
                    print("找到了a标签：", element.find('a').get('href'))
        else:
            print('未找到符合条件的元素')
except TimeoutException:
    print('等待超时，未能找到元素')

