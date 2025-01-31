# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import Error
import json
import logging
from scrapy.exceptions import DropItem


logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ShoplifterPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        
        price_value = adapter.get('price')
        price_value = str(price_value).replace("$ ", '')
        adapter['price'] = float(price_value)

        return item



class MySQLPipeline:
    def __init__(self, mysql_host, mysql_database, mysql_user, mysql_password, mysql_port):
        self.mysql_host = mysql_host
        self.mysql_database = mysql_database
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_port = mysql_port

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_database=crawler.settings.get('MYSQL_DATABASE'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        try:
            self.connection = mysql.connector.connect(
                host=self.mysql_host,
                database=self.mysql_database,
                user=self.mysql_user,
                password=self.mysql_password,
                port=self.mysql_port
            )
            self.cursor = self.connection.cursor()
            self.logger = logging.getLogger(__name__)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id  VARCHAR (255) UNIQUE,
                    url VARCHAR(255),
                    title text,
                    price DECIMAL,
                    description text,
                    color JSON,
                    size JSON,
                    pictures JSON
                )
            """)
        except Error as e:
            self.logger.error(f"Error opening MySQL connection: {e}")
            raise DropItem(f"Error opening MySQL connection: {e}")


    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Error as e:
            self.logger.error(f"Failed to commit data to MySQL: {e}")
        finally:
            self.cursor.close()
            self.connection.close()

    def process_item(self, item, spider):
        try:
            # Adjust based on your scraped item fields
            self.cursor.execute("""
                INSERT INTO products (
                    product_id,
                    url,
                    title,
                    price,
                    description,
                    color,
                    size,
                    pictures
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item.get('product_id'),
                item.get('url'),
                item.get('title'),
                item.get('price'),
                item.get('description'),
                json.dumps(item.get('color')),
                json.dumps(item.get('size')),
                json.dumps(item.get('pictures')),
            ))
            self.connection.commit()
        except Error as e:
            self.logger.error(f"Error inserting item into MySQL: {e}")
            raise DropItem(f"Error inserting item into MySQL: {e}")

            return None  # Continue processing other items
        return item
