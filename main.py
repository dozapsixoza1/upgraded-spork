import telebot
import random
from telebot import types

# --- НАСТРОЙКИ ---
TOKEN = "8178663250:AAHgXKeZeSoy9d3z5ApD8Dk_JbnOW9MLbXM"
TARGET_CHAT_USERNAME = "chatkaratels" # Юзернейм без @
MY_ID = 7950038145 # Твой цифровой ID

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

# 2. ПОДТВЕРЖДЕНИЕ ПЛАТЕЖА (Чтобы не было ошибки FORM_SUBMIT_DUPLICATE)
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout_process(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def pay_ok(message):
    bot.send_message(message.chat.id, "✅ Звезды зачислены!")

# 3. ОСНОВНАЯ ЛОГИКА В ЧАТЕ
@bot.message_handler(func=lambda m: m.chat.username == TARGET_CHAT_USERNAME)
def chat_logic(message):
    if message.from_user.is_bot: return

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
    print("Бот запущен. Напиши ему /pay в личку для пополнения.")
    bot.infinity_polling()
