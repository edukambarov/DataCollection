# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class PhotoparserPipeline:
    def process_item(self, item, spider):
        return item

class PhotoparserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['img']:
            try:
                yield scrapy.Request(item['img'])
                # print(f"photo_{item['img']} is loading")
            except Exception as e:
                print(e)
                # print(f"photo_{item['img']} is NOT loading: {e}")

    def item_completed(self, results, item, info):
        if results:
            item['img'] = [ele[1] for ele in results if ele[0]]
        return item