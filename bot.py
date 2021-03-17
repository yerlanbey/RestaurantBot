from telebot import types
import telebot
import psycopg2
import math

bot = telebot.TeleBot("")
user_data ={}
con = psycopg2.connect(
    host = "localhost",
    database = "restaurants",
    user = "",
    password = "",
    port = ""
)



class User:
    def __init__(self, restourant_name):
        self.restourant_name = restourant_name




cities = ["Алматы","Нур-Султан","Москва","Санкт-Петербург"]
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        keyboard_search = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons_search = [types.KeyboardButton(text=city) for city in ["По городам","По ресторанам","По кухням"]]
        keyboard_search.add(*buttons_search)
        msg = bot.send_message(message.chat.id, "Я бот поисковик ресторанов, выберите как вы будете искать",reply_markup=keyboard_search)
        bot.register_next_step_handler(msg,process_submenu_step)
    except Exception as e:
        bot.reply_to(message,"Ooops")





def process_submenu_step(message):
    if message.text == "По городам":
        keyboard_city = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons_city = [types.KeyboardButton(text=city) for city in cities]
        keyboard_city.add(*buttons_city)
        msg = bot.send_message(message.chat.id, "Я бот поисковик ресторанов, где вы ищите ресторан?",reply_markup=keyboard_city)
        bot.register_next_step_handler(msg, process_geo_step)
    elif message.text == "По ресторанам":
        msg = bot.send_message(message.chat.id, "Напишите имя ресторана, чтобы узнать подробнее о ресторане")
        bot.register_next_step_handler(msg, process_geo_step)
    elif message.text == "По кухням":
        cuisine_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons_cuisine = [types.KeyboardButton(text=city) for city in ["Европейская","Азиатская","Восточноевропейская","Турецкая"]]
        cuisine_keyboard.add(*buttons_cuisine)
        msg  = bot.send_message(message.chat.id, "Напишите или нажмите на кнопку кухни, и узнайте больше о ресторане",reply_markup=cuisine_keyboard)
        bot.register_next_step_handler(msg, process_geo_step)




@bot.message_handler(content_types=["location"])
def process_geo_step(message):
    global query_name
    query_name = message.text
    print(query_name)
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.row(button_geo)
        msg = bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=keyboard)
        bot.register_next_step_handler(msg,process_wait_step)
    except Exception as e:
        bot.reply_to(message, "Ooops")


