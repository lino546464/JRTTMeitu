import requests
import json
import os
import time
import multiprocessing
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

#url = 'http://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=3'

def get_pictures(url):
    content = requests.get(url, headers=headers)
    html = json.loads(content.text)
    # print(html)
    if 'data' in html.keys():
        for result in html.get('data'):
            title = result.get('title')
            url = result.get('url')
            makedir(title)
            if 'image_detail' in result.keys():
                for img in result.get('image_detail'):
                    img_url = img.get('url')
                    save_img(img_url)
                    print(img_url)

def makedir(name):
    path = str(name).strip()
    #path = str(name).strip()
    img_path = os.path.exists(os.path.join('H:\Python\crawl\JRTT0',path))
    if img_path:
        print('文件夹已经存在')
        return False
    else:
        print('正在创建名字为 {} 的文件夹'.format(name))
        os.makedirs(os.path.join('H:\Python\crawl\JRTT0',path))
        os.chdir(os.path.join('H:\Python\crawl\JRTT0',path))
        return True

def save_img(img_url):
    name = img_url[-20:]
    imgs = requests.get(img_url, headers=headers)
    with open(name+'.jpg','wb') as f:
        print('正在保存图片{}'.format(name))
        f.write(imgs.content)


def main():
    urls = []
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in range(0,5):
        page = str(i*20)
        #print('正在保存第{}页'.format(i))
        url = 'http://www.toutiao.com/search_content/?offset={}&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=3'.format(page)
        # get_pictures(url)
        urls.append(url)
    #print(urls)
    for uri in urls:
        pool.apply_async(get_pictures,(uri,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    star = time.time()
    main()
    end = time.time()
    print('爬取结束，共耗时{}s'.format(end-star))