import scrapy


class BayutSpider(scrapy.Spider):
    name = "bayut_spider"

    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']

    def parse(self, response):
        # Extract property details
        properties = response.css('article')

        for property in properties:
            try:
                title = property.css('h2::text').get(default='').strip()
                price = property.css('span[class*="price"]::text').get(default='').strip()
                location = property.css('div[class*="location"]::text').get(default='').strip()
                bedrooms = property.css('span[class*="bedrooms"]::text').get(default='').strip()
                bathrooms = property.css('span[class*="bathrooms"]::text').get(default='').strip()
                size = property.css('span[class*="size"]::text').get(default='').strip()
                link = response.urljoin(property.css('a.property-link::attr(href)').get())

                yield {
                    'Title': title,
                    'Price': price,
                    'Location': location,
                    'Bedrooms': bedrooms,
                    'Bathrooms': bathrooms,
                    'Size': size,
                    'Link': link
                }
            except AttributeError:
                continue

        # Follow pagination links
        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

