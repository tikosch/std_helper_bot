from re import sub
import telebot
import config
from datetime import datetime
import pymongo
from telebot import types
import random
import os
import pafy
from cryptography.fernet import Fernet

client = pymongo.MongoClient("mongodb+srv://tikosch:qwerty123@cluster0.zjsr8ku.mongodb.net/bdbot?retryWrites=true&w=majority")
db = client["bdbot"]
users = db["Users"]
homeworks = db["Homeworks"]
musics = db["Music"]
videos = db["Video"]
# user = {"_id": 123, "name": "Arnur"}
# users.insert_one(user)


class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance
bot = SingletonClass()

bot = telebot.TeleBot(config.token)

def download_music(file_name, link):
    ydl_opts = {
        'outtmpl': './'+file_name,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
        'prefer_ffmpeg': True
    }


def save_user_to_db(user):
    result = users.replace_one({"id": user['id']}, user, upsert=True)
def home_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📚 Add homework")
    btn2 = types.KeyboardButton("🗓 See deadlines")
    btn3 = types.KeyboardButton("✅ Finish homework")
    btn4 = types.KeyboardButton("🔴 Youtube Link")
    btn5 = types.KeyboardButton("📂 All Completed homeworks")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup
def deadlines_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("For 2 days")
    btn2 = types.KeyboardButton("For week")
    btn3 = types.KeyboardButton("For month")
    btn4 = types.KeyboardButton("🏠Go home")
    markup.add(btn1, btn2, btn3, btn4)
    return markup
def homeBtn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn4 = types.KeyboardButton("🏠Go home")
    markup.add(btn4)
    return markup
def a_v():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn4 = types.KeyboardButton("Video")
    btn5 = types.KeyboardButton("Audio")
    markup.add(btn4,btn5)
    return markup
