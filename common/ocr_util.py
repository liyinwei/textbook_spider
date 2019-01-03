"""
@Author: liyinwei
@E-mail: coridc@foxmail.com
@Time: 2018/12/8 9:46 AM
@Description: baidu ocr
"""

from aip import AipOcr

APP_ID = '15093189'
API_KEY = 'g6moXImz17WDuZYQxkGd9M0a'
SECRET_KEY = '8fdbLBHWDO2cFsVUK4OQoZ2Ewo1TNsGx'

ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

if __name__ == '__main__':
    pass
