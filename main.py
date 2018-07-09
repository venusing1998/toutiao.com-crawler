import json
import os
from hashlib import md5
from multiprocessing.pool import Pool

import requests

GROUP_START = 1
GROUP_END = 8
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.join(BASE_DIR, "images")


def get_html(offset, keyword):
    """获取网页源代码

    """
    url = "https://www.toutiao.com/search_content/?offset={0}&format=json&keyword={1}&autoload=true&count=20&cur_tab=1&from=search_tab"
    new_url = url.format(offset, keyword)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    try:
        response = requests.get(new_url, headers=headers)
        if response.status_code == 200:
            html = response.json()
            # result = json.dumps(html, indent=4)
            return html
    except requests.ConnectionError:
        return None


def get_images(json):
    """获取image的url

    """
    data = json.get("data")
    if data:
        for item in data:
            image_list = item.get("image_list")
            if image_list:
                for image in image_list:
                    yield {
                        "url": image.get("url"),
                    }


def write_into_file(keyword, item):
    """写入文件

    """
    if not os.path.exists(os.path.join(RESULT_DIR, keyword)):
        os.makedirs(os.path.join(RESULT_DIR, keyword))
    try:
        image_url = item.get("url")
        new_image_url = "http:" + image_url.replace("list", "large")
        response = requests.get(new_image_url)
        if response.status_code == 200:
            file_path = "{0}/{1}/{2}.{3}".format(RESULT_DIR, keyword,
                                                 md5(response.content).hexdigest(), "jpg")
            if not os.path.exists(file_path):
                with open(file_path, "wb") as f:
                    f.write(response.content)
            else:
                print("Already Downloaded", md5(
                    response.content).hexdigest(), "jpg", sep="")
    except requests.ConnectionError:
        print("Failed to save image")


def main(offset):
    """主函数

    """
    # 这里修改keyword
    keyword = "测试"
    json = get_html(offset, keyword)
    for item in get_images(json):
        print("正在下载: http:", item["url"], "jpg", sep="")
        write_into_file(keyword, item)


if __name__ == '__main__':
    print('*'*20, 'begin', '*'*20, '\n')
    print('author: Chris\n')
    print('*'*47)
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START-1, GROUP_END+1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
    print('*'*21, 'end', '*'*21, '\n')
