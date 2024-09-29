import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse

from ..items import PhotoparserItem


class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/s/photos/pizza"]

    def parse(self, response):
        links = response.xpath('//figure[contains(@data-testid,"photo-grid-list-figure")]/link[contains(@itemprop,"acquireLicensePage")]/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_post)

    def parse_post(self, response: HtmlResponse):
        loader = ItemLoader(item=PhotoparserItem(),response=response)
        loader.add_xpath('author', '//div[contains(@class,"iMmTi")]/a/text()')
        loader.add_value('post_url', response.url)
        loader.add_xpath('title', '//div[contains(@class,"wdUrX")]/img[2]/@alt')
        loader.add_xpath('categories','//div[contains(@class,"zb0Hu atI7H")]/a/text()')
        loader.add_xpath('img', '//div[contains(@class,"wdUrX")]/img[2]/@src')
        yield loader.load_item()

