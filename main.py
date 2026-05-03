import telebot
import random
from telebot import types

# --- НАСТРОЙКИ ---
TOKEN = "8178663250:AAHgXKeZeSoy9d3z5ApD8Dk_JbnOW9MLbXM"
TARGET_CHAT_USERNAME = "chatkaratels" # Юзернейм без @
MY_ID = 7950038145 # Твой цифровой ID (обязательно укажи свой!)

# ID подарков
GIFT_PAINTER_ID = 6026193266406327981  # 50 звезд
GIFT_HEART_ID = 5170145012310081615    # 15 звезд
GIFT_ROSE_ID = 5168103777563050263     # 25 звезд

bot = telebot.TeleBot(TOKEN)

# 1. КОМАНДА ДЛЯ ПОПОЛНЕНИЯ (Пиши боту в личку /pay)
@bot.message_handler(commands=['pay'])
def send_payment(message):
    if message.from_user.id == MY_ID:
        bot.send_invoice(
            chat_id=message.chat.id,
            title="Пополнение баланса",
            description="Зачислить 100 звезд на подарки",
            invoice_payload="topup",
            provider_token="", 
            currency="XTR",
            prices=[types.LabeledPrice(label="Звезды", amount=100)]
        )

# 2. ПОДТВЕРЖДЕНИЕ ПЛАТЕЖА (Служебное)
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout_process(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def pay_ok(message):
    bot.send_message(message.chat.id, "✅ Звезды зачислены!")

# 3. КОМАНДА ЕЖЕДНЕВНОГО КОНКУРСА (Пиши в чате /daily или /конкурс)
@bot.message_handler(commands=['daily', 'конкурс'], func=lambda m: m.chat.username == TARGET_CHAT_USERNAME)
def start_daily_contest(message):
    # Проверяем, что команду запустил именно ты
    if message.from_user.id != MY_ID:
        return
    
    text = (
        "🎉 **Ежедневный розыгрыш начинается!**\n\n"
        "Сегодня я разыграю бонусные подарки самым активным участникам. "
        "Просто общайтесь в чате, и шанс на победу увеличится!\n"
        "Кто залутает первого мишку? Погнали! 🚀"
    )
    # Удаляем твое сообщение с командой, чтобы было красиво
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# 4. ОСНОВНАЯ ЛОГИКА В ЧАТЕ (Автоответ на посты + Рулетка)
# Добавили content_types, чтобы бот реагировал и на посты с фото/видео
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'animation'], func=lambda m: m.chat.username == TARGET_CHAT_USERNAME)
def chat_logic(message):
    
    # --- АВТООТВЕТ НА ПОСТЫ ИЗ КАНАЛА ---
    if getattr(message, 'is_automatic_forward', False):
        welcome_text = (
            "приветствую всех! \n\n"
            "тут ты можешь общаться в комментариях и чате и получить мишку от @psychokaratel ✌️\n\n"
            "просто общайся в чате и получай возможность залутать мишку 🧸\n\n"
            "⭐️ купить звезды дешево любым способом оплаты 👉 @mirrorstarsbot"
        )
        bot.reply_to(message, welcome_text)
        return # Выходим, чтобы канал сам себе подарки не выигрывал

    # Игнорируем обычных ботов
    if message.from_user.is_bot or not message.text: 
        return

    # --- РУЛЕТКА ПОДАРКОВ ---
    roll = random.uniform(0, 100)
    gift_id = None
    prize_name = ""

    if roll <= 0.1:
        gift_id = GIFT_PAINTER_ID
        prize_name = "нового мишку-маляра 🧸🎨 за 50 звёзд"
    elif roll <= 1.5:
        gift_id = GIFT_ROSE_ID
        prize_name = "красивую розу 🌹 за 25 звёзд"
    elif roll <= 4.5:
        gift_id = GIFT_HEART_ID
        prize_name = "сердечко 💖 за 15 звёзд"

    if gift_id:
        try:
            bot.send_gift(user_id=message.from_user.id, gift_id=gift_id)
            text = (
                f"🎉 Поздравляю!\n"
                f"🎁 Ты выиграл {prize_name} от @psychokaratel\n"
                f"✅ Подарок отправлен.\n\n"
                f"⭐ Купить звезды дешево с любым способом оплаты:\n"
                f"@mirrorstarsbot\n\n"
                f"‼️ пишите сообщения в чате, и получайте возможность так же залутать призы"
            )
            bot.reply_to(message, text)
        except Exception as e:
            print(f"Ошибка выдачи: {e}")

if __name__ == "__main__":
    print("Бот запущен. Мониторю посты и чат...")
    bot.infinity_polling()
