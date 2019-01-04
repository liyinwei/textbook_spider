"""
@Author: liyinwei
@E-mail: coridc@foxmail.com
@Time: 2019-01-03 10:07
@Description: 人教版小学数学
"""

import re

from scrapy import Request, Spider

from textbook_spider.items import TextbookSpiderItem


class XXSXPepSpider(Spider):
    name = "xxsx_pep_spider"

    allowed_domains = ['shuxue9.com']

    # start_urls = list(
    #     map(lambda x: 'http://www.shuxue9.com/pep/xx%ss/ebook/1.html' % x, range(1, 7))
    # )
    #
    # start_urls.extend(list(
    #     map(lambda x: 'http://www.shuxue9.com/pep/xx%sx/ebook/1.html' % x, range(1, 7))
    # ))
    start_urls = ['http://www.shuxue9.com/pep/xx1s/ebook/1.html']

    def parse(self, response):
        """
        教材首页
        :param response:
        :return:
        """
        last_item = response.meta.get('item')
        if last_item is not None:
            chapter = response.xpath('//h1[@class="title"]/text()').extract_first()
            if chapter == last_item['chapter']:
                last_item['image_urls'].append(response.xpath('//div[@class="center"]/a/img/@src').extract_first())
                next_item = last_item
            else:
                yield last_item
                next_item = self.get_item(response)
        else:
            next_item = self.get_item(response)

        next_page = response.xpath('//a[@class="two"]/@href').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(url=next_page, meta={'item': next_item}, callback=self.parse)

    @staticmethod
    def get_item(response):
        item = TextbookSpiderItem()
        # spider
        item['spider'] = 'xxsx_pep_spider'

        # 年级
        item['grade'] = int(re.search('xx(.+)(sx)', response.request.url).group(1))

        # 章节
        item['chapter'] = response.xpath('//h1[@class="title"]/text()').extract_first()

        # 课文来源:1-文本;2-图片;
        item['source'] = 2

        # url = 'http://www.shuxue9.com/pep/xx1s/ebook/1.html'
        item['url'] = response.request.url

        # image_url = 'http://www.wsbedu.com/shu/book/sutu/rs1111.jpg'
        item['image_urls'] = response.xpath('//div[@class="center"]/a/img/@src').extract()
        return item
