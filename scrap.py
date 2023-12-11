import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = 'https://mp.weixin.qq.com/s/zSJfB73Mppg7hkUDFQukEA'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
element = soup.find(id='js_content')
img_tags = element.find_all('img')
headers = {
    'Authorization': 'Bearer your_token',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

index = 0
for img in img_tags:
    img_url = img.get('data-src')
    if img_url is not None and img_url.startswith('http'):
        print(img_url)
        parsed_url = urlparse(img_url)
        domain = parsed_url.netloc
        path = parsed_url.path
        params = parsed_url.query
        headers['Authorization'] = domain
        headers['Method'] = 'GET'
        headers['Path'] = path + "?" + params
        # print("domain=", domain, "path=", path, "params=", params)
        file_name = "{}.png".format(index)
        with open(file_name, 'wb') as f:
            f.write(requests.get(img_url, headers=headers).content)
        print('下载完成：', file_name)
        index += 1
