import json
import os
import time
import multiprocessing
import uuid
from bs4 import BeautifulSoup as bfs
import re
import math

from elastic.elastic import create_index, delete_index
from elastic.elastic import insert_doc

cnt = 0
fail_cnt = 0

rootPath = "/home/xiaochaojun/TsinghuaNewsV4-20190617091014070/mirror/"


def print_time():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def print_info(s):
    times = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print("[%s] %s" % (times, s), flush=True)


month_day = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
pics = re.compile(r'<img .*?src="(.*?)".*?>')

pageRankVal = json.load(open('resource/pageRankVal.txt', 'r'))
url2id = json.loads(open('resource/pageRankResult.txt', 'r').readline())

def getContent(html):
    global pics

    soup = bfs(html)
    title = soup.h1
    if title is None:
        title = soup.h2
        if title is None:
            title = soup.h3
        if title is None:
            title = soup.h4
        if title is None:
            title = 'None'
        else:
            title = title.text
    else:
        title = title.text
    for script in soup.findAll('script'):
        script.extract()
    for style in soup.findAll('style'):
        style.extract()
    soup.prettify()
    content = soup.get_text().replace('\n', '').replace('\u3000', '').replace('\xa0', '')

    pic_urls = pics.findall(html)

    return content, title, pic_urls


def insert_file(index, doc_type, file_path):
    global cnt, fail_cnt
    global pageRankVal, url2id
    try:
        if file_path[-4:] != 'html' and file_path[-3:] != 'htm':
            return
        content = open(file_path, "r", encoding="utf8").read()
    except:
        try:
            content = open(file_path, "r", encoding = "gbk").read()
        except:
            global fail_cnt
            fail_cnt += 1
            return None
    content, title, pic_urls = getContent(content)
    url = file_path.replace(rootPath, '')
    for i in range(len(pic_urls)):
        pic_urls[i] = url.split('/')[0] + pic_urls[i]
    

    # date = file_path.split("/")[-1].split("_")[0]
    # title = file_path.split("/")[-1].split("_")[1].replace(".md", "")

    insert_data = {
        "content": content,
        "title": title,
        "url": url,
        "pic_urls": json.dumps(pic_urls),
        "pageRank": math.log(pageRankVal[url2id[url]])/math.log(10) + 7
    }
    insert_doc(index, doc_type, insert_data, str(uuid.uuid4()))

    cnt += 1
    #if cnt > 10000:
    #    exit(0)


def dfs_search(index, doc_type, input_file_path):
    for filename in os.listdir(input_file_path):
        next_file = os.path.join(input_file_path, filename)
        if os.path.isdir(next_file):
            dfs_search(index, doc_type, next_file)
        else:
            #if filename[-4:] != 'html' or filename[-3:] != 'htm':
            #    continue
            insert_file(index, doc_type, next_file)


def insert_pdf_doc(index, doc_type):
    filelist = ['resource/doc.txt', 'resource/doc2.txt', 'resource/pdf.txt', 'resource/pdf2.txt']
    for f in filelist:
        print(f)
        fin = open(f, 'r')
        line = fin.readline()
        while line:
            line = json.loads(line)
            if line['content'] != '':
                insert_data = {
                    "content": line['content'],
                    "title": line['title'],
                    "url": line['url'],
                    "pic_urls": "[]",
                    "pageRank": 4
                }
                insert_doc(index, doc_type, insert_data, str(uuid.uuid4()))

            line = fin.readline()


if __name__ == "__main__":
    index_name = "project_for_search_engine"
    doc_type = "data"

    text = ["title", "content"]
    keyword = []
    url = ["url", "pic_urls"]

    try:
        delete_index(index_name)
    except Exception as e:
        print(e)

    mapping = {}
    for key in text:
        mapping[key] = {
            "type": "text",
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_smart"
        }

    for key in keyword:
        mapping[key] = {
            "type": "keyword"
        }

    for key in url:
        mapping[key] = {
            "type": "url"
        }

    mapping['pageRank'] = {
        "type": "double"
    }

    mapping = {"mappings": {doc_type: {"properties": mapping}},
               "settings": {"number_of_replicas": 0, "number_of_shards": 30}}
    print(json.dumps(mapping, indent=2))
    create_index(index_name, json.dumps(mapping))
    
    insert_pdf_doc(index_name, doc_type)
    dfs_search(index_name, doc_type, rootPath)
    print(cnt)
