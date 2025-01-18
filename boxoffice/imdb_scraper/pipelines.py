# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImdbScraperPipeline:
    def process_item(self, item, spider):
        return item
import psycopg2

class PostgresPipeline:

    def __init__(self, postgres_uri, postgres_dbname, postgres_user, postgres_password):
        self.postgres_uri = postgres_uri
        self.postgres_dbname = postgres_dbname
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.conn = None
        self.cur = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(
            postgres_uri=crawler.settings.get('POSTGRES_URI'),
            postgres_dbname=crawler.settings.get('POSTGRES_DBNAME'),
            postgres_user=crawler.settings.get('POSTGRES_USER'),
            postgres_password=crawler.settings.get('POSTGRES_PASSWORD')
        )

    def open_spider(self, spider):
        """Open a database connection."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.postgres_dbname,
                user=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_uri
            )
            self.cur = self.conn.cursor()
            # Create the table if it doesn't exist
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    rank TEXT,
                    title TEXT,
                    lifetime_gross TEXT,
                    year TEXT,
                    budget TEXT,
                    mpaa_rating TEXT,
                    running_time TEXT
                )
            """)
            self.conn.commit()
        except Exception as e:
            spider.logger.error(f"Error opening PostgreSQL connection: {e}")

    def close_spider(self, spider):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        """Process each item and insert it into the database."""
        try:
            self.cur.execute("""
                INSERT INTO movies (rank, title, lifetime_gross, year, budget, mpaa_rating, running_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                item['rank'],
                item['title'],
                item['lifetime_gross'],
                item['year'],
                item['budget'],
                item['mpaa_rating'],
                item['running_time']
            ))
            self.conn.commit()
        except Exception as e:
            spider.logger.error(f"Error inserting item into PostgreSQL: {e}")
        return item
