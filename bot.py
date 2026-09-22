import asyncio, os, json, logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, PreCheckoutQuery,
    SuccessfulPayment,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8639907128:AAG5r4mx868b1a1fSrS8CflW1GluY2EURKQ"
ADMIN_ID = 8813054628
CHANNEL_ID = "@WorlldStudios"
CHANNEL_URL = "https://t.me/WorlldStudios"
FREE_URL = "https://t.me/FreeeWorlld"
USERS_DB = "users.json"
WORLDS_DB = "worlds.json"

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

TEXTS = {
"ru": {
"choose_lang": "🌍 <b>Выбери язык</b>",
"menu": "🏠 <b>Главное меню</b>",
"btn_check": "📢 Проверить подписку",
"btn_worlds": "🔐 Приватные миры",
"btn_settings": "⚙️ Настройки",
"sub_need": "❌ <b>Сначала подпишись на канал.</b>\n\nПосле подписки нажми «Проверить подписку».",
"sub_ok": "✅ <b>Подписка подтверждена.</b>\n\nДобро пожаловать!",
"sub_btn": "📢 Подписаться",
"worlds_hdr": "🔐 <b>Приватные миры</b>\n\nВыбери мир:",
"buy_hdr": "💎 <b>Приобрести мир можно за</b>",
"btn_buy": "⭐ Купить за {price} звёзд",
"btn_free": "🎁 Бесплатно",
"paid_ok": "✅ <b>Спасибо за покупку!</b>\n\nАвтор отправит мир тебе в личку.",
"settings_hdr": "⚙️ <b>Настройки</b>\n\nТекущий язык: Русский 🇷🇺",
"btn_chlang": "🌐 Сменить язык",
"btn_back": "⬅️ Назад",
"btn_continue": "🎞️ Продолжить",
"no_worlds": "Пока нет миров.",
},
"en": {
"choose_lang": "🌍 <b>Choose your language</b>",
"menu": "🏠 <b>Main menu</b>",
"btn_check": "📢 Check subscription",
"btn_worlds": "🔐 Private worlds",
"btn_settings": "⚙️ Settings",
"sub_need": "❌ <b>Subscribe first.</b>\n\nAfter subscribing, press «Check subscription».",
"sub_ok": "✅ <b>Subscription confirmed.</b>\n\nWelcome!",
"sub_btn": "📢 Subscribe",
"worlds_hdr": "🔐 <b>Private worlds</b>\n\nChoose a world:",
"buy_hdr": "💎 <b>Get this world for</b>",
"btn_buy": "⭐ Buy for {price} stars",
"btn_free": "🎁 Free",
"paid_ok": "✅ <b>Thank you for purchase!</b>\n\nAuthor will send the world to your DM.",
"settings_hdr": "⚙️ <b>Settings</b>\n\nCurrent language: English 🇬🇧",
"btn_chlang": "🌐 Change language",
"btn_back": "⬅️ Back",
"btn_continue": "🎞️ Continue",
"no_worlds": "No worlds yet.",
},
"hi": {
"choose_lang": "🌍 <b>अपनी भाषा चुनें</b>",
"menu": "🏠 <b>मुख्य मेनू</b>",
"btn_check": "📢 सब्सक्रिप्शन जांचें",
"btn_worlds": "🔐 निजी दुनिया",
"btn_settings": "⚙️ सेटिंग्स",
"sub_need": "❌ <b>पहले सब्सक्राइब करें।</b>",
"sub_ok": "✅ <b>सब्सक्रिप्शन की पुष्टि हो गई।</b>",
"sub_btn": "📢 सब्सक्राइब करें",
"worlds_hdr": "🔐 <b>निजी दुनिया</b>",
"buy_hdr": "💎 <b>यह दुनिया प्राप्त करें</b>",
"btn_buy": "⭐ {price} सितारों के लिए खरीदें",
"btn_free": "🎁 मुफ़्त",
"paid_ok": "✅ <b>खरीदारी के लिए धन्यवाद!</b>",
"settings_hdr": "⚙️ <b>सेटिंग्स</b>",
"btn_chlang": "🌐 भाषा बदलें",
"btn_back": "⬅️ वापस",
"btn_continue": "🎞️ जारी रखें",
"no_worlds": "अभी कोई दुनिया नहीं।",
},
}

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

users = load_json(USERS_DB)
worlds = load_json(WORLDS_DB)
user_world = {}

def t(uid, key, **kw):
    lang = users.get(str(uid), "ru")
    txt = TEXTS[lang].get(key, TEXTS["ru"][key])
    return txt.format(**kw) if kw else txt

def set_user_lang(uid, lang):
    users[str(uid)] = lang
    save_json(USERS_DB, users)

def get_lang(uid):
    return users.get(str(uid))

async def is_subbed(uid):
    try:
        m = await bot.get_chat_member(CHANNEL_ID, uid)
        return m.status in ("creator", "administrator", "member")
    except:
        return False

