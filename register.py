import asyncio
from flask import Flask, request
from telebot import TeleBot, types
from aiogram import Bot, Dispatcher, types as aio_types
from aiogram.filters import Command
from fastapi import FastAPI, Request
import http.server
import socketserver
import threading
from contextlib import asynccontextmanager
import httpx

from fastapi import FastAPI
from fastapi import HTTPException
# Correctly define the app instance
fastapi_app = FastAPI()

from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
# # API keys and admin chat ID
# API_KEY = "7759515826:AAG9Gl8kSJLbpeaGbui351Nx-A"
# ADMIN_CHAT_ID = "793034140"

# Initialize Telebot and Flask app
telebot_instance = TeleBot(API_KEY)
flask_app = Flask(__name__)

# Initialize Aiogram and FastAPI
aiogram_bot = Bot(token=API_KEY)
dp = Dispatcher()

# Define a common endpoint for both bots
PING_ENDPOINT = "https://easygate-registration-bot-34qv.onrender.com/healthcheck"

# Telebot Handlers
@telebot_instance.message_handler(commands=["start"])
def telebot_start(message):
    print(f"Received /start from {message.chat.id}")  # Debugging
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('About Us')
    btn2 = types.KeyboardButton('Our Services')
    btn3 = types.KeyboardButton('Continue to Register')
    btn4 = types.KeyboardButton('Feedback')
    markup.add(btn1, btn2, btn3, btn4)

    telebot_instance.reply_to(
        message,
        f"""👋 Hi {message.chat.first_name}!  
        👋 Welcome to EasyGate!, 
        Welcome to Your Gateway to Global Opportunities.
        
        Simplifying Your Path to Success.
        From Dreams to Destinations.
        Open Doors, Easy Journeys.

We’re thrilled to have you here! 🎉

At EasyGate, we specialize in making your goals more accessible, whether it’s education, travel, or career growth. Here's what we can help you with:
- Scholarship and admission opportunities
- Passport and visa applications
- International career and e-commerce services
- Embassy appointments and travel consultancy
- Online courses and proficiency tests

Let us guide you every step of the way! Simply explore the options below and get started on your journey with us.

Feel free to reach out if you have any questions—we’re here to make things easy for you!

We are currently in the registration period. You can continue to register or see our services. 
If you need help, please type /help.
If you need to contact us, use the command /contact.
If you need a guide on how to use our services, we have prepared a tour guide here: /guide.
        """,
        reply_markup=markup,
    )

@flask_app.route(f"/{API_KEY}", methods=["POST"])
def telebot_webhook():
    update = request.get_json()
    if update:
        telebot_instance.process_new_updates([types.Update.de_json(update)])
    return {"status": "ok"}



@dp.message(Command("start"))
async def aiogram_start(message: aio_types.Message):
    # await message.answer("Hello! I'm the EasyGate registration bot. How can I help you?")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('About Us')
    btn2 = types.KeyboardButton('Our Services')
    btn3 = types.KeyboardButton('Continue to Register')
    btn4 = types.KeyboardButton('Feedback')
    btn5 = types.KeyboardButton('Already Registered?')
    markup.add(btn1, btn2, btn3, btn4, btn5)

    telebot_instance.reply_to(
        message,
        f"""👋 Hi {message.chat.first_name}! 
        👋 Welcome to EasyGate!, 
        Welcome to Your Gateway to Global Opportunities.
        
        Simplifying Your Path to Success.
        From Dreams to Destinations.
        Open Doors, Easy Journeys.

We’re thrilled to have you here! 🎉

At EasyGate, we specialize in making your goals more accessible, whether it’s education, travel, or career growth. Here's what we can help you with:
- Scholarship and admission opportunities
- Passport and visa applications
- International career and e-commerce services
- Embassy appointments and travel consultancy
- Online courses and proficiency tests

Let us guide you every step of the way! Simply explore the options below and get started on your journey with us.

Feel free to reach out if you have any questions—we’re here to make things easy for you!

We are currently in the registration period. You can continue to register or see our services. 
If you need help, please type /help.
If you need to contact us, use the command /contact.
If you need a guide on how to use our services, we have prepared a tour guide here: /guide.
        """,
        reply_markup=markup,
    )




    
    # Guide Command