def youtube_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("Delete Song")
    btn3 = types.KeyboardButton("Download Song")
    btn4 = types.KeyboardButton("🏠Go home")
    markup.add(btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    # Generate a key for encryption
    key = Fernet.generate_key()

    # Initialize a Fernet cipher object using the key
    cipher = Fernet(key)
    user = {}
    ciphertext = cipher.encrypt(message.from_user.first_name.encode())
    user['id'] = message.from_user.id
    user['first_name'] = ciphertext
    user['last_name']= message.from_user.last_name
    user['username'] =  message.from_user.username
    users.insert_one(user)
    save_user_to_db(user)
    markup = home_button()

    bot.send_message(message.chat.id, "Welcome to <b>Std_Helper!</b> {0.first_name}!\nI can help you to organize your homeworks, track deadlines and track finished homeworks!"
    .format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def home(message):
    if message.chat.type == 'private':
        if message.text == "📚 Add homework":
            user = {}
            user['id'] = message.from_user.id
            user['is_completed'] = False
            bot.send_message(message.chat.id, "Please enter the subject: ", reply_markup=homeBtn())
            bot.register_next_step_handler(message, lambda m: enter_subject(m, user))
        elif message.text == "🗓 See deadlines":
            bot.send_message(message.chat.id, "Choose the period of deadlines: ", reply_markup=deadlines_buttons())
            bot.register_next_step_handler(message,choose_period_of_deadlines)
        elif message.text == "✅ Finish homework":
            finish_homework(message)
        elif message.text == "📂 All Completed homeworks":
            get_completed_hws(message)
        elif message.text == "🔴 Youtube Link":

            bot.send_message(message.chat.id, 'Go make some things', parse_mode='html', reply_markup=youtube_btn())
            try:
                bot.register_next_step_handler(message, youtube)
            except:
                bot.send_message(message.chat.id, 'Send me the right link', parse_mode='html')

        else:
            bot.send_message(message.chat.id, "Select only buttons below!", reply_markup=home_button())
            
def youtube(message):
    if message.chat.type == 'private':
        if message.text == "🏠Go home":
            bot.send_message(message.chat.id, "Going home...", reply_markup=home_button())
            bot.register_next_step_handler(message,home)
        elif message.text == "Delete Song":
            bot.send_message(message.chat.id, "Going to delete by the title:")
            choose_song(message)
        elif message.text == "Download Song":
            bot.send_message(message.chat.id, "Going to download:", reply_markup=a_v())
            bot.register_next_step_handler(message,choice)
def choose_song(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    all_songs = musics.find({})
    for i in all_songs:
        btn1 = types.KeyboardButton(f"📄{i['title']}")
        markup.add(btn1)
    bot.send_message(message.chat.id, "Choose song to delete: " , reply_markup=markup, parse_mode='html')
    bot.register_next_step_handler(message, delete_song)
def delete_song(message):
    try:
        message.text = message.text.replace("📄", "")
        os.remove("/Users/tikosch/Desktop/python/telegramBot/music/{}.webm".format(message.text))
        musics.delete_many({"title": message.text})
        bot.send_message(message.chat.id, "{} has been deleted".format(message.text) , reply_markup=youtube_btn(), parse_mode='html')
    except OSError as e:
        bot.send_message(message.chat.id, f"Has not been deleted {e}", reply_markup=youtube_btn(), parse_mode='html')

def enter_subject(message, user):
    if message.text == "🏠Go home":
        bot.send_message(message.chat.id, "Going home...", reply_markup=home_button())
        bot.register_next_step_handler(message,home)
    else:
        subject_name = message.text
        user['subject'] = subject_name
        bot.send_message(message.chat.id, f"Subject is: <b>{subject_name}</b>, enter the assignment: ", parse_mode='html', reply_markup=homeBtn())
        bot.register_next_step_handler(message, lambda m: enter_assignment(m, user))

def enter_assignment(message, user):
    if message.text == "🏠Go home":
        bot.send_message(message.chat.id, "Going home...", reply_markup=home_button())
        bot.register_next_step_handler(message,home)
    else:
        assignment = message.text
        user['assignment'] = assignment
        bot.send_message(message.chat.id, f"Assignment is: <b>{assignment}</b>, enter the deadline in format YYYY-MM-DD: ", parse_mode='html', reply_markup=homeBtn())
        bot.register_next_step_handler(message, lambda m: enter_date(m, user))

def enter_date(message, user):
    if message.text == "🏠Go home":
        bot.send_message(message.chat.id, "Going home...", reply_markup=home_button())
        bot.register_next_step_handler(message,home)
    else:
        date_text = message.text
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            try:
                user['deadline'] = date_text
                homeworks.insert_one(user)
                users.update_one({"id": user['id']},{"$push":{"deadlines": user}})
            except:
                bot.send_message(message.chat.id, f"Oops, something went wrong, try again.", parse_mode='html', reply_markup=homeBtn())
                pass
            bot.send_message(message.chat.id, f"You have successfully saved the assignment!", parse_mode='html', reply_markup=home_button())
        
        except ValueError:
            bot.send_message(message.chat.id, f"Oops, wrong date. Follow pattern YYYY-MM-DD ", parse_mode='html', reply_markup=homeBtn())
            bot.register_next_step_handler(message, lambda m: enter_date(m, user))
            pass
    
def choose_period_of_deadlines(message):
    if message.chat.type == 'private':
        if message.text == "For 2 days":
            for_days(message, 2)
        elif message.text == "For week":
            for_days(message, 7)
        elif message.text == "For month":
            for_days(message, 30)
        elif message.text == "🏠Go home":
            bot.send_message(message.chat.id, "Going home...", reply_markup=home_button())
            bot.register_next_step_handler(message,home)
        else:
            bot.send_message(message.chat.id, "Oops, choose only buttons below.", reply_markup=deadlines_buttons() )

def for_days(message,number_of_days):
    user_id = message.from_user.id
    HWs = homeworks.find({'id':user_id})
    today = datetime.today().day
    counter = 0
    Text = ""
    for works in HWs:
        if works['is_completed'] == False:
            deadline = works['deadline']
            date = datetime.strptime(deadline, "%Y-%m-%d")
            days = date.day
            if days-today <= number_of_days:
                counter = counter + 1
                Text = Text + f"{counter}. <b>{works['subject']}</b> - {works['assignment']} with deadline {works['deadline']}\n"
    if counter == 0:
        bot.send_message(message.chat.id, f"Hey, you can chill out. You don't have any deadlines for {number_of_days} days!📚" , reply_markup=home_button(), parse_mode='html')
    else:
        bot.send_message(message.chat.id, Text , reply_markup=home_button(), parse_mode='html')
        if counter == 1:
            bot.send_message(message.chat.id, "You have only 1 assignment. Easy peasy!🍋" , reply_markup=home_button(), parse_mode='html')
        if counter == 2:
            bot.send_message(message.chat.id, "You have 2 assignments. Not bad!" , reply_markup=home_button(), parse_mode='html')
        if counter >= 3:
            bot.send_message(message.chat.id, "Hey, you have a lot of work to do. Let's get done all of them!🤓" , reply_markup=home_button(), parse_mode='html')
    bot.register_next_step_handler(message,home)

def get_music(message):
    pass

def choice(message):
    if message.text == "Video":
        bot.send_message(message.chat.id, "Send me the link" , reply_markup=youtube_btn(), parse_mode='html')
        bot.register_next_step_handler(message, download_video)
    elif message.text == "Audio":
        bot.send_message(message.chat.id, "Send me the link" , reply_markup=youtube_btn(), parse_mode='html')
        bot.register_next_step_handler(message, download_audio)
    else:
        bot.send_message(message.chat.id, "Going home...", reply_markup=home_button())
        bot.register_next_step_handler(message,home)

def download_audio(message):
    audio = pafy.new(message.text)
    stream = audio.audiostreams
    title = audio.title
    try:
        with open("/Users/tikosch/Desktop/python/telegramBot/music/{}.mp3".format(title), 'rb') as audio:
            bot.send_audio(message.chat.id, audio=audio)
            bot.send_message(message.chat.id, "Done ✅", reply_markup=youtube_btn())
            bot.register_next_step_handler(message,youtube)
    except:    
        music = {}
        music['title'] = title
        music['link'] = message.text
        needed = {}
        needed['duration'] = audio.duration
        needed['viewcount'] = int(audio.viewcount)
        needed['rating'] = audio.rating
        musics.insert_one(music)
        musics.update_one({"link": music['link']}, {"$push": {"description": needed}})
        stream[2].download("/Users/tikosch/Desktop/python/telegramBot/music")
        with open("/Users/tikosch/Desktop/python/telegramBot/music/{}.webm".format(title), 'rb') as audio:
            bot.send_audio(message.chat.id, audio=audio)
        audio.close()
        bot.send_message(message.chat.id, "Done ✅", reply_markup=youtube_btn())
        bot.register_next_step_handler(message,youtube)


def download_video(message):
    video = pafy.new(message.text)
    stream = video.videostreams
    title = video.title
    try:
        with open("/Users/tikosch/Desktop/python/telegramBot/music/{}.mp4".format(title), 'rb') as video:
            bot.send_video(message.chat.id, video=video)
            bot.send_message(message.chat.id, "Done ✅", reply_markup=youtube_btn())
            bot.register_next_step_handler(message,youtube)
    except:    
        vid = {}
        vid['title'] = title
        vid['link'] = message.text
        needed = {}
        needed['duration'] = video.duration
        needed['viewcount'] = int(video.viewcount)
        needed['rating'] = video.rating
        videos.insert_one(vid)
        videos.update_one({"link": vid['link']}, {"$push": {"description": needed}})
        stream[0].download("/Users/tikosch/Desktop/python/telegramBot/video")
        with open("/Users/tikosch/Desktop/python/telegramBot/video/{}.mp4".format(title), 'rb') as video:
            bot.send_video(message.chat.id, video=video)
        video.close()
        bot.send_message(message.chat.id, "Done ✅", reply_markup=youtube_btn())
        bot.register_next_step_handler(message,youtube)
#Finish homework steps
def finish_homework(message):
    user_id = message.from_user.id
    HWs = homeworks.find({'id':user_id})
    Text = ""
    counter = 0
    for works in HWs:
        if works['is_completed'] == False:
            counter = counter + 1
            Text = Text + f"{counter}. <b>{works['subject']}</b> - {works['assignment']} with deadline {works['deadline']}\n"
    if counter == 0:
        bot.send_message(message.chat.id, f"Hey, you can chill out. You don't have any homeworks to finish." , reply_markup=home_button(), parse_mode='html')
    else:
        bot.send_message(message.chat.id, Text , parse_mode='html')
        choose_hw_ids(message, counter)

def choose_hw_ids(message, counter):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    HWs = homeworks.find({'id':user_id, 'is_completed':False})
    for i in HWs:
        btn1 = types.KeyboardButton(f"📄{i['subject']} - {i['assignment']}")
        markup.add(btn1)
    bot.send_message(message.chat.id, f"Choose finished homework's ID: " , reply_markup=markup, parse_mode='html')
    bot.register_next_step_handler(message, set_finish_to_hw)
    

def set_finish_to_hw(message):
    if message.text == "🏠Go home":
        bot.send_message(message.chat.id, "Going home...", reply_markup=home_button())
        bot.register_next_step_handler(message,home)
    else:
        try:
            user_id = message.from_user.id
            text = message.text
            text = text.replace("📄",'')
            splitted = text.split("-")
            print(text, splitted)
            subject = splitted[0].strip()
            assignment = splitted[1].strip()
            
            HWs = homeworks.update_one(
                {'id':user_id,'subject':subject,'assignment':assignment},
                {"$set":{"is_completed": True}
            })
            HW = users.update_one(
                {'id':user_id},
                {"$pop":{"deadlines": 1}
            })
            bot.send_message(message.chat.id, f"Successully finished <b>{subject}</b>!" , reply_markup=home_button(), parse_mode='html')
            bot.register_next_step_handler(message, home)
        except:
            bot.send_message(message.chat.id, f"Oops, you entered wrong ID, try again!", parse_mode='html', reply_markup=homeBtn())
            bot.register_next_step_handler(message, set_finish_to_hw)
            
            pass



#all completed HWs
def get_completed_hws(message):
    user_id = message.from_user.id
    HWs = homeworks.find({'id':user_id, 'is_completed':True})
    counter = 0
    Text = ""
    for works in HWs:
            counter = counter + 1
            Text = Text + f"✅{counter}. <b>{works['subject']}</b> - {works['assignment']} with deadline {works['deadline']}\n"
    if counter == 0:
        bot.send_message(message.chat.id, f"You don't have completed any homeworks:(" , reply_markup=home_button(), parse_mode='html')
    else:
        bot.send_message(message.chat.id, Text , parse_mode='html')
        bot.send_message(message.chat.id, f"Keep it going! You already have done {counter} homeworks." , reply_markup=home_button(), parse_mode='html')
    bot.register_next_step_handler(message,home)
bot.enable_save_next_step_handlers(delay=1)
bot.polling(none_stop=True)


