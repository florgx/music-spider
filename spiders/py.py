# -*- coding: utf-8 -*-
import scrapy, copy
# 增量式爬虫需增加部分1
from scrapy_redis.spiders import RedisSpider


class PySpider(RedisSpider):
    name = 'py'
    allowed_domains = ['example.com']
    redis_key = "py"

    def parse(self, response):
        """
        场景：scene
        风格：style
        :param response:
        :return:
        """
        item, scene_dict, style_dict = {},{},{}
        scene_list, style_list = [],[]
        print(response.status)
        sce_a_list = response.xpath("//div[@class='type1'][1]/div[@class='uli']/a/following-sibling::a")
        sty_a_list = response.xpath("//div[@class='type1'][2]/div[@class='uli']/a/following-sibling::a")
        home_url = 'https://www.example.com/peiyue/'
        # 解析场景类型
        for url in sce_a_list:
            sc_url = url.xpath("./@href").extract_first().split("/")[-2]  # m105
            scene = url.xpath("./text()").extract_first() # 情绪场景
            scene_dict[sc_url] = scene
            scene_list.append(sc_url)

        # 解析音乐风格类型
        for url in sty_a_list:
            sty_url = url.xpath("./@href").extract_first().split('/')[-2]  # j114
            style = url.xpath("./text()").extract_first()  # 安静
            style_dict[sty_url] = style
            style_list.append(sty_url)  # 收集得到的 url 后缀
        item['scene_name'] = scene_dict
        item['style_name'] = style_dict

        # 组合分类版块url,所有音频项目的顶点
        for i in scene_list:
            print('------')
            for n in style_list:
                print("++++++")
                page_url = home_url + i + '_' + n  
                print(page_url)
                yield scrapy.Request(url=page_url, meta={"item": copy.deepcopy(item)}, callback=self.parse_page, dont_filter=True)
            #     break
            # break

    def parse_page(self, response):
        item = response.meta["item"]
        # 解析音频区域
        dl_list = response.xpath("//div[@class='b-box']/dl")
        # 遍历当前页所有音频url
        for dl in dl_list:
            # 配乐名
            item['title'] = dl.xpath(".//a[@class='title']/text()").extract_first()
            href_list = response.xpath("//div[@class='type1'][2]//a[@class='current']/@href").extract_first().split('/')[-2].split('_')
            # 配乐类型
            item['style'] = item['scene_name'][href_list[0]] + '-' + item['style_name'][href_list[1]]  # 情绪场景-安静
            # 配乐src
            src = dl.xpath('./audio/source/@src').extract_first()
            # 已经解析到音频的url，接下来开始爬取音频文件并保存到本地
            # 并且爬取下一页
            print('https:' + src)  # 打印真实配乐url
            print(item['style'])  #
            # 碰到了403，被反扒了，哈哈
            item['type'] = src.split('/')[-1].split('.')[-1]  # .mp3
            print('./' + item['title'] + '.' + item['type'])  # 电音节奏转换.mp3
            yield scrapy.Request(url='https:' + src, meta={'item': copy.deepcopy(item)}, callback=self.down_au, dont_filter=True)
        # 下一页
        next_page = response.xpath("//div[@class='pageinfo']//a[contains(text(), '下一页')]/@href").extract_first()
        if next_page:
            print("开始爬取下一页", next_page)
            yield scrapy.Request(url='https://example.com' + next_page, meta={'item': copy.deepcopy(item)}, callback=self.parse_page, dont_filter=True)

    def down_au(self, response):
        item = response.meta['item']
        item['audio'] = response.body
        yield item

  