@telebot_instance.message_handler(commands=['guide'])
@telebot_instance.message_handler(func=lambda message: message.text == "Guide")
def send_guide(message):
    telebot_instance.reply_to(
        message,
        """ Guide to EasyGate registration bot:
1️⃣ See our services, get to know our bot, contact us and learn more.
2️⃣ Follow instructions to register.
3️⃣ Use 'Payment' to handle transactions securely.

Explore and simplify your journey with EasyGate! 🌟""", reply_markup = main_menu_markup()
    )




 # Help Command
@telebot_instance.message_handler(commands=['help'])
@telebot_instance.message_handler(func=lambda message: message.text == "Help")
def send_guide(message):
    telebot_instance.reply_to(
        message,
        """ to use this service, please hit /start
        for guide, use this /guide
        to  contact us, use this /contact
""", reply_markup = main_menu_markup()
    )
    # Contact Command
@telebot_instance.message_handler(commands=['contact'])
@telebot_instance.message_handler(func=lambda message: message.text == "Contact")
def send_guide(message):
    telebot_instance.reply_to(
        message,
        """Contact us via:
        @easygate2
        0964255107
        contact.easygate@gmail.com
        for help, use this /help
        to start using this service, use this /start""",reply_markup = main_menu_markup())


@telebot_instance.message_handler(func=lambda message: True)
def handle_options(message):
    print(f"Message received: {message.text}")  # Debugging
    service_selected = message.text  # Define service_selected
    if message.text == 'About Us':
        telebot_instance.reply_to(
        message,
        """Welcome to EasyGate! 

    We are a team of young Ethiopians, currently studying and working across the globe. Our mission is to simplify the process of accessing international education and career opportunities by reducing costs and eliminating the need for expensive intermediaries. 

    We aim to make services that can be accessed easily from home, such as visa applications, scholarship opportunities, and career guidance, more affordable and accessible to you.

    At EasyGate, we're dedicated to guiding you through every step of your global journey, whether it's education, work, or travel. Let us help you unlock your future, right from the comfort of your home!.
    Stay connected with us on our social media platforms to explore our services further:

     Telegram: @easygate or https://t.me/easygate
     WhatsApp: 0964255107 or https://wa.me/0964255107
     Email: contact.easygate@gmail.com

    Feel free to contact us via any of the platforms above for more information or to get started! 
    """, reply_markup = main_menu_markup())
    elif message.text == "Our Services":
        telebot_instance.reply_to(
        message,
        """ Our Services:
    1️⃣ Embassy Interview Assistance
    2️⃣ Document Review
    3️⃣ Travel Advice
    4️⃣ Visa Application Assistance
    5️⃣ Scholarship Opportunities
    6️⃣ English Proficiency Test Preparation
    7️⃣ Passport Services
    8️⃣ E-Visa Applications
    9️⃣ International Payments
    🔟 International Career Opportunities
    1️⃣1️⃣ Recommend Educational Travel Consultancies
    1️⃣2️⃣ Assistance with Any Embassy Interview Practice
    1️⃣3️⃣ Other Services

📞 Contact us to learn more.""", reply_markup = main_menu_markup())
    elif message.text == "Continue to  Register":
        telebot_instance.reply_to(
        message,
            """To register, we offer three ways, you can register through
            our google form link, you can contact us and register, and you can register through our bot.
            please choose one of the options below to continue.""", reply_markup = register_markup())
    elif message.text == "Feedback":
        telebot_instance.reply_to(
        message,
            """We value your feedback!. you can directly send your feedbacks to Admin
            or you can send your feedbacks using our Google form link: please choose what suits you well"""
            , reply_markup = feedback_markup())
    elif message.text == "Already Registered?":
        telebot_instance.reply_to(
        message,
            """If you have already registered, please continue to the payment method""", reply_markup = payment_markup())
    elif message.text == "Google Form":
        telebot_instance.reply_to(
        message,
            """Please fill out the Google form to register: [Google Form](https://forms.gle/7oZ6z5f4v5ZnUv8dA)""", reply_markup = register_markup())
    elif message.text == "Directly on Telegram":
        telebot_instance.reply_to(
            message,
                """please use this username
                @easygate2 or 0964255107 to register""", reply_markup = register_markup())
    elif message.text == "Bot Registration":
        start_registration(message)
    elif message.text == "Google Form feedback":
        telebot_instance.reply_to(
            message,
                """Please fill out the Google form to provide feedback: [Google Form](https://forms.gle/7oZ6z5f4v5ZnUv8dA)""", reply_markup = feedback_markup())

@telebot_instance.message_handler(func=lambda message: message.text == "Directly to Admin")
def handle_feedback(message):
    telebot_instance.reply_to(
        message,
        """Please send your feedback directly to the admin.""",
        reply_markup=feedback_markup()
    )

