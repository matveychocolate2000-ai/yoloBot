# 🤖 YOLO Bot — Telegram-бот для распознавания объектов и прогноза погоды

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0.svg?logo=telegram)](https://core.telegram.org/bots)
[![YOLOv3](https://img.shields.io/badge/Model-YOLOv3-red.svg)](https://pjreddie.com/darknet/yolo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Open-source Telegram-бот на Python, который **распознаёт объекты на фотографиях** с помощью нейросети **YOLOv3** и показывает **прогноз погоды** для любого города.

---

## 📌 Описание

Бот объединяет две полезные функции в одном интерфейсе:

1. **Анализ изображений.** Пользователь отправляет фото — бот прогоняет его через предобученную модель **YOLOv3**, находит объекты, рисует вокруг них рамки с подписями и процентом уверенности, а затем возвращает:
   - обработанное изображение с разметкой;
   - текстовый отчёт со списком найденных объектов и их количеством.
2. **Прогноз погоды.** По команде `/weather` или кнопке «Погода» бот запрашивает у сервиса [wttr.in](https://wttr.in) текущую погоду в указанном городе (температура, ощущаемая температура, описание, влажность, ветер) и присылает её в чат.

### Как это работает

- Модель **YOLOv3** (`yolov3.pt`) загружается один раз при старте бота через библиотеку `imageai`.
- При получении фото бот скачивает его, прогоняет через детектор (`minimum_percentage_probability=50`), фильтрует слишком крупные боксы (занимающие >70% кадра — обычно это ложные срабатывания), рисует рамки через **OpenCV** и подсчитывает объекты с помощью `collections.Counter`.
- Временные файлы (`input_<uid>.jpg`, `output_<uid>.jpg`) создаются и удаляются автоматически.

---

## ✨ Возможности

- 📷 Распознавание объектов на фото (YOLOv3)
- 📊 Подсчёт найденных объектов по классам
- 🖼️ Возврат изображения с нарисованными рамками и подписями
- 🌤️ Прогноз погоды по названию города (wttr.in, поддержка русского языка)
- ⌨️ Удобное меню с кнопками (`ReplyKeyboardMarkup`) и командами бота
- 🧹 Автоматическая очистка временных файлов

---

## 📸 Скриншоты

> Добавь свои скриншоты в папку `docs/` и замени ссылки ниже.

**Главное меню:**

![Главное меню](docs/screenshot_menu.png)

**Результат распознавания:**

![Распознавание объектов](docs/screenshot_detection.png)

**Прогноз погоды:**

![Погода](docs/screenshot_weather.png)

---

## 🗂️ Структура проекта

```
yolo_bot_py/
├── .vscode/
│   └── settings.json       # настройки окружения VS Code
├── bot.py                  # основной код бота
├── yolov3.pt               # веса модели YOLOv3 (не входит в репозиторий)
├── labels.txt              # список классов модели
├── requirements.txt        # зависимости
├── LICENSE                 # лицензия MIT
└── README.md               # этот файл
```

---

## ⚙️ Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/<твой-username>/yolo_bot_py.git
cd yolo_bot_py
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Загрузка весов модели

Скачай `yolov3.pt` (например, из официального репозитория [imageai](https://github.com/OlafenwaMoses/ImageAI/releases)) и положи его в корень проекта.

### 5. Настройка токена бота

В файле `bot.py` замени:

```python
TOKEN = "bot_token"
```

на токен, полученный у [@BotFather](https://t.me/BotFather).

### 6. Запуск

```bash
python bot.py
```

---

## 📦 requirements.txt

```txt
pyTelegramBotAPI>=4.14.0
imageai>=3.0.3
opencv-python>=4.8.0
requests>=2.31.0
numpy>=1.24.0
tensorflow>=2.13.0
keras>=2.13.0
pillow>=10.0.0
```

> ⚠️ `imageai` требует `tensorflow` и `keras`. Если возникают проблемы совместимости — устанавливай в указанном порядке.

---

## 🧠 Используемая модель

| Параметр | Значение |
|---|---|
| Архитектура | YOLOv3 |
| Формат весов | `yolov3.pt` |
| Библиотека | `imageai.Detection.ObjectDetection` |
| Порог уверенности | 50% |
| Классы | 80 (стандартный COCO) |

---

## 🛠️ Используемые технологии

- **Python 3.9+**
- **pyTelegramBotAPI** — работа с Telegram Bot API
- **ImageAI + YOLOv3** — детекция объектов
- **OpenCV** — отрисовка рамок и подписей
- **requests** — запросы к wttr.in
- **collections.Counter** — подсчёт объектов

---

## 🤝 Вклад в проект

Pull request'ы приветствуются! Если нашёл баг или есть идея:

1. Форкни репозиторий
2. Создай ветку: `git checkout -b feature/my-feature`
3. Закоммить: `git commit -m "Add my feature"`
4. Запушь: `git push origin feature/my-feature`
5. Открой Pull Request

---

## 📄 Лицензия

Проект распространяется под лицензией **MIT**. Подробности — в файле [LICENSE](LICENSE).

---

## 👤 Автор

**<Твоё имя>**
- GitHub: [@<твой-username>](https://github.com/<твой-username>)
- Telegram: [@<твой-ник>](https://t.me/<твой-ник>)
