"""
@Author: liyinwei
@E-mail: coridc@foxmail.com
@Time: 2019-01-07 09:59
@Description: 人教版（PEP）小学英语课件爬虫
"""

from scrapy import Request, Spider

from textbook_spider.items import TextbookSpiderItem


class XXYYPepSpider(Spider):
    name = "xxyy_pep_spider"

    allowed_domains = ['wsbedu.com']

    start_urls = list(
        map(lambda x: 'http://www.wsbedu.com/xiaox/rje%s1kb.asp' % x, range(3, 7))
    )

    start_urls.extend(list(
        map(lambda x: 'http://www.wsbedu.com/xiaox/rje%s2kb.asp' % x, range(3, 7))
    ))

    # start_urls = ['http://www.wsbedu.com/xiaox/rje31kb.asp']

    def parse(self, response):
        """
        教材首页
        :param response:
        :return:
        """
        for sel in response.xpath('//div[@class="main_left2"]/table//tr[position()>1]//a'):
            item = TextbookSpiderItem()
            # spider
            item['spider'] = 'xxyy_pep_spider'
            # 年级
            item['grade'] = response.request.url[-8]
            # 章节
            item['chapter'] = sel.xpath('text()').extract_first().strip().replace('电子课本', '')
            # 课文来源:1-文本;2-图片;
            item['source'] = 2
            # url
            item['url'] = []
            # image_urls
            item['image_urls'] = []

            url = response.urljoin(sel.xpath('@href').extract_first())
            # 正文
            yield Request(url=url, meta={'item': item}, callback=self.parse_context)

    def parse_context(self, response):
        """
        正文页-分页
        :param response:
        :return:
        """
        item = response.meta['item']
        pages = response.xpath('//div[@class="STYLE8"]//a[position()>1]')
        # 单个章节多页的处理
        for index, sel in enumerate(pages):
            url = response.urljoin(sel.xpath('@href').extract_first())
            # url
            item['url'].append(url)

        yield Request(
            url=item['url'][0],
            meta={
                'item': item,
                'page_no': 0
            },
            callback=self.parse_context_detail
        )

    def parse_context_detail(self, response):
        """
        正文页
        :param response:
        :return:
        """
        item = response.meta['item']
        page_no = int(response.meta['page_no'])

        img_urls = response.xpath('//div[@class="main_left2"]/img/@src').extract()
        img_urls = list(response.urljoin(x) for x in img_urls)
        item['image_urls'].extend(img_urls)

        if page_no == len(item['url']) - 1:
            yield item
        else:
            page_no += 1
            yield Request(
                url=item['url'][page_no],
                meta={
                    'item': item, 'page_no': page_no
                },
                callback=self.parse_context_detail
            )
