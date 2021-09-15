import requests
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from lxml import etree
from scrapy_medicine.items import ScrapyMedicineItem
from queue import Queue

count = 1


class MedicinespSpider(scrapy.Spider):
    name = 'MedicineSp'

    # allowed_domains = ['https://ypk.99.com.cn/kszyp/']
    # start_urls = ['https://ypk.99.com.cn/Home/GetDrugListByFind/']

    def start_requests(self):
        print(1)
        for i in range(1, 19999):
            url = "https://ypk.99.com.cn/Home/GetDrugListByFind?classid=0&brandid=0&drugtype=&fourtype=1&isotc=0" \
                  "&isyibao=0&pageindex={}".format(
                i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        if 'pageindex' in response.url:
            link_head = 'https://ypk.99.com.cn/DrugInstructions'
            text = response.xpath('//dl')
            for i in text:
                None_eff = response.xpath('./dd/p/text()').extract_first()
                if None_eff != ' ' and None_eff != '暂无信息':
                    link_ = i.xpath('./dt/a/@href').extract_first()
                    url__ = link_[3:len(link_)]
                    yield scrapy.Request(url=link_head + url__, callback=self.parse)
        else:
            print(response.url)
            name = response.xpath('//div[@class="drug-wrap1"]//b/text()').extract()
            print(name)
            efficacy_component = response.xpath('//div[@class="drug-mcont"]/p/text()').extract()
            efficacy = efficacy_component[4].strip()
            component = efficacy_component[5].strip()
            # print('药效:', efficacy)
            # print('成分', component)
            item = ScrapyMedicineItem()
            item['name'] = name[0].encode('GBK', 'ignore').decode('GBk')
            item['efficacy'] = efficacy.encode('GBK', 'ignore').decode('GBk')
            item['component'] = component.encode('GBK', 'ignore').decode('GBk')
            global count
            count += 1
            print(count)
            yield item
