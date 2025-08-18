# -*- coding: utf-8 -*-
import os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PeiyuePipeline(object):
    def process_item(self, item, spider):

        if not os.path.exists('./素材库/' + item['style']):
            print("目录不存在，创建中……")
            os.mkdir('./素材库/' + item['style'])
            print("创建完成")
        with open('./素材库/' + item['style'] + '/' + item['title'] + '.' + item['type'], 'wb') as f:
            print("保存文件：", item['title'])  # 3.5版可没有f""的格式化方法
            f.write(item['audio'])

        print("保存完毕……")
        return item

