import json
import os

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")


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
            result = json.dumps(html, indent=4)
            return result
    except requests.ConnectionError:
        return None


def write_into_file(result):
    """写入文件

    """
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
    with open("dist/result.json", "w", encoding="utf-8") as f:
        f.write(result)


def main():
    """主函数

    """
    # 可以修改的测试值 offset=20
    offset = 20
    keyword = "测试"
    result = get_html(offset, keyword)
    write_into_file(result)


if __name__ == "__main__":
    print('*'*20, 'begin', '*'*20, '\n')
    print('author: Chris\n')
    print('*'*47)
    main()
    print('*'*21, 'end', '*'*21, '\n')
