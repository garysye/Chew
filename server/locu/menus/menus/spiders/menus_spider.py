import scrapy
import re
from menus.items import RestaurantsItem, MenusItem, SectionsItem, FoodsItem, AddressesItem

class MenuSpider(scrapy.Spider):
  name = "menu"
  allowed_domains = ['sanfrancisco.menupages.com']
  start_urls = ['http://sanfrancisco.menupages.com/']

  def parse(self, response):
    for href in response.selector.xpath('//div[@id="list-by-neighborhood"]/div[@class="content"]/ul/li/a/@href'):
      url = response.urljoin(href.extract())
      yield scrapy.Request(url, callback=self.parse_results)

  def parse_results(self, response):
    for href in response.selector.xpath('//table[@class="search-results"]/tbody/tr/td[@class="name-address"]/a[@class="link"]/@href'):
      url = response.urljoin(href.extract())
      yield scrapy.Request(url, callback=self.parse_restaurant)

  def parse_restaurant(self, response):
    selector = response.selector

    restaurant = RestaurantsItem()
    restaurant['name'] = selector.xpath('//h1/text()').extract()
    cuisine = selector.xpath('//li[@class="cuisine category"]/text()').extract()
    restaurant['cuisine'] = cuisine
    
    restaurant['address'] = AddressesItem()
    restaurant['address']['street_address'] = []
    address_selector = selector.xpath('//li[@class="address adr"]')
    street_address_selectors = address_selector.xpath('./span[contains(@class, "address")]/text()')
    for sel in street_address_selectors:
      restaurant['address']['street_address'].append(sel.extract())
    restaurant['address']['city'] = address_selector.xpath('.//span[@class="locality"]/text()').extract()
    restaurant['address']['zipcode'] = address_selector.xpath('.//span[@class="postal-code"]/text()').extract()

    phone_string = selector.xpath('//li[@class="phonenew"]/text()').extract()[0]
    phone_match = re.search('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}', phone_string)
    if phone_match:
      restaurant['phone'] = phone_match.group(0)
    restaurant['website'] = selector.xpath('//dl[@class="website"]//a[@class="note"]/text()').extract()
    restaurant['hours'] = selector.xpath('//dl[@class="hours"]//span[@class="note"]/text()').extract()
    restaurant['features'] = re.sub('\\\w|\s{3,}', '', selector.xpath('//dl[@class="features"]//dd[@class="note"]/text()').extract()[0])

    url = response.urljoin('menu')
    yield scrapy.Request(url, callback=self.parse_menu, meta={'item':restaurant})

  def parse_menu(self, response):
    restaurant = response.meta['item']
    selector = response.selector
    menu = MenusItem()
    menu['sections'] = []
    menu_child_selectors = selector.xpath('//div[@id="restaurant-menu"]/child::*')
    for idx, sel in enumerate(menu_child_selectors):
      if idx % 3 == 0:
        section = SectionsItem()
        section['name'] = sel.xpath('./text()').extract()
        section['foods'] = []
      if idx % 3 == 1:
        section['description'] = sel.xpath('./text()').extract()
      if idx % 3 == 2:
        row_selectors = sel.xpath('.//tr')
        for row_selector in row_selectors:
          food = FoodsItem()
          food['name'] = row_selector.xpath('./th/cite/text()').extract()
          food['description'] = re.sub('\\xa0', '', row_selector.xpath('./th/text()').extract()[0])
          food['prices'] = []
          prices_list = row_selector.xpath('./td/text()').extract()
          for prices_string in prices_list:
            if prices_string is not '\\xa0':
              prices_string = re.sub('\\xa0', ':', prices_string)
              prices_string = re.sub('\\r\\n\\r\\n', '', prices_string)
              prices_string = re.sub(' \\r\\n ', '~', prices_string)
              prices_string = re.sub('\\\w|\s{3,}', '', prices_string)
              prices_array = prices_string.split('~')
              for price in prices_array:
                if price is not '':
                  food['prices'].append(price)
          section['foods'].append(food)
        menu['sections'].append(section)
      restaurant['menu'] = menu;
    yield restaurant
    
