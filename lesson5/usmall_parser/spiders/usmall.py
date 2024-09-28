import scrapy
from scrapy.http import HtmlResponse



from usmall_parser.items import UsmallParserItem

# scrapy crawl usmall -o output.json

class UsmallSpider(scrapy.Spider):
    name = "usmall"
    allowed_domains = ["usmall.ru"]
    start_urls = ["https://usmall.ru/products/men/shoes/sneakers-athletic-shoes?brand=885&size=16&page=1"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//div[contains(@class,"pagination")]/a[@class="__show-more"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath(
            '//div[contains(@class,"product-preview")]/div[@class="__inner"]/a[@class="__brand"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_post)


    def parse_post(self, response: HtmlResponse):
        item = UsmallParserItem()
        brand = response.xpath(
            '//h1[contains(@class, "p-product__h1")]/a/text()').get()
        item['brand'] = brand
        name = response.xpath(
            '//h1[contains(@class, "p-product__h1")]/span/text()').get()
        item['name'] = name
        vendor_code = response.xpath(
            '//div[contains(@class, "p-product__vendor-code")]/span/text()').get()
        item['vendor_code'] = vendor_code
        color = response.xpath(
            '//div[contains(@class, "p-product__color-list")]/label/span/@title').getall()
        item['color'] = color
        price = response.xpath(
            '//div[contains(@class, "p-product__price-value")]/text()').get()
        item['price'] = price
        yield item
