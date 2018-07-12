# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BilibiliItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = table = 'bilivideo'
    aid = Field()  #视频ID
    view = Field() #观看次数
    danmaku = Field() #弹幕总数
    reply = Field()  #评论数
    favorite = Field() #收藏数
    coin = Field() #投币数
    share = Field() # 分享数
    like = Field() #喜欢人数
    now_rank = Field()
    his_rank = Field() #最好全站日排行
    no_reprint = Field() 
    copyright = Field() #
    uploadDate = Field() #上传日期
    tname = Field() # 标签
    title = Field() # 标题
    desc = Field() # 描述
    mid = Field() # up主ID
    upname = Field() # up主名称
    sex = Field() #性别
    fans = Field() #粉丝数
    attention = Field() #关注数
