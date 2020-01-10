# -*- coding: utf-8 -*-
# author: ffteen
"""
爬取央视网新闻联播
依赖 
requests 
sbcrawler
"""
from sbcrawler import Crawler, HTML
from pprint import pprint
import requests
import re
import json
import pathlib
from urllib.request import urlretrieve

def get_pid(detai_url):
    html = requests.get(detai_url).text
    pid = re.findall('var guid = "(.*?)"', html)[0]
    return pid

def get_video_info(pid):
    part_url = 'http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid='
    response_json = requests.get(part_url+pid).json()

    title = response_json['tag']
    time = response_json['f_pgmtime']
    video = response_json['video']['chapters4']
    video_url = []
    for i in video:
        video_url.append(i['url'])
    return {
        'title': response_json["title"],
        'time': time,
        'video_urls': video_url
    }

def download_videos(video_info, path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    video_urls = video_info['video_urls']
    filename = '{}.txt'.format(video_info['title'])
    filename = pathlib.Path(path) / filename
    # 合并之前的视频名，合并之后删除
    for index, item in enumerate(video_urls):
        print('正在下载第{}个视频'.format(index+1), item)
        video_filename = video_info['title']+'-'+str(index+1)+'.mp4'
        video_filename = pathlib.Path(path) / video_filename
        urlretrieve(item, video_filename)
        # 创建一个txt文件，在每行写入file '待合并的视频名称'
        with open(filename, 'a+')as f:
            f.write(f'{video_filename}\n')

class CCTVCrawlerExample(Crawler):
    start_url = "http://tv.cctv.com/lm/xwlb/day/20200105.shtml"
    date_string = "20200105"
    allowed_domain = "http://tv.cctv.com/"

    def extract_links(self, html, task):
        # 抽取链接 加到爬取任务列表
        if task.depth == 1:
            pid = get_pid(task.url)
            info = get_video_info(pid)
            download_videos(info, self.date_string)
            return
        super().extract_links(html, task)

    def download_html(self, task):   # 编码的问题，重写一下吧
        headers = {
            "User-Agent": self.user_agent
        }
        response = requests.get(task.url, headers=headers)
        if response.status_code != 200:
            self.download_error_urls.append(task.url)
            self.log.warning(
                f"download [ {task.url} ] error! status_code={response.status_code}")
            return None
        else:
            self.log.info(f"download [ {task.url} ] success.")
            text = response.content.decode("utf-8")
            return HTML(html=text, url=task.url)

    def extract_content(self, html, task):
        pass  # 因为父类要求子类必须实现


def crawl_date(date_string):
    crawler = CCTVCrawlerExample()
    crawler.date_string = date_string
    crawler.start_url =  f"http://tv.cctv.com/lm/xwlb/day/{date_string}.shtml"
    crawler.start()


if __name__ == '__main__':
    crawl_date("20200105")
