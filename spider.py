import os 
import math 

import scrapy
from mastodon import Mastodon 


class VacinatedSpider(scrapy.Spider):
    name = 'vacinatedspider'
    start_urls = ['https://impfdashboard.de']

    def parse(self, response):
        with open("progress.txt", "w", encoding="utf-8") as file:
            text = response.xpath("/html/body/main/section/div[2]/div/div/div/div/div/div[2]/p/span[4]/span/text()").get()
            percentage = text.split()[0]
            floatpercentage = float(percentage.replace(",", "."))
            percentagerounded = int(math.ceil(floatpercentage))

            divider = 5 
            maxchars = int(100 / divider)

            fullchars = math.ceil(percentagerounded/divider)
            emptychars = maxchars - fullchars
            
            bar = ""
            for _ in range(fullchars):
                bar = "{}{}".format(bar, "█")
            
            for _ in range(emptychars):
                bar = "{}{}".format(bar, "░")

            bar = "{} {} %".format(bar, percentage)

            file.write(bar)

            mastodon = Mastodon(
                access_token = os.getenv("MASTODON_ACCESS_TOKEN"),
                api_base_url = 'https://mastodon.online'
            )
            mastodon.toot(bar)
