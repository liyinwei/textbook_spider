# -*- coding: utf-8 -*-

import logging
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pandas as pd
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from textbook_spider import settings

logging.basicConfig(filename='spider.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class TextbookSpiderPipeline(object):
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(vars(item).get('_values'))

    def close_spider(self, spider):
        pd.DataFrame(self.data).to_csv('textbook_spider.csv')


class TextbookImageSpiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item.get('image_urls') is not None:
            for url in item['image_urls'].split(','):
                yield Request('http://www.newxue.com' + url)

            item['context'] = self.ocr(item['chapter'])

    def item_completed(self, results, item, info):
        """
        按章节重新存放图片
        :param results:
        :param item:
        :param info:
        :return:
        """
        if item.get('image_urls') is not None:
            # 一次请求的所有图片列表
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                # 下载失败忽略该 Item 的后续处理
                logging.info('download failed. %s' % results)
            else:
                item_image_paths = []
                # 将图片转移至子目录中
                for image_path in image_paths:
                    images_store = settings.IMAGES_STORE
                    newdir = os.path.join(images_store, 'full', item['chapter'])
                    if not os.path.exists(newdir):
                        os.makedirs(newdir)

                    src = os.path.join(images_store, image_path)
                    dest = os.path.join(newdir, image_path.split('/')[-1])

                    if os.path.exists(src):
                        os.rename(src, dest)
                        item_image_paths.append(dest)
                    else:
                        logging.error('img missed: %s' % src)
                item['image_paths'] = None if len(item_image_paths) == 0 else ','.join(item_image_paths)
        logging.info(type(item))
        logging.info(item)
        return item

    def ocr(self, image_dir):
        return 'aaaaaaaa'