def process_wait_step(message):
    global query_name
    print(query_name)
    bot.send_message(message.chat.id, "Пожалуйста ожидайте несколько секунд")
    sql = "select * from restaurant_bot where city = "+"'" +query_name + "'"+" or restaurant_name = '"+query_name+"' or cuisine LIKE '%" + query_name+"%'"
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 0 :
        bot.reply_to(message, "У нас нету такого ресторана")
    for j in rows:
        if "http" in j[5]:
            markup = types.InlineKeyboardMarkup()
            btn_my_site = types.InlineKeyboardButton(text='Меню', url=j[5])
            markup.add(btn_my_site)
            #if distance < 603:
            if query_name in j[0] :
                R = 6373.0
                userLat = math.radians(message.location.latitude)
                userLon = math.radians(message.location.longitude)
                resLat = math.radians(float(j[7]))
                resLon = math.radians(float(j[8]))
                dlon = resLon - userLon
                dlat = resLat - userLat
                a = math.sin(dlat / 2) ** 2 + math.cos(userLat) * math.cos(resLat) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c
                if distance < 604:
                    bot.send_message(message.chat.id, (str("Имя ресторана: ") + j[
                                1] + "\n\n" + str(": Адрес") + j[2] + "\n\n" + str("Контакты: ") + j[3]
                                                               + "\n\n" + str("Кухня: ") + j[4] + "\n\n" + str(
                                        "Рейтинг по 5 бальной шкале: ") + j[6]), reply_markup=markup)
                    bot.send_location(message.chat.id, j[7], j[8])
            elif query_name in j[1]:
                R = 6373.0
                userLat = math.radians(message.location.latitude)
                userLon = math.radians(message.location.longitude)
                resLat = math.radians(float(j[7]))
                resLon = math.radians(float(j[8]))
                dlon = resLon - userLon
                dlat = resLat - userLat
                a = math.sin(dlat / 2) ** 2 + math.cos(userLat) * math.cos(resLat) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c
                bot.send_message(message.chat.id, (str("Имя ресторана: ") + j[
                    1] + "\n\n" + str(": Адрес") + j[2] + "\n\n" + str("Контакты: ") + j[3]
                                                   + "\n\n" + str("Кухня: ") + j[4] + "\n\n" + str(
                            "Рейтинг по 5 бальной шкале: ") + j[6]),reply_markup=markup)
                bot.send_location(message.chat.id, j[7], j[8])
            elif query_name in j[4]:
                R = 6373.0
                userLat = math.radians(message.location.latitude)
                userLon = math.radians(message.location.longitude)
                resLat = math.radians(float(j[7]))
                resLon = math.radians(float(j[8]))
                dlon = resLon - userLon
                dlat = resLat - userLat
                a = math.sin(dlat / 2) ** 2 + math.cos(userLat) * math.cos(resLat) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c
                if distance < 604:
                    bot.send_message(message.chat.id, (str("Имя ресторана: ") + j[
                        1] + "\n\n" + str(": Адрес") + j[2] + "\n\n" + str("Контакты: ") + j[3]
                                                       + "\n\n" + str("Кухня: ") + j[4] + "\n\n" + str(
                                "Рейтинг по 5 бальной шкале: ") + j[6]), reply_markup=markup)
                    bot.send_location(message.chat.id, j[7], j[8])
        else:
            if query_name in j[0]:
                R = 6373.0
                userLat = math.radians(message.location.latitude)
                userLon = math.radians(message.location.longitude)
                resLat = math.radians(float(j[7]))
                resLon = math.radians(float(j[8]))
                dlon = resLon - userLon
                dlat = resLat - userLat
                a = math.sin(dlat / 2) ** 2 + math.cos(userLat) * math.cos(resLat) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R *c
                if distance < 604:
                    bot.send_message(message.chat.id, (str("Имя ресторана: ") + j[
                                1] + "\n\n" + str(": Адрес") + j[2] + "\n\n" + str("Контакты: ") + j[3]
                                                               + "\n\n" + str("Кухня: ") + j[4] + "\n\n" + str(
                                        "Рейтинг по 5 бальной шкале: ") + j[6]
                                                               + "\n\n" + str("Меню: ") + j[5]))
                    bot.send_location(message.chat.id, j[7], j[8])
            elif query_name in j[1]:
                R = 6373.0
                userLat = math.radians(message.location.latitude)
                userLon = math.radians(message.location.longitude)
                resLat = math.radians(float(j[7]))
                resLon = math.radians(float(j[8]))
                dlon = resLon - userLon
                dlat = resLat - userLat
                a = math.sin(dlat / 2) ** 2 + math.cos(userLat) * math.cos(resLat) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c
                bot.send_message(message.chat.id, (str("Имя ресторана: ") + j[
                    1] + "\n\n" + str(": Адрес") + j[2] + "\n\n" + str("Контакты: ") + j[3]
                                                   + "\n\n" + str("Кухня: ") + j[4] + "\n\n" + str(
                            "Рейтинг по 5 бальной шкале: ") + j[6]))
                bot.send_location(message.chat.id, j[7], j[8])
            elif query_name in j[4]:
                R = 6373.0
                userLat = math.radians(message.location.latitude)
                userLon = math.radians(message.location.longitude)
                resLat = math.radians(float(j[7]))
                resLon = math.radians(float(j[8]))
                dlon = resLon - userLon
                dlat = resLat - userLat
                a = math.sin(dlat / 2) ** 2 + math.cos(userLat) * math.cos(resLat) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c
                if distance < 604:
                    bot.send_message(message.chat.id, (str("Имя ресторана: ") + j[
                        1] + "\n\n" + str(": Адрес") + j[2] + "\n\n" + str("Контакты: ") + j[3]
                                                   + "\n\n" + str("Кухня: ") + j[4] + "\n\n" + str(
                            "Рейтинг по 5 бальной шкале: ") + j[6]))
                    bot.send_location(message.chat.id, j[7], j[8])




bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()



if __name__ == '__main__':
    bot.polling(none_stop=True)



con.close()

