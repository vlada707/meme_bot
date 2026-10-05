import os
import random
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


# =========================================================
# НАСТРОЙКИ
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

API_URL = "https://justmeme.wtf/api/v1/templates"


# =========================================================
# 50 ОБЪЯСНЕНИЙ МЕМОВ
# =========================================================

MEMES = {
    "drake hotline bling": "Дрейк отвергает один вариант и одобряет другой. Используется для смешного сравнения двух вариантов.",
    "distracted boyfriend": "Парень отвлекается на другую девушку вместо своей. Используется, когда человек бросает старый вариант ради чего-то нового.",
    "buff doge vs cheems": "Две версии Doge показывают контраст между сильной и слабой версией чего-либо.",
    "two buttons": "Персонаж не может выбрать между двумя кнопками. Используется, когда оба варианта кажутся сложными или неприятными.",
    "batman slapping robin": "Бэтмен бьёт Робина, который говорит что-то очевидное или глупое. Используется для резкого опровержения.",
    "doge": "Doge — известный мем с собакой породы сиба-ину. Используется для ироничных, милых или абсурдных подписей.",
    "this is fine": "Персонаж спокойно сидит среди хаоса и делает вид, что всё нормально.",
    "bad luck brian": "Персонажу постоянно не везёт. Используется для историй о максимально неудачных ситуациях.",
    "stonks": "Stonks — намеренно неправильное написание stocks. Используется иронично для странных финансовых решений.",
    "change my mind": "Человек уверенно высказывает мнение и предлагает другим попробовать его переубедить.",
    "y u no": "Персонаж задаёт вопрос в намеренно неправильной форме. Используется для шуточных претензий.",
    "waiting skeleton": "Скелет ждёт так долго, что превращается в скелет. Используется для шуток о бесконечном ожидании.",
    "mocking spongebob": "Губка Боб передразнивает человека. Используется, когда хочется насмешливо повторить чьи-то слова.",
    "expanding brain": "Несколько уровней мозга показывают якобы всё более умные идеи. Финальный вариант часто абсурдный.",
    "one does not simply": "Используется, когда какое-то действие намного сложнее, чем кажется.",
    "hide the pain harold": "Гарольд улыбается, хотя выглядит так, будто ему плохо. Используется для скрытой неловкости или раздражения.",
    "surprised pikachu": "Пикачу удивляется результату, который был вполне предсказуемым.",
    "is this a pigeon": "Персонаж принимает один объект за другой. Используется, когда кто-то неправильно понимает ситуацию.",
    "say the line bart": "Персонажа просят произнести привычную известную фразу.",
    "epic handshake": "Две разные стороны объединяются из-за общей идеи.",
    "tuxedo winnie the pooh": "Обычный вариант сравнивается с более элегантным или продвинутым вариантом.",
    "trade offer": "Персонаж предлагает сделку: ты получаешь одно, а я получаю другое.",
    "sad pablo escobar": "Пабло Эскобар грустит в ожидании. Используется для шуток о скуке и долгом ожидании.",
    "you guys are getting paid": "Персонаж удивляется, узнав, что за какую-то работу вообще платят.",
    "bernie sanders asking": "Берни Сандерс выглядит так, будто просит или требует что-то.",
    "disaster girl": "Девочка улыбается на фоне хаоса. Используется, когда кто-то слишком доволен происходящим.",
    "always has been": "Герои делают неожиданное открытие, после которого оказывается, что всё было именно так с самого начала.",
    "roll safe": "Используется для шуток в стиле «если не сделать X, то не будет проблемы Y».",
    "left exit 12 off ramp": "Машина резко сворачивает с дороги. Используется для внезапного выбора другого варианта.",
    "woman yelling at cat": "Женщина эмоционально что-то доказывает, а кот выглядит невозмутимо.",
    "gru's plan": "Грю строит идеальный план, но последний пункт полностью ломает всё.",
    "running away balloon": "Используется для сравнения того, от чего человек убегает, и того, к чему он стремится.",
    "clown applying makeup": "Человек постепенно превращает ситуацию в ещё больший цирк.",
    "they are the same picture": "Два изображения объявляются одинаковыми. Используется, когда две вещи очень похожи.",
    "panik kalm panik": "Персонаж сначала паникует, успокаивается, а затем снова паникует.",
    "anakin padme": "Один персонаж говорит что-то оптимистичное, а второй уточняет, действительно ли всё хорошо.",
    "types of headaches": "Несколько изображений показывают разные варианты одной проблемы.",
    "monkey puppet": "Обезьянка смотрит в сторону с неловким выражением. Используется, когда человек делает вид, что ничего не произошло.",
    "well yes but actually no": "Сначала кажется, что человек соглашается, но затем полностью меняет позицию.",
    "grandma finds the internet": "Используется для шуток о непонимании современных технологий.",
    "spider-man pointing": "Два одинаковых Человека-паука показывают друг на друга. Используется, когда два человека обвиняют друг друга в одном и том же.",
    "success kid": "Ребёнок выглядит довольным маленькой победой. Используется, когда что-то неожиданно получилось.",
    "evil kermit": "Обычный человек разговаривает со своей более злой версией. Используется для шуток о внутреннем желании сделать что-то неправильное.",
    "boardroom meeting suggestion": "На совещании человек предлагает идею, после чего его выбрасывают из окна. Используется для шуток о предложениях, которые никто не принимает.",
    "laughing leo": "Леонардо ДиКаприо смеётся и указывает на что-то. Используется как реакция на смешную ситуацию.",
    "wolverine remember": "Росомаха грустит, смотря на фотографию. Используется для ностальгии.",
    "squidward looking out window": "Сквидвард смотрит из окна на то, как другие веселятся. Используется для ощущения, что ты остался в стороне.",
    "i bet he's thinking about other women": "Девушка думает, что парень думает о других девушках, но его мысли оказываются неожиданными.",
    "pepe": "Пепе используется для выражения грусти, неловкости, иронии и других эмоций.",
    "obama cowboy hat": "Обама в ковбойской шляпе используется как абсурдный и ироничный образ.",
}