def kb_lang():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="lang:hi")],
    ])

def kb_menu(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_check"), callback_data="check")],
        [InlineKeyboardButton(text=t(uid, "btn_worlds"), callback_data="worlds")],
        [InlineKeyboardButton(text=t(uid, "btn_settings"), callback_data="settings")],
    ])

def kb_sub(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "sub_btn"), url=CHANNEL_URL)],
        [InlineKeyboardButton(text=t(uid, "btn_check"), callback_data="check")],
    ])

def kb_worlds(uid):
    rows = []
    for code, w in worlds.items():
        rows.append([InlineKeyboardButton(text=w.get("name", code), callback_data=f"world:{code}")])
    rows.append([InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="back_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def kb_buy(uid, code):
    w = worlds.get(code, {})
    price = w.get("price", 25)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_buy", price=price), callback_data=f"buy:{code}")],
        [InlineKeyboardButton(text=t(uid, "btn_free"), url=FREE_URL)],
        [InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="worlds")],
    ])

def kb_settings(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_chlang"), callback_data="chlang")],
        [InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="back_menu")],
    ])

def kb_chlang(uid):
    cur = get_lang(uid) or "ru"
    names = {"ru": "🇷🇺 Русский", "en": "🇬🇧 English", "hi": "🇮🇳 हिन्दी"}
    rows = []
    for code in ["ru", "en", "hi"]:
        mark = "✅ " if code == cur else ""
        rows.append([InlineKeyboardButton(text=mark + names[code], callback_data="lang:" + code)])
    rows.append([InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="settings")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

@dp.message(F.document)
async def admin_add_video(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    fid = msg.document.file_id
    await msg.answer(f"📎 Файл сохранён.\n\n<code>{fid}</code>\n\nОтправь /setsample &lt;код_мира&gt; чтобы привязать видео.")
# ============ ПРИВАТНЫЕ МИРЫ ============

@dp.callback_query(F.data == "worlds")
async def cb_worlds(call: CallbackQuery):
    uid = call.from_user.id
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    if not worlds:
        await call.message.edit_text(t(uid, "no_worlds"), reply_markup=kb_menu(uid))
        await call.answer()
        return
    await call.message.edit_text(t(uid, "worlds_hdr"), reply_markup=kb_worlds(uid))
    await call.answer()

@dp.callback_query(F.data.startswith("world:"))
async def cb_world(call: CallbackQuery):
    uid = call.from_user.id
    code = call.data.split(":", 1)[1]
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    w = worlds.get(code)
    if not w:
        await call.answer("Мир не найден", show_alert=True)
        return
    await call.answer()
    await call.message.delete()
    if w.get("video"):
        try:
            await bot.send_video(uid, w["video"])
        except:
            pass
    if w.get("photo"):
        try:
            await bot.send_photo(uid, w["photo"])
        except:
            pass
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_continue"), callback_data=f"cont:{code}")],
    ])
    await bot.send_message(uid, w.get("name", code), reply_markup=kb)

@dp.callback_query(F.data.startswith("cont:"))
async def cb_continue(call: CallbackQuery):
    uid = call.from_user.id
    code = call.data.split(":", 1)[1]
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    await call.message.edit_text(t(uid, "buy_hdr"), reply_markup=kb_buy(uid, code))
    await call.answer()

# ============ ОПЛАТА ЗВЁЗДАМИ ============

@dp.callback_query(F.data.startswith("buy:"))
async def cb_buy(call: CallbackQuery):
    uid = call.from_user.id
    code = call.data.split(":", 1)[1]
    w = worlds.get(code)
    if not w:
        await call.answer("Мир не найден", show_alert=True)
        return
    price = w.get("price", 25)
    await bot.send_invoice(
        chat_id=uid,
        title=w.get("name", code),
        description=f"Мир {w.get('name', code)} — {price} звёзд",
        payload=f"world:{code}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=w.get("name", code), amount=price)],
    )
    await call.answer()

@dp.pre_checkout_query()
async def pre_checkout(pcq: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pcq.id, ok=True)

@dp.message(F.successful_payment)
async def on_paid(msg: Message):
    uid = msg.from_user.id
    payload = msg.successful_payment.invoice_payload
    code = payload.split(":", 1)[1] if ":" in payload else payload
    w = worlds.get(code, {})
    name = w.get("name", code)
    price = w.get("price", 0)
    await msg.answer(t(uid, "paid_ok"))
    username = msg.from_user.username or msg.from_user.first_name
    try:
        await bot.send_message(
            ADMIN_ID,
            f"💰 <b>Покупка!</b>\n\n"
            f"Мир: <b>{name}</b> (код {code})\n"
            f"Цена: {price} ⭐\n"
            f"Покупатель: @{username} (id {uid})\n\n"
            f"Отправь ему файл в личку."
        )
    except:
        pass

# ============ НАСТРОЙКИ ============

