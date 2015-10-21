# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RestaurantsItem(scrapy.Item):
  name = scrapy.Field()
  address = scrapy.Field()
  cuisine = scrapy.Field()
  phone = scrapy.Field()
  website = scrapy.Field()
  hours = scrapy.Field()
  features = scrapy.Field()
  menu = scrapy.Field()

class AddressesItem(scrapy.Item):
  street_address = scrapy.Field()
  city = scrapy.Field()
  zipcode = scrapy.Field()

class MenusItem(scrapy.Item):
  sections = scrapy.Field()

class SectionsItem(scrapy.Item):
  name = scrapy.Field()
  description = scrapy.Field()
  foods = scrapy.Field()

class FoodsItem(scrapy.Item):
  name = scrapy.Field()
  description = scrapy.Field()
  prices = scrapy.Field()