# This will handle the feedback sent by the user
@telebot_instance.message_handler(func=lambda message: message.text and message.text != "Directly to Admin")
def forward_feedback_to_admin(message):
    if message.text:
        try:
            # Send the user's message to the admin
            telebot_instance.send_message(ADMIN_CHAT_ID, f"Feedback from {message.from_user.first_name} ({message.from_user.id}):\n\n{message.text}")
            telebot_instance.reply_to(
                message,
                "Your feedback has been sent to the admin. Thank you!"
            )
        except Exception as e:
            telebot_instance.reply_to(
                message,
                "There was an error sending your feedback. Please try again later."
            )
            print(f"Error forwarding feedback: {e}")

    elif message.text == "Bank Transfer":
        telebot_instance.reply_to(
            message,
                """Please transfer the payment to the following bank account:
                Bank Name: CBE
                Account Number: 1000000000000
                Account Name: EasyGate
                Please provide the receipt after payment.""", reply_markup = payment_markup())
    elif message.text == "Telebirr":
        telebot_instance.reply_to(
            message,
                """Please transfer the payment to the following Telebirr account:
                Telebirr Number: 0964255107
                Account Name: EasyGate
                Please provide the receipt after payment.""", reply_markup = payment_markup())
    elif message.text == "PayPal":
        telebot_instance.reply_to(
            message,
                """Please transfer the payment to the following PayPal account:
                PayPal Email: contact.easygate@gmail.com""", reply_markup = payment_markup())
    elif message.text == "Already Paid? (Submit receipt)": 
        telebot_instance.reply_to(
            message,
                """Please submit the receipt after payment.""", reply_markup = payment_markup())
    elif message.text == "Choose Different Payment Method":
        telebot_instance.reply_to(
            message,
                """Please choose a different payment method.""", reply_markup = payment_markup())
    elif message.text == "main menu":
        telebot_instance.reply_to(
            message,
                """Welcome to EasyGate!
                We are a team of young Ethiopians, currently studying and working across the globe. Our mission is to simplify the process of accessing international education and career opportunities by reducing costs and eliminating the need for expensive intermediaries.   
                We aim to make services that can be accessed easily from home, such as visa applications, scholarship opportunities, and career guidance, more affordable and accessible to you.
                At EasyGate, we're dedicated to guiding you through every step of your global journey, whether it's education, work, or travel. Let us help you unlock your future, right from the comfort of your home!.
                Stay connected with us on our social media platforms to explore our services further:
                Telegram: [@easygate](https://t.me/easygate)
                WhatsApp: [0964255107](https://wa.me/0964255107)
                Email: contact.easygate@gmail.com
                Feel free to contact us via any of the platforms above for more information or to get started!""", reply_markup = main_menu_markup())
    else:
        telebot_instance.reply_to(
                message,
                "I don't understand that command. Please use the help commant."
            )
# Handle the feedback submission and forward to admin
@telebot_instance.message_handler(func=lambda message: message.text == "Directly to Admin")
def handle_direct_to_admin(message):
    telebot_instance.reply_to(
        message,
        "Please send your feedback now. I'll forward it to the admin."
    )
    
    # Register a handler to capture the next message as feedback
    telebot_instance.register_next_step_handler(message, forward_feedback_to_admin)

def forward_feedback_to_admin(message):
    # Send the user's feedback to the admin
    try:
        telebot_instance.send_message(
            ADMIN_CHAT_ID,
            f"Feedback from @{message.from_user.username or message.from_user.first_name}:\n{message.text}"
        )
        telebot_instance.reply_to(message, "Thank you! Your feedback has been sent to the admin.")
    except Exception as e:
        telebot_instance.reply_to(message, "Oops! Something went wrong while sending your feedback.")
        print(f"Error: {e}")


@telebot_instance.message_handler(func=lambda message: message.text == "Bot Registration")
def start_registration(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}  # Initialize user data for this chat
    telebot_instance.send_message(chat_id, "Please provide your first name:")
    telebot_instance.register_next_step_handler(message, collect_first_name)



user_data = {}
pending_verifications = {}
user_states = {}



def collect_first_name(message):
    chat_id = message.chat.id
    first_name = message.text.strip()
    if len(first_name) < 3:
        telebot_instance.reply_to(message, "First name must be at least 3 characters. Try again:")
        telebot_instance.register_next_step_handler(message, collect_first_name)
        return
    user_data['first_name'] = first_name
    telebot_instance.reply_to(message, "Please enter your father's name:")
    telebot_instance.register_next_step_handler(message, collect_fathers_name)
