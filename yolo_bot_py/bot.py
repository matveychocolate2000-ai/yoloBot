import os
from collections import Counter

import cv2
import requests
import telebot
from imageai.Detection import ObjectDetection
from telebot import types

TOKEN = "bot_token"

bot = telebot.TeleBot(TOKEN)

exec_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(exec_path, "yolov3.pt"))
detector.loadModel()

bot.set_my_commands([
    types.BotCommand("start", "Главное меню"),
    types.BotCommand("weather", "Погода"),
])


def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Отправить фото", "Погода")
    return keyboard


@bot.message_handler(commands=["start"])
def start(message):
    text = (
        "Привет. Я бот для анализа фото и прогноза погоды.\n\n"
        "Используй кнопки ниже или команду /weather."
    )
    bot.send_message(message.chat.id, text, reply_markup=get_keyboard())


@bot.message_handler(func=lambda m: m.text in ["Погода", "/weather"])
def weather(message):
    msg = bot.send_message(message.chat.id, "Введите название города:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_weather)


def get_weather(message):
    city = message.text.strip()
    try:
        url = f"https://wttr.in/{city}?format=j1&lang=ru"
        res = requests.get(url, timeout=10)
        
        if res.status_code == 200:
            data = res.json()["current_condition"][0]
            temp = data["temp_C"]
            feels = data["FeelsLikeC"]
            desc = data["lang_ru"][0]["value"] if "lang_ru" in data and data["lang_ru"] else data["weatherDesc"][0]["value"]
            humidity = data["humidity"]
            wind = data["windspeedKmph"]

            text = (
                f"Погода в городе {city.capitalize()}:\n"
                f"Температура: {temp}°C (ощущается как {feels}°C)\n"
                f"Описание: {desc}\n"
                f"Влажность: {humidity}%\n"
                f"Ветер: {wind} км/ч"
            )
        else:
            text = "Город не найден. Попробуйте еще раз."
    except Exception as e:
        text = f"Ошибка получения данных: {e}"

    bot.send_message(message.chat.id, text, reply_markup=get_keyboard())


def process_image(input_path, output_path):
    detections = detector.detectObjectsFromImage(
        input_image=input_path,
        output_image_path=None,
        minimum_percentage_probability=50,
    )

    image = cv2.imread(input_path)
    h, w, _ = image.shape
    names = []

    for det in detections:
        name = det["name"]
        x1, y1, x2, y2 = det["box_points"]
        
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        if (x2 - x1) > w * 0.7 or (y2 - y1) > h * 0.7:
            continue

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"{name} {int(det['percentage_probability'])}%",
            (x1, max(15, y1 - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )
        names.append(name)

    cv2.imwrite(output_path, image)
    return Counter(names)


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    uid = message.from_user.id
    input_path = f"input_{uid}.jpg"
    output_path = f"output_{uid}.jpg"

    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)

        with open(input_path, "wb") as f:
            f.write(downloaded)

        counts = process_image(input_path, output_path)

        if counts:
            text = "Результаты анализа:\n\n"
            for name, count in counts.items():
                text += f"- {name.capitalize()}: {count} шт.\n"
            text += f"\nВсего объектов: {sum(counts.values())}"
        else:
            text = "Объекты не обнаружены."

        bot.send_message(message.chat.id, text)

        with open(output_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=get_keyboard())

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}", reply_markup=get_keyboard())

    finally:
        for path in [input_path, output_path]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    bot.infinity_polling()