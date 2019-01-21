# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re

import pandas as pd
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from common.logger import logger
from common.ocr_util import ocr_client
from textbook_spider import settings


class TextbookSpiderPipeline(object):
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(vars(item).get('_values'))

    def close_spider(self, spider):
        pd.DataFrame(self.data).to_csv('./data/%s.csv' % spider.name)


class TextbookImageSpiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item.get('image_urls') is not None:
            # for url in item['image_urls'].split(','):
            for url in item['image_urls']:
                yield Request(url)

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
                logger.info('download failed. %s' % results)
            else:
                item_image_paths = []
                # 将图片转移至子目录中
                for image_path in image_paths:
                    images_store = settings.IMAGES_STORE
                    newdir = os.path.join(images_store, 'full', item['spider'], item['chapter'])
                    if not os.path.exists(newdir):
                        os.makedirs(newdir)

                    src = os.path.join(images_store, image_path)
                    dest = os.path.join(newdir, image_path.split('/')[-1])

                    if os.path.exists(src):
                        os.rename(src, dest)
                        item_image_paths.append(dest)
                    else:
                        logger.error('img missed: %s' % src)
                item['image_paths'] = None if len(item_image_paths) == 0 else ','.join(item_image_paths)
                # ocr 识别
                item['context'] = self.ocr(item['image_paths'], item['spider'])

        return item

    def ocr(self, image_paths_str, spider):
        if not image_paths_str:
            return None

        # 一个章节的所有图像列表
        image_paths = image_paths_str.split(',')

        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "false"
        options["detect_language"] = "true"
        options["probability"] = "false"

        context = []
        for image_path in image_paths:
            response = ocr_client.basicGeneral(self.get_file_content(image_path), options)
            context.append(''.join([x['words'] for x in response.get('words_result')]))
        return self.clean_context(spider, ' '.join(context))

    @staticmethod
    def clean_context(spider, context):
        if spider == 'xxyw_pep_spider':
            return re.sub('[^\u4e00-\u9fa5,，。:：\?？]', '', context.replace('www.newxue.com', ''))
        elif spider == 'xxsx_pep_spider':
            return re.sub('[^\u4e00-\u9fa5,，。:：\?？]', '', context)
        elif spider == 'xxyy_pep_spider':
            # return re.sub('[^a-zA-Z,\.\s\']', '', context)
            return context

    @staticmethod
    def get_file_content(file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()