# =========================================================
# ЗАГРУЗКА МЕМОВ
# =========================================================

def load_50_memes():
    print("Загружаю список мемов...")

    try:
        response = requests.get(
            API_URL,
            params={
                "page": 1,
                "limit": 100
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("success"):
            print("API вернул ошибку.")
            return []

        templates = data.get("templates", [])

        selected = []

        for meme_name in MEMES.keys():

            for template in templates:

                name = template.get("name", "").lower()
                slug = template.get("slug", "").lower()

                search_name = meme_name.lower()

                if (
                    search_name == name
                    or search_name in name
                    or search_name == slug
                    or search_name.replace(" ", "-") == slug
                ):
                    selected.append(template)
                    break

        print(
            f"Найдено шаблонов: {len(selected)} из {len(MEMES)}"
        )

        return selected

    except Exception as error:

        print("Ошибка загрузки:", error)

        return []


# =========================================================
# ГЛАВНОЕ МЕНЮ
# =========================================================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🔥 Случайный мем",
                callback_data="random"
            )
        ],

        [
            InlineKeyboardButton(
                "🤔 Что это значит?",
                callback_data="explain"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# МЕНЮ МЕМА
# =========================================================

def meme_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🤔 Что это значит?",
                callback_data="explain"
            )
        ],

        [
            InlineKeyboardButton(
                "➡️ Следующий мем",
                callback_data="next"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 Главное меню",
                callback_data="menu"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# /START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(

        "😂 Добро пожаловать в Meme Helper!\n\n"
        "Я знаю популярные мем-шаблоны "
        "и могу объяснить, что каждый из них означает.\n\n"
        "Нажми кнопку 👇",

        reply_markup=main_menu()
    )


# =========================================================
# ПОКАЗ МЕМА
# =========================================================

async def show_meme(
    query,
    context
):

    memes = context.application.bot_data.get(
        "memes",
        []
    )

    if not memes:

        await query.message.reply_text(

            "😔 Не удалось загрузить мемы.\n\n"
            "Попробуй перезапустить бота."
        )

        return

    meme = random.choice(memes)

    context.user_data[
        "current_meme"
    ] = meme

    name = meme.get(
        "name",
        "Неизвестный мем"
    )

    image_url = meme.get("url")

    if not image_url:

        await query.message.reply_text(
            "😔 У этого шаблона нет изображения."
        )

        return

    try:

        await query.message.reply_photo(

            photo=image_url,

            caption=f"😂 {name}",

            reply_markup=meme_menu()
        )

    except Exception as error:

        print(
            "Ошибка отправки картинки:",
            error
        )

        await query.message.reply_text(

            f"😂 {name}\n\n"
            "⚠️ Не получилось отправить картинку.",

            reply_markup=meme_menu()
        )


# =========================================================
# ОБЪЯСНЕНИЕ МЕМА
# =========================================================

async def explain_meme(
    query,
    context
):

    meme = context.user_data.get(
        "current_meme"
    )

    if not meme:

        await query.message.reply_text(

            "Сначала выбери мем 👇",

            reply_markup=main_menu()
        )

        return

    name = meme.get(
        "name",
        ""
    )

    slug = meme.get(
        "slug",
        ""
    )

    explanation = None

    for meme_name, text in MEMES.items():

        if (
            meme_name.lower() in name.lower()
            or meme_name.lower() in slug.lower()
        ):

            explanation = text

            break

    if not explanation:

        explanation = (

            "Это популярный мем-шаблон. "
            "Он используется как основа "
            "для добавления собственного текста "
            "и создания шуток."
        )

    message = (

        "🤔 *Что это значит?*\n\n"

        f"😂 *{name}*\n\n"

        f"💡 {explanation}"
    )

    keyboard = [

        [
            InlineKeyboardButton(
                "➡️ Следующий мем",
                callback_data="next"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 Главное меню",
                callback_data="menu"
            )
        ]

    ]

    await query.message.reply_text(

        message,

        parse_mode="Markdown",

        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# ОБРАБОТКА КНОПОК
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "random":

        await show_meme(
            query,
            context
        )

    elif query.data == "next":

        await show_meme(
            query,
            context
        )

    elif query.data == "explain":

        await explain_meme(
            query,
            context
        )

    elif query.data == "menu":

        await query.message.reply_text(

            "🏠 Главное меню 👇",

            reply_markup=main_menu()
        )


# =========================================================
# ЗАПУСК
# =========================================================

def main():

    if not TOKEN:

        raise RuntimeError(
            "Переменная BOT_TOKEN не установлена!"
        )

    memes = load_50_memes()

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.bot_data[
        "memes"
    ] = memes

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print("Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()