@dp.callback_query(F.data == "settings")
async def cb_settings(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(t(uid, "settings_hdr"), reply_markup=kb_settings(uid))
    await call.answer()

@dp.callback_query(F.data == "chlang")
async def cb_chlang(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(t(uid, "choose_lang"), reply_markup=kb_chlang(uid))
    await call.answer()

@dp.callback_query(F.data == "back_menu")
async def cb_back_menu(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(t(uid, "menu"), reply_markup=kb_menu(uid))
    await call.answer()

@dp.callback_query(F.data == "check")
async def cb_check(call: CallbackQuery):
    uid = call.from_user.id
    if await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_ok"), reply_markup=kb_menu(uid))
    else:
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
    await call.answer()

# ============ АДМИН-КОМАНДЫ ============

@dp.message(F.text.startswith("/addworld"))
async def admin_addworld(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.replace("/addworld", "").strip().split("|")
        name = parts[0].strip()
        code = parts[1].strip()
        price = int(parts[2].strip())
        worlds[code] = {"name": name, "price": price, "video": None, "photo": None}
        save_json(WORLDS_DB, worlds)
        await msg.answer(f"✅ Мир добавлен: <b>{name}</b> (код {code}, {price} ⭐)")
    except Exception as e:
        await msg.answer(f"❌ Формат: /addworld Название | КОД | 25\nОшибка: {e}")

@dp.message(F.text.startswith("/setvideo"))
async def admin_setvideo(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    if not msg.reply_to_message or not msg.reply_to_message.video:
        await msg.answer("Ответь этой командой на видео.")
        return
    code = msg.text.replace("/setvideo", "").strip()
    if code not in worlds:
        await msg.answer(f"Мир {code} не найден. Сначала /addworld")
        return
    worlds[code]["video"] = msg.reply_to_message.video.file_id
    save_json(WORLDS_DB, worlds)
    await msg.answer(f"✅ Видео привязано к {code}")

@dp.message(F.text.startswith("/setphoto"))
async def admin_setphoto(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    if not msg.reply_to_message or not msg.reply_to_message.photo:
        await msg.answer("Ответь этой командой на фото.")
        return
    code = msg.text.replace("/setphoto", "").strip()
    if code not in worlds:
        await msg.answer(f"Мир {code} не найден.")
        return
    worlds[code]["photo"] = msg.reply_to_message.photo[-1].file_id
    save_json(WORLDS_DB, worlds)
    await msg.answer(f"✅ Фото привязано к {code}")

@dp.message(F.text == "/listworlds")
async def admin_list(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    if not worlds:
        await msg.answer("Миров нет.")
        return
    lines = ["📋 <b>Миры:</b>"]
    for code, w in worlds.items():
        v = "🎥" if w.get("video") else "—"
        p = "🖼" if w.get("photo") else "—"
        lines.append(f"• <b>{w.get('name')}</b> | {code} | {w.get('price')} ⭐ | видео {v} | фото {p}")
    await msg.answer("\n".join(lines))

@dp.message(F.text.startswith("/delworld"))
async def admin_del(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    code = msg.text.replace("/delworld", "").strip()
    if code in worlds:
        del worlds[code]
        save_json(WORLDS_DB, worlds)
        await msg.answer(f"🗑 Мир {code} удалён.")
    else:
        await msg.answer(f"Мир {code} не найден.")

@dp.message(F.text.startswith("/setprice"))
async def admin_setprice(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.replace("/setprice", "").strip().split()
        code, price = parts[0], int(parts[1])
        if code in worlds:
            worlds[code]["price"] = price
            save_json(WORLDS_DB, worlds)
            await msg.answer(f"✅ {code} → {price} ⭐")
        else:
            await msg.answer(f"Мир {code} не найден.")
    except Exception as e:
        await msg.answer(f"Формат: /setprice CODE 25\n{e}")

# ============ ЛЮБОЙ ТЕКСТ = /START ============

@dp.message(F.text)
async def any_text(msg: Message):
    if msg.from_user.id == ADMIN_ID and msg.text.startswith("/"):
        return
    uid = msg.from_user.id
    if not get_lang(uid):
        await msg.answer(TEXTS["ru"]["choose_lang"], reply_markup=kb_lang())
        return
    if not await is_subbed(uid):
        await msg.answer(t(uid, "sub_need"), reply_markup=kb_sub(uid))
        return
    await msg.answer(t(uid, "menu"), reply_markup=kb_menu(uid))

# ============ ВЫБОР ЯЗЫКА ============

@dp.callback_query(F.data.startswith("lang:"))
async def cb_lang(call: CallbackQuery):
    uid = call.from_user.id
    lang = call.data.split(":")[1]
    set_user_lang(uid, lang)
    if await is_subbed(uid):
        await call.message.edit_text(t(uid, "sub_ok"), reply_markup=kb_menu(uid))
    else:
        await call.message.edit_text(t(uid, "sub_need"), reply_markup=kb_sub(uid))
    await call.answer()
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())