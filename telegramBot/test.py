# from re import sub
# import telebot
# import config
# from datetime import datetime
# import pymongo
# from telebot import types


# client = pymongo.MongoClient("mongodb+srv://tikosch:qwerty123@cluster0.zjsr8ku.mongodb.net/bdbot?retryWrites=true&w=majority")
# db = client["bdbot"]
# users = db["Users"]
# homeworks = db["Homeworks"]
# # user = {"_id": 112, "chat_id": 123, "name": "Darkhan"}
# # users.insert_one(user)

# hw = {"chat_id": 669325851, "is_completed": True, "subject": "Calculus", "assignment": "assign1", "deadline": "2022-12-26"}
# homeworks.insert_one(hw)
from re import sub
import telebot
import config
from datetime import datetime
import pymongo
from telebot import types
import random
import os
import pafy
import youtube_dl

def get_music(message):
    video = pafy.new(message)
    print("1 - V\n2-A")
    a = int(input())
    if a == 1:
        stream = video.videostreams
    elif a == 2:
        stream = video.audiostreams
    else:
        print("invalid choice")
    for i in stream:
        print(i.extension, i.get_filesize())
    
    select = int(input())
    stream[select].download("/Users/tikosch/Desktop/python/telegramBot/music")

get_music("https://www.youtube.com/watch?v=VeOqfhz21Lk")


