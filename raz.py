import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '7490024301:AAFKur4oy9ojJ5mmpno9-BCNZHjBKxTmpTs'
USER_DATA_FILE = "users.txt"

# تابعی برای بررسی اینکه آیا کاربر برای اولین بار وارد شده است
def is_first_time(user_id):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            user_ids = f.read().splitlines()
            return str(user_id) not in user_ids
    return True

# تابعی برای ذخیره شناسه کاربر در فایل
def save_user(user_id):
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{user_id}\n")

# تابع اصلی /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # بررسی اینکه آیا کاربر اولین بار است وارد می‌شود
    if is_first_time(user_id):
        save_user(user_id)
        await update.message.reply_text("به ربات خوش آمدید! 😊\nیک گزینه را انتخاب کنید:")
    else:
        await update.message.reply_text("سلام دوباره! یک گزینه را انتخاب کنید:")

    # ساخت منوی اصلی کیبورد
    main_keyboard = [
        ["پیدا کردن آدرس", "پیدا کردن شماره"],
        ["هک سیستمی", "ایجاد مزاحمت"],
        ["خرید اشتراک"]
    ]
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

    # ارسال منوی اصلی به کاربر
    await update.message.reply_text("یک گزینه را انتخاب کنید:", reply_markup=reply_markup)

# هندلر برای پیام‌های کیبورد
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # بررسی انتخاب کاربر و تغییر منو بر اساس آن
    if user_message == "پیدا کردن آدرس":
        keyboard = [
            ["با استفاده از شماره موبایل", "با استفاده از ایدی"],
            ["بازگشت به منوی اصلی"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("نوع آدرس را انتخاب کنید:", reply_markup=reply_markup)

    elif user_message == "پیدا کردن شماره":
        
        keyboard = [
            ["(با شماره موبایل) شماره تلفن خانه", "شماره تلفن همراه"],
            ["بازگشت به منوی اصلی"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("نوع شماره را انتخاب کنید:", reply_markup=reply_markup)

    elif user_message == "هک سیستمی":
       
        mkeyboard = [
            ["هک اینترنتی (فیشینگ)", "هک درون شبکه ای"],
            ["بازگشت به منوی اصلی"]
        ]
        reply_markup = ReplyKeyboardMarkup(mkeyboard, resize_keyboard=True)
        await update.message.reply_text("نوع هک را انتخاب کنید:", reply_markup=reply_markup)

    elif user_message == "ایجاد مزاحمت":
     mkeyboard = [
            ["تماس بمبر", "اس ام اس بمبر"],
            ["بازگشت به منوی اصلی"]
        ]
     reply_markup = ReplyKeyboardMarkup(mkeyboard, resize_keyboard=True)
     await update.message.reply_text("نوع هک را انتخاب کنید:", reply_markup=reply_markup)

    elif user_message == "خرید اشتراک" :
     await update.message.reply_text("متاسفانه درگاه پرداخت به مشکل خورده است ")
    
    elif user_message == "بازگشت به منوی اصلی":
        # بازگشت به منوی اصلی
        main_keyboard = [
            ["پیدا کردن آدرس", "پیدا کردن شماره"],
            ["هک سیستمی", "ایجاد مزاحمت"]
        ]
        reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
        await update.message.reply_text("بازگشت به منوی اصلی", reply_markup=reply_markup)

    else:
        await update.message.reply_text("برای استفاده از این گزینه باید اشتراک پرمیوم بات را خریداری کنید")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن فرمان /start
    app.add_handler(CommandHandler("start", start))
    
    # هندلر برای پیام‌های کیبورد
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # اجرای بات
    app.run_polling()

if __name__ == '__main__':
    main()