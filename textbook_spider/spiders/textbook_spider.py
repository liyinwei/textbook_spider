"""
@Author: liyinwei
@E-mail: coridc@foxmail.com
@Time: 2018/12/6 10:52 AM
@Description: 人教版（新课程标准）小学语文课件爬虫
"""
import logging
import re

from scrapy import Request, Spider

from textbook_spider.items import TextbookSpiderItem

logging.basicConfig(filename='spider.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class TextbookSpider(Spider):
    name = "textbook_spider"

    allowed_domains = ['newxue.com']

    start_urls = list(
        map(lambda x: 'http://www.newxue.com/yuwen/rjkb%sa' % x, range(1, 10))
    )

    start_urls.extend(list(
        map(lambda x: 'http://www.newxue.com/yuwen/rjkb%sb' % x, range(1, 10))
    ))

    def parse(self, response):
        """
        教材首页
        :param response:
        :return:
        """
        for sel in response.xpath('//div[@class="ywlblt" or @class="ywlbrt"]/p/a'):
            item = TextbookSpiderItem()
            # 年级
            item['grade'] = response.request.url[-3]
            # 章节
            item['chapter'] = sel.xpath('text()').extract()[0].strip()
            # 正文
            yield Request(url=sel.xpath('@href').extract()[0], meta={'item': item}, callback=self.parse_context)

    def parse_context(self, response):
        """
        跳转页
        :param response:
        :return:
        """
        item = response.meta['item']
        # 课文原文
        sel = response.xpath('//a[contains(text(), "课文原文")]')

        if len(sel) > 0:
            # 有原文，则直接读取文本
            item['source'] = 1
            item['url'] = sel[0].xpath('@href').extract()[0]
            item['image_paths'] = None
            item['image_urls'] = None
            yield Request(url=item['url'], meta={'item': item},
                          callback=self.parse_context_detail)
        else:
            # 无原文，则需抓取图片列表
            item['source'] = 2
            sel = response.xpath('//a[contains(text(), "电子课本")]')
            if len(sel) > 0:
                item['url'] = sel[0].xpath('@href').extract()[0]
                yield Request(url=item['url'], meta={'item': item},
                              callback=self.parse_context_detail)
            else:
                item['source'] = 0
                item['url'] = None
                item['context'] = None
                item['image_paths'] = None
                item['image_urls'] = None
                logging.info('no source found, url: %s' % response)
                yield item

    def parse_context_detail(self, response):
        """
        正文页
        :param response:
        :return:
        """
        item = response.meta['item']
        if item['source'] == 1:
            # 有原文，直接读取文本（过滤换行及<p></p>等标签）
            item['context'] = re.sub(r'\s+', '',
                                     response.xpath('//div[@class="jclj_text"]')[0].xpath('string(.)').extract()[0])
        elif item['source'] == 2:
            # 无原文，则需抓取图片列表
            img_urls = response.xpath('//div[@class="jclj_text"]//img[contains(@src, "dianzikeben")]//@src').extract()

            item['image_urls'] = ','.join(img_urls)
        yield item