def collect_fathers_name(message):
    chat_id = message.chat.id
    fathers_name = message.text.strip()
    if len(fathers_name) < 3:
        telebot_instance.reply_to(message, "First name must be at least 3 characters. Try again:")
        telebot_instance.register_next_step_handler(message, collect_fathers_name)
        return
    user_data['fathers_name'] = fathers_name
    telebot_instance.reply_to(message, "Please enter your phone number:")
    telebot_instance.register_next_step_handler(message, collect_phone_number)
def collect_phone_number(message):
    chat_id = message.chat.id
    phone_number = message.text
    if len(phone_number) != 10 or not phone_number.isdigit():
        telebot_instance.send_message(message.chat.id, "Phone number must be exactly 10 digits. Please try again.")
        telebot_instance.register_next_step_handler(message, collect_phone_number)
        return
    user_data['phone_number'] = phone_number
    telebot_instance.send_message(message.chat.id, "Please enter your email address (must contain @gmail.com):")
    telebot_instance.register_next_step_handler(message, collect_email)
def collect_email(message):
    chat_id = message.chat.id
    email = message.text.strip()
    if not email.endswith('@gmail.com'):
        telebot_instance.reply_to(message, "Email must contain @gmail.com. Please try again:")
        telebot_instance.register_next_step_handler(message, collect_email)
        return
    user_data['email'] = email
    telebot_instance.send_message(chat_id, """Thank you! Now, please select a payment method or submit your receipt.
                     and write your name on the file format or when you send a file, write your name on it or rename the file as your name.
                     for example, JohnDoe.jp for images or JohnDoe.pdf for pdf files""", reply_markup=payment_markup())



# Handle the receipt submission and forward to admin
@telebot_instance.message_handler(content_types=['document', 'photo'])
def process_receipt(message):
    user_id = message.chat.id
    user_first_name = message.chat.first_name



    

    if message.document:
        file_name = message.document.file_name
        file_extension = file_name.split('.')[-1].lower()  # Extract file extension
        
        # Check if the document is a PDF
        if file_extension == 'pdf':
            receipt_file = message.document.file_id
            file_type = 'PDF'
            telebot_instance.send_document(ADMIN_CHAT_ID, receipt_file)
        else:
            telebot_instance.reply_to(message, "Please send a valid receipt in PDF format.")
            return

    elif message.photo:
        receipt_file = message.photo[-1].file_id  # Get the highest quality photo
        file_type = 'Photo'
        telebot_instance.send_photo(ADMIN_CHAT_ID, receipt_file)

    else:
        telebot_instance.reply_to(message, "Please send a valid receipt in PDF or image format.")
        return

    # Inform the admin about the receipt submission
    pending_verifications[user_id] = {'file_id': receipt_file, 'file_type': file_type, 'user_name': user_first_name}
    telebot_instance.reply_to(message, "Your payment receipt has been sent for verification. The admin will confirm your payment shortly.")
    telebot_instance.send_message(ADMIN_CHAT_ID, f"📩 New Payment Receipt from {user_first_name} ({user_id}):")
    # bot.send_message(ADMIN_CHAT_ID, registration_details)

    # Send Inline buttons to Admin for verification
    markup = types.InlineKeyboardMarkup()
    verify_button = types.InlineKeyboardButton("✅ Verify User", callback_data=f"verify_{user_id}")
    invalid_button = types.InlineKeyboardButton("❌ Invalid Payment", callback_data=f"invalid_{user_id}")
    markup.add(verify_button, invalid_button)
    telebot_instance.send_message(ADMIN_CHAT_ID, "Please verify the payment from the user:", reply_markup=markup)


# Handle admin verification actions
@telebot_instance.callback_query_handler(func=lambda call: call.data.startswith('verify_') or call.data.startswith('invalid_'))
def handle_admin_response(call):
    user_id = int(call.data.split('_')[1])
    
    if call.data.startswith('verify_'):
        if user_id in pending_verifications:
            user_data[user_id] = pending_verifications.pop(user_id)
            telebot_instance.send_message(user_id, "✅ Your payment has been verified! Please proceed to select your service. this is our channel, please join us [channel](https://t.me/easygate)", reply_markup=main_menu_markup())
        else:
            telebot_instance.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")

    elif call.data.startswith('invalid_'):
        if user_id in pending_verifications:
            pending_verifications.pop(user_id)
            telebot_instance.send_message(user_id, "❌ Your payment could not be verified. Please contact support.")
            telebot_instance.send_message(ADMIN_CHAT_ID, f"Payment invalid for {user_id}. User has been notified.")
        else:
            telebot_instance.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")

    telebot_instance.answer_callback_query(call.id)  # Close the callback button


