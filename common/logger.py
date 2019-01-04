"""
@Author: liyinwei
@E-mail: coridc@foxmail.com
@Time: 2019-01-04 16:09
@Description: logger
"""

import logging.config

logging.config.fileConfig('./conf/logging.conf')

# create logger
logger = logging.getLogger('textbook_spider')

if __name__ == '__main__':
    pass
