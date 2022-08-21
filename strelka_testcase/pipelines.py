# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2

class StrelkaTestcasePipeline:
    """
        Пайплайн для загрузки данных в кластер
    """
    def open_spider(self, spider):
        hostname = 'db02.cluster.strlk.ru'
        username = 'testuser01'
        password = 'test01'
        database = 'test01'
        port = '5455'
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password,  
            dbname=database, port=port)
        self.cur = self.connection.cursor()
    
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute(f"insert into hotels(id,hotel,type,legal_entity_name,region,inn,ogrn,address,phone_number,email,site_url,classification) values('{item['id']}','{item['hotel']}','{item['type']}','{item['legal_entity_name']}','{item['region']}','{item['inn']}','{item['ogrn']}','{item['address']}','{item['phone_number']}','{item['email']}','{item['site_url']}','{item['classification']}')")
            self.connection.commit()
        except:
            self.connection.rollback()
            raise        
        
        return item