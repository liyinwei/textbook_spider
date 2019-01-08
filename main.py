"""
@Author: liyinwei
@E-mail: coridc@foxmail.com
@Time: 2018/12/8 10:09 AM
@Description: main
"""

from scrapy import cmdline

# 小学语文 - 人教版
cmdline.execute("scrapy crawl xxyw_pep_spider".split())

# 小学数学 - 人教版
# cmdline.execute("scrapy crawl xxsx_pep_spider".split())