def handle_service_selection(message):
    user_id = message.chat.id
    service_selected = message.text

    # Debug log
    print(f"User {user_id} selected the service: {service_selected}")

    if user_id in user_data:
        receipt_details = user_data[user_id]
        file_id = receipt_details['file_id']
        file_type = receipt_details['file_type']

        # Forward the receipt and service selection to the admin
        telebot_instance.send_message(ADMIN_CHAT_ID, f"📩 Verified Payment Receipt from {receipt_details['user_name']} ({user_id}):\n\nService: {service_selected}")
        if file_type == 'Document':
            telebot_instance.send_document(ADMIN_CHAT_ID, file_id)
        elif file_type == 'Photo':
            telebot_instance.send_photo(ADMIN_CHAT_ID, file_id)

        # Inform the user about the service selection

        # Clear the user's data after the service has been provided
        del user_data[user_id]
    else:
        telebot_instance.reply_to(message, "We could not find your payment details. Please resend your receipt.")


def process_receipt(message):
    # Process receipt logic here
    chat_id = message.chat.id
    telebot_instance.send_message(
        chat_id,
        "Thank you for submitting your receipt. Please choose a payment method or let us know if you've already paid:",
        reply_markup=payment_markup()  # Show the payment options
    )

def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('About Us')
    btn2 = types.KeyboardButton('Our Services')
    btn3 = types.KeyboardButton('Continue to  Register')
    btn4 = types.KeyboardButton('Feedback')
    btn5 = types.KeyboardButton('Already Registered?')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup
def register_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Google Form')
    btn2 = types.KeyboardButton('Bot Registration')
    btn3 = types.KeyboardButton('Directly on Telegram')
    btn4 = types.KeyboardButton('main menu')
    markup.add(btn1, btn2, btn3, btn4)
    return markup
def feedback_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Google Form feedback')
    btn2 = types.KeyboardButton('Directly to Admin')
    btn3 = types.KeyboardButton('main menu')
    markup.add(btn1, btn2, btn3)
    return markup
def payment_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Bank Transfer')
    btn2 = types.KeyboardButton('Telebirr')
    btn3 = types.KeyboardButton('PayPal')
    btn4 = types.KeyboardButton('Already Paid? (Submit receipt)')
    btn5 = types.KeyboardButton('Choose Different Payment Method')
    btn6 = types.KeyboardButton('main menu')
    btn7 = types.KeyboardButton('Feedback')
    btn8 = types.KeyboardButton('back')
    markup.add(btn1, btn2, btn3, btn4, btn5,btn6, btn7, btn8)
    return markup


@fastapi_app.post(f"/{API_KEY}")
async def aiogram_webhook(request: Request):
    update = await request.json()
    await dp.process_update(aio_types.Update(**update))
    return {"status": "ok"}

# Async Ping Task for Healthcheck
async def cyclic_ping():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(PING_ENDPOINT)
                print(f"Pinging app: Status code {response.status_code}")
            await asyncio.sleep(600)  # Ping every 10 minutes
        except Exception as e:
            print(f"Error in cyclic_ping: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying

# Thread for Telebot
def run_telebot():
    print("Starting Telebot...")
    telebot_instance.polling()

# Async Task for Aiogram
async def run_aiogram():
    print("Starting Aiogram...")
    await dp.start_polling(aiogram_bot)

# Dummy HTTP Server for Testing
def start_dummy_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

# Main Entry Point
if __name__ == "__main__":
    # Start Telebot in a separate thread
    telebot_thread = threading.Thread(target=run_telebot, daemon=True)
    telebot_thread.start()

    # Start Dummy HTTP Server in another thread
    dummy_server_thread = threading.Thread(target=start_dummy_server, daemon=True)
    dummy_server_thread.start()

    # Run Aiogram in the main asyncio loop
    asyncio.run(run_aiogram())


if __name__ == "__main__":
    # Start the dummy server in a separate thread
    threading.Thread(target=start_dummy_server, daemon=True).start()

    telebot_thread = threading.Thread(target=run_telebot, daemon=True)
    telebot_thread.start()
    # Start the Telegram bot
    telebot_instance.polling()
