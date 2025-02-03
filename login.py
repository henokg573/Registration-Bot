import telebot
import sqlite3
import bcrypt
import random
import smtplib
from email.message import EmailMessage

API_KEY = "7927894477:AAH0TZjNJWahF1To1oUf-O_YvQVZ3ZSjpyM"
bot = telebot.TeleBot(API_KEY)

# Connect to Database
def create_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE,
                    email TEXT UNIQUE,
                    password TEXT,
                    verified INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()
create_db()

# Store verification codes
otp_store = {}

# Send email function
def send_verification_email(email, otp):
    sender_email = "contact.easygate.com"
    sender_password = "your_email_password"
    
    msg = EmailMessage()
    msg.set_content(f"Your verification code is: {otp}")
    msg["Subject"] = "Verify Your Email"
    msg["From"] = sender_email
    msg["To"] = email
    
    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email failed:", e)

# Start Command
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Welcome! Please choose:", 
                     reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).row("Register", "Login"))

# Register User
@bot.message_handler(func=lambda msg: msg.text == "Register")
def register(message):
    bot.send_message(message.chat.id, "Enter your email:")
    bot.register_next_step_handler(message, process_email)

def process_email(message):
    email = message.text
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        bot.send_message(message.chat.id, "Email already exists. Try logging in.")
        return start(message)
    
    otp = random.randint(100000, 999999)
    otp_store[message.chat.id] = (email, otp)
    send_verification_email(email, otp)
    bot.send_message(message.chat.id, "Enter the verification code sent to your email:")
    bot.register_next_step_handler(message, process_otp)
    conn.close()

def process_otp(message):
    chat_id = message.chat.id
    if chat_id in otp_store and message.text == str(otp_store[chat_id][1]):
        bot.send_message(chat_id, "Email verified! Now set a password:")
        bot.register_next_step_handler(message, process_password)
    else:
        bot.send_message(chat_id, "Invalid OTP. Try again.")
        return start(message)

def process_password(message):
    password = bcrypt.hashpw(message.text.encode(), bcrypt.gensalt())
    chat_id = message.chat.id
    email = otp_store[chat_id][0]
    
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (telegram_id, email, password, verified) VALUES (?, ?, ?, 1)", 
                (chat_id, email, password))
    conn.commit()
    conn.close()
    del otp_store[chat_id]
    bot.send_message(chat_id, "Registration successful! Please login.")
    start(message)

# Login User
@bot.message_handler(func=lambda msg: msg.text == "Login")
def login(message):
    bot.send_message(message.chat.id, "Enter your registered email:")
    bot.register_next_step_handler(message, process_login_email)

def process_login_email(message):
    email = message.text
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    if user:
        bot.send_message(message.chat.id, "Enter your password:")
        bot.register_next_step_handler(message, lambda msg: process_login_password(msg, email, user[0]))
    else:
        bot.send_message(message.chat.id, "Email not found. Please register.")
        start(message)

def process_login_password(message, email, hashed_password):
    if bcrypt.checkpw(message.text.encode(), hashed_password):
        bot.send_message(message.chat.id, "Login successful! You can now access the official bot.")
    else:
        bot.send_message(message.chat.id, "Incorrect password. Try again.")
        login(message)

# Official Bot Access
@bot.message_handler(commands=["official_bot"])
def official_bot(message):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (message.chat.id,))
    user = cur.fetchone()
    conn.close()
    if user:
        bot.send_message(message.chat.id, "Welcome to the Official Bot! You can now use our services.")
    else:
        bot.send_message(message.chat.id, "You need to register first.")
        start(message)

bot.polling()
