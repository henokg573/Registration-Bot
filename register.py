import os
from flask import Flask, request
import telebot
import logging
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import InlineKeyboardMarkup
# from apscheduler.schedulers.background import BackgroundScheduler
import requests
import threading
import time  # Add this line to import the time module
# from flask import Flask, request
import requests
# from apscheduler.schedulers.background import BackgroundScheduler
# API_KEY = "7759515826:AAGOtQ4V-ZVeq_caHh9uYynSQ1UX9THdcq0"
API_KEY = "7759515826:AAEjjGhr8pM7WAJBWP8JG1F-wu85nJck338"
ADMIN_CHAT_ID = "7701687225"
# APP_URL = f'https://easygate-registration-bot-34qv.onrender.com/{API_KEY}'
bot = telebot.TeleBot(API_KEY)

bot.remove_webhook()
# bot.set_webhook(url=APP_URL)
API_URL = f"https://api.telegram.org/bot{API_KEY}"

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running."

def get_updates(offset=None):
    """Fetch updates from Telegram."""
    params = {"offset": offset, "timeout": 60}
    response = requests.get(f"{API_URL}/getUpdates", params=params)
    return response.json()

def send_message(chat_id, text):
    """Send a message to a chat."""
    params = {"chat_id": chat_id, "text": text}
    requests.post(f"{API_URL}/sendMessage", params=params)

# def bot_main():
#     """Main function to handle bot updates."""
#     print("Bot is starting...")
#     offset = None
#     while True:
#         try:
#             updates = get_updates(offset)
#             if "result" in updates:
#                 for update in updates["result"]:
#                     offset = update["update_id"] + 1
#                     chat_id = update["message"]["chat"]["id"]
#                     text = update["message"].get("text", "")
#                     send_message(chat_id, f"You said: {text}")
#         except Exception as e:
#             print(f"Error: {e}")
#             time.sleep(5)  # Avoid crashing on errors

if __name__ == "__main__":
    # Get the port from the environment variable (default to 8000)
    port = int(os.environ.get("PORT", 8000))
    print(f"Running on port: {port}")

    # Run Flask in a separate thread
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port), daemon=True).start()

    # Run the bot's main loop
    # bot_main()








# Define the bot's handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"Received /start from {message.chat.id}")  # Debugging

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = telebot.types.KeyboardButton('About Us')
    btn2 = telebot.types.KeyboardButton('Our Services')
    btn3 = telebot.types.KeyboardButton('Continue to Register')
    btn4 = telebot.types.KeyboardButton('Feedback')
    markup.add(btn1, btn2, btn3, btn4)

    bot.reply_to(
        message,
        f"""👋 Hi {message.chat.first_name}! 
        👋 Welcome to EasyGate!
Your Gateway to Global Opportunities

🌟 Simplifying Your Path to Success
From Dreams to Destinations, we’re here to open doors and ensure smooth journeys.

We are delighted to have you with us!

At EasyGate, we specialize in making your aspirations achievable, whether in education, travel, or career advancement. Here’s how we can support you:

🎓 Scholarship and Admission Assistance
🛂 Passport and Visa Processing
🌐 International Career and E-commerce Services
🏛️ Embassy Appointments and Travel Consultancy
💻 Online Courses and Proficiency Tests



🔹 Registration Period Open!
We are on registration for the clients like you, who desires to use our services to be successful in
your desired career path. 

You can proceed with registration or explore our range of services.

🔹 Need Assistance?

Type /help for immediate guidance.
Use /contact to connect with our support team.
For a detailed guide on using our services, check out /guide.
Let us simplify the complex and help you reach your goals effortlessly!

Thank you for visiting us! We are currently in the registration phase.
📋 Please use the options below to register or check out our services.
We look forward to serving you once the registration process is complete!

Thank you for choosing EasyGate. Let’s achieve greatness together!
        """,
        reply_markup=markup,
        )
    
    @bot.message_handler(func=lambda message: True)
    def handle_options(message):
        print(f"Message received: {message.text}")  # Debugging
        service_selected = message.text  # Define service_selected
        if message.text == "Continue to  Register":
            bot.reply_to(
                message,
                 """To register, we offer three convenient options:

1. Register through our Google Form link.  
2. Contact us directly to complete your registration.  
3. Register directly through our bot.

Please choose one of the options below to continue.""", reply_markup = register_markup())
        elif message.text == "Feedback":
            bot.reply_to(
                message,
                """We value your feedback!

You can send your feedback in one of two ways:

1. Directly to our Admin via the Directly to Admin button.  
2. Submit your feedback using our Google Form by clicking Google Form Feedback.

Please choose the option that suits you best."""
                , reply_markup = feedback_markup())
        
        elif message.text == "Already Registered?":
            bot.reply_to(
                message,
                "If you have already registered, please continue to the payment method",
                reply_markup=payment_markup()
            )


    
    # Guide Command
@bot.message_handler(commands=['guide'])
@bot.message_handler(func=lambda message: message.text == "Guide")
def send_guide(message):
    bot.reply_to(
        message,
        """ Guide to EasyGate registration bot:
1️⃣ See our services, get to know our bot, contact us and learn more.
2️⃣ Follow instructions to register.
3️⃣ Use 'Payment' to handle transactions securely.

Explore and simplify your journey with EasyGate! 🌟""", reply_markup = main_menu_markup()
    )
    # if message.text == "Continue to Register":
    #     bot.reply_to(
    #     message,
    #         """To register, we offer three ways:

    #     1. You can register through our Google Form link.
    #     2. You can contact us directly and register.
    #     3. You can register through our bot.

    #     Please choose one of the options below to continue.""", reply_markup = register_markup())




 # Help Command
@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text == "Help")
def send_guide(message):
    bot.reply_to(
        message,
        """ To use this service, please type /start.  

For a guide on how to use the service, please type /guide.  

To contact us, please use /contact.  
""", reply_markup = main_menu_markup()
    )
    # if message.text == "Continue to Register":
    #     bot.reply_to(
    #     message,
    #         """To register, we offer three ways:

    #     1. You can register through our Google Form link by clicking the Google form button
    #     2. You can contact us directly and register by clicking the Directly on Telegram button
    #     3. You can register through our bot by clicking Bot Registration button

    #     Please choose one of the options below to continue.""", reply_markup = register_markup())
    # Contact Command
@bot.message_handler(commands=['contact'])
@bot.message_handler(func=lambda message: message.text == "Contact")
def send_guide(message):
    bot.reply_to(
        message,
        """Contact us via:
        @easygate2
        0964255107
        contact.easygate@gmail.com
        WhatsApp: +251964255107 or [https://wa.me/+251964255107]
        for help, use this /help
        to start using this service, use this /start""",reply_markup = main_menu_markup())
    # if message.text == "Continue to Register":
    #     bot.reply_to(
    #     message,
    #         """To register, we offer three ways:

    #     1. You can register through our Google Form link.
    #     2. You can contact us directly and register.
    #     3. You can register through our bot.

    #     Please choose one of the options below to continue.""", reply_markup = register_markup())

@bot.message_handler(func=lambda message: message.text == "Continue to Register")
def handle_continue_to_register(message):
    print(f"Message received: {message.text}")  # Debugging
    service_selected = message.text  # Define service_selected  
    if message.text == "Continue to Register":
        bot.reply_to(
            message,
            """To register, we offer three ways:
        1. You can register through our Google Form link by clicking the Google form button
        2. You can contact us directly and register by clicking the Directly on Telegram button
        3. You can register through our bot by clicking Bot Registration button"""
    
        , reply_markup = register_markup())
@bot.message_handler(func=lambda message: True)
def handle_options(message):
    print(f"Message received: {message.text}")  # Debugging
    service_selected = message.text  # Define service_selected
    if message.text == 'About Us':
        bot.reply_to(
        message,
        """Welcome to EasyGate!

We are a team of young Ethiopians currently studying and working across the globe. Our mission is to simplify the process of accessing international education and career opportunities by reducing costs and eliminating the need for expensive intermediaries.

Our goal is to make services such as visa applications, scholarship opportunities, and career guidance more affordable and easily accessible from the comfort of your home.

At EasyGate, we are dedicated to guiding you through every step of your global journey, whether it's education, work, or travel. Let us help you unlock your future, right from your home!

Stay connected with us on our social media platforms to explore our services further:

==> Telegram: @easygate2 or [https://t.me/easygate2]
==> WhatsApp: +251964255107 or [https://wa.me/+251964255107]
==> Email: contact.easygate@gmail.com

Feel free to contact us via any of the platforms above for more information or to get started!
    """, reply_markup = main_menu_markup())
        

    elif message.text == "Our Services":
        bot.reply_to(
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
        
    elif message.text == "Continue to Register":
        bot.reply_to(
        message,
            """To register, we offer three ways:

        1. You can register through our Google Form link.
        2. You can contact us directly and register.
        3. You can register through our bot.

        Please choose one of the options below to continue.""", reply_markup = register_markup())
    elif message.text == "Feedback":
        bot.reply_to(
        message,
            """We value your feedback!

You can send your feedback in one of two ways:

1. Directly to our Admin via the bot.  
2. Submit your feedback using our Google Form link.

Please choose the option that suits you best."""
            , reply_markup = feedback_markup())
    elif message.text == "Already Registered?":
        bot.reply_to(
        message,
            """If you have already registered, please continue to the payment method""", reply_markup = payment_markup())
    elif message.text == "Google Form":
        markup = InlineKeyboardMarkup()
        form_button = InlineKeyboardButton("Click here to fill out the Google Form", url="https://forms.gle/pwapv5YrnVn81KWa6")
        markup.add(form_button)
    
        bot.reply_to(
        message,
        "Please use the button below to access the registration form.",
        reply_markup=markup
    )

    # elif message.text == "Directly on Telegram":
    #     bot.reply_to(
    #         message,
    #             """please use this username
    #             @easygate2 or 0964255107 to register""", reply_markup = register_markup())
        

    elif message.text == "Directly on Telegram":
        markup = InlineKeyboardMarkup()
        register_button = InlineKeyboardButton(
        "please use this link to contact the Admin and register to get services", 
        url="https://t.me/easygate2"
    )
        markup.add(register_button)
        bot.reply_to(
        message,
        "Please send your feedback directly to the admin using this username", 
        reply_markup=markup  # Pass the InlineKeyboardMarkup object here
    )
    elif message.text == "Bot Registration":
        start_registration(message)
    elif message.text == "Google Form feedback":
        markup = InlineKeyboardMarkup()
        form_button = InlineKeyboardButton("Click here to fill out the Google Form", url="https://forms.gle/RqPgyEHv5iSuQVav7")
        markup.add(form_button)
    
        bot.reply_to(
        message,
        "Please use the button below to access the registration form.",
        reply_markup=markup
    )
    elif message.text == "Directly to Admin":
        markup = InlineKeyboardMarkup()
        feeback_button = InlineKeyboardButton(
        "Click here to send your feedback directly to the Admin", 
        url="https://t.me/easygate2"
    )
        markup.add(feeback_button)
        bot.reply_to(
        message,
        "Please send your feedback directly to the admin using this username", 
        reply_markup=markup  # Pass the InlineKeyboardMarkup object here
    )

    elif message.text == "Bank Transfer":
        bot.reply_to(
            message,
                """
                Please transfer the payment to the following bank account:
                Bank Name: CBE
                Account Number: 1000553465994
                Account Name: Henok Girma

                Bank Name: Awash Bank
                Account Number: 01320246243200
                Account Name: Henok Girma
                
        The registration fee for our service is 200 Birr. However, this amount will be deducted from your total service fee, meaning you won’t need to pay the 200 Birr separately during registration. 

                Please provide the receipt after payment.
                """, reply_markup = payment_markup())
    elif message.text == "Telebirr":
        bot.reply_to(
            message,
                """Please transfer the payment to the following Telebirr account:
                Telebirr Number: 0964255107
                Account Name: Henok Girma
                Please provide the receipt after payment.""", reply_markup = payment_markup())
    elif message.text == "Other":
        markup = InlineKeyboardMarkup()
        other_button = InlineKeyboardButton(
        "Click here to make the payment by contacting the admin", 
        url="https://t.me/easygate2"
    )
        markup.add(other_button)
        bot.reply_to(
        message,
        """Please contact the admin
        """, 
        reply_markup=markup  # Pass the InlineKeyboardMarkup object here
    )
    elif message.text == "Already Paid? (Submit receipt)": 
        bot.reply_to(
            message,
                """Please submit the receipt after payment.""", reply_markup = payment_markup())
    elif message.text == "Choose Different Payment Method":
        bot.reply_to(
            message,
                """Please choose a different payment method.
                if your preferred choice is not in the list, please contact the admin to make the payment
                """, reply_markup = payment_markup())
    elif message.text == "main menu":
        bot.reply_to(
            message,
                """
Welcome back to EasyGate!

We are a team of young Ethiopians, currently studying and working across the globe. Our mission is to simplify the process of accessing international education and career opportunities by reducing costs and eliminating the need for expensive intermediaries.

We aim to make services that can be accessed easily from home, such as visa applications, scholarship opportunities, and career guidance, more affordable and accessible to you.

At EasyGate, we're dedicated to guiding you through every step of your global journey, whether it's education, work, or travel. Let us help you unlock your future, right from the comfort of your home!

Stay connected with us on our social media platforms to explore our services further:

Telegram: @easygate2
WhatsApp: +251964255107
Email: contact.easygate@gmail.com
Feel free to contact us via any of the platforms above for more information or to get started!
""", reply_markup = main_menu_markup())
    else:
        bot.reply_to(
                message,
                "I don't understand that command. Please use the help command."
            )
# # Handle the feedback submission and forward to admin
# @bot.message_handler(func=lambda message: message.text == "Directly to Admin")
# def handle_direct_to_admin(message):
#     bot.reply_to(
#         message,
#         "Please send your feedback directly to the admin. Your message will be forwarded.",
#         reply_markup=feedback_markup()  # Ensure you have the correct markup
#     )
    
#     # Register the next step to capture the user's feedback message
#     bot.register_next_step_handler(message, forward_feedback_to_admin)


# def forward_feedback_to_admin(message):
#     user_feedback = message.text
#     user_name = message.from_user.username or "No username"
#     admin_chat_id = "793034140"  # Replace with the admin's chat ID

#     # Create the message that will be sent to the admin
#     feedback_message = (
#         f"New feedback received:\n\n"
#         f"From: @{user_name}\n"
#         f"Message: {user_feedback}"
#     )

#     # Send the feedback message to the admin
#     bot.send_message(admin_chat_id, feedback_message)

    # Confirm to the user that their feedback has been sent
    # bot.reply_to(message, "Your feedback has been sent to the admin. Thank you!")




@bot.message_handler(func=lambda message: message.text == "Bot Registration")
def start_registration(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}  # Initialize user data for this chat
    bot.send_message(chat_id, "Please provide your first name:")
    bot.register_next_step_handler(message, collect_first_name)



user_data = {}
pending_verifications = {}
user_states = {}



def collect_first_name(message):
    chat_id = message.chat.id
    first_name = message.text.strip()
    if len(first_name) < 3:
        bot.reply_to(message, "First name must be at least 3 characters. Try again:")
        bot.register_next_step_handler(message, collect_first_name)
        return
    user_data['first_name'] = first_name
    bot.reply_to(message, "Please enter your father's name:")
    bot.register_next_step_handler(message, collect_fathers_name)
def collect_fathers_name(message):
    chat_id = message.chat.id
    fathers_name = message.text.strip()
    if len(fathers_name) < 3:
        bot.reply_to(message, "First name must be at least 3 characters. Try again:")
        bot.register_next_step_handler(message, collect_fathers_name)
        return
    user_data['fathers_name'] = fathers_name
    bot.reply_to(message, "Please enter your phone number:")
    bot.register_next_step_handler(message, collect_phone_number)
def collect_phone_number(message):
    chat_id = message.chat.id
    phone_number = message.text
    if len(phone_number) != 10 or not phone_number.isdigit():
        bot.send_message(message.chat.id, "Phone number must be exactly 10 digits. Please try again.")
        bot.register_next_step_handler(message, collect_phone_number)
        return
    user_data['phone_number'] = phone_number
    bot.send_message(message.chat.id, "Please enter your email address (must contain @gmail.com):")
    bot.register_next_step_handler(message, collect_email)
def collect_email(message):
    chat_id = message.chat.id
    email = message.text.strip()
    if not email.endswith('@gmail.com'):
        bot.reply_to(message, "Email must contain @gmail.com. Please try again:")
        bot.register_next_step_handler(message, collect_email)
        return
    user_data['email'] = email
    bot.send_message(chat_id, """Thank you! Now, please select a payment method or submit your receipt as pdf or image file
                     """, reply_markup=payment_markup())






# # payment process
# # Handle the receipt submission and forward to admin
# @bot.message_handler(content_types=['document', 'photo'])
# def process_receipt(message):
#     user_id = message.chat.id
#     user_first_name = message.chat.first_name

#     if message.document:
#         file_name = message.document.file_name
#         file_extension = file_name.split('.')[-1].lower()  # Extract file extension
        
#         # Check if the document is a PDF
#         if file_extension == 'pdf':
#             receipt_file = message.document.file_id
#             file_type = 'PDF'
#             bot.send_document(ADMIN_CHAT_ID, receipt_file)
#         else:
#             bot.reply_to(message, "Please send a valid receipt in PDF format.")
#             return

#     elif message.photo:
#         receipt_file = message.photo[-1].file_id  # Get the highest quality photo
#         file_type = 'Photo'
#         bot.send_photo(ADMIN_CHAT_ID, receipt_file)

#     else:
#         bot.reply_to(message, "Please send a valid receipt in PDF or image format.")
#         return

#     # Inform the admin about the receipt submission
#     pending_verifications[user_id] = {'file_id': receipt_file, 'file_type': file_type, 'user_name': user_first_name}
#     bot.reply_to(message, "Your payment receipt has been sent for verification. The admin will confirm your payment shortly.")
#     bot.send_message(ADMIN_CHAT_ID, f"📩 New Payment Receipt from {user_first_name} ({user_id}):")

#     # Send Inline buttons to Admin for verification
#     markup = InlineKeyboardMarkup()
#     verify_button = InlineKeyboardButton("✅ Verify User", callback_data=f"verify_{user_id}")
#     invalid_button = InlineKeyboardButton("❌ Invalid Payment", callback_data=f"invalid_{user_id}")
#     markup.add(verify_button, invalid_button)
#     bot.send_message(ADMIN_CHAT_ID, "Please verify the payment from the user:", reply_markup=markup)


# # Handle admin verification actions
# @bot.callback_query_handler(func=lambda call: call.data.startswith('verify_') or call.data.startswith('invalid_'))
# def handle_admin_response(call):
#     user_id = int(call.data.split('_')[1])

#     if call.data.startswith('verify_'):
#         if user_id in pending_verifications:
#             user_data[user_id] = pending_verifications.pop(user_id)
#             bot.send_message(user_id, "✅ Your payment has been verified! Please proceed to select your service. this is our channel, please join us [channel](https://t.me/easygate)", reply_markup=main_menu_markup())
#         else:
#             bot.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")

#     elif call.data.startswith('invalid_'):
#         if user_id in pending_verifications:
#             pending_verifications.pop(user_id)
#             bot.send_message(user_id, "❌ Your payment could not be verified. Please contact support.")
#             bot.send_message(ADMIN_CHAT_ID, f"Payment invalid for {user_id}. User has been notified.")
#         else:
#             bot.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")

#     bot.answer_callback_query(call.id)  # Close the callback button


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
        bot.send_message(ADMIN_CHAT_ID, f"📩 Verified Payment Receipt from {receipt_details['user_name']} ({user_id}):\n\nService: {service_selected}")
        if file_type == 'Document':
            bot.send_document(ADMIN_CHAT_ID, file_id)
        elif file_type == 'Photo':
            bot.send_photo(ADMIN_CHAT_ID, file_id)

        # Inform the user about the service selection

        # Clear the user's data after the service has been provided
        del user_data[user_id]
    else:
        bot.reply_to(message, "We could not find your payment details. Please resend your receipt.")
        bot.send_message(ADMIN_CHAT_ID, f"❌ User {user_id} has not submitted a valid receipt.")


   
# Handle receipt submission
@bot.message_handler(content_types=['document', 'photo'])
def process_receipt(message):
    user_id = message.chat.id
    user_first_name = message.chat.first_name

    if message.document:
        file_name = message.document.file_name
        file_extension = file_name.split('.')[-1].lower()

        if file_extension == 'pdf':  # Check if the document is a PDF
            receipt_file = message.document.file_id
            file_type = 'PDF'
            bot.send_document(ADMIN_CHAT_ID, receipt_file)
        else:
            bot.reply_to(message, "Please send a valid receipt in PDF format.")
            return
    elif message.photo:
        receipt_file = message.photo[-1].file_id  # Get the highest quality photo
        file_type = 'Photo'
        bot.send_photo(ADMIN_CHAT_ID, receipt_file)
    else:
        bot.reply_to(message, "Please send a valid receipt in PDF or image format.")
        return

    # Inform admin about the receipt
    pending_verifications[user_id] = {'file_id': receipt_file, 'file_type': file_type, 'user_name': user_first_name}
    bot.reply_to(message, "Your payment receipt has been sent for verification. The admin will confirm your payment shortly.")
    bot.send_message(ADMIN_CHAT_ID, f"📩 New Payment Receipt from {user_first_name} ({user_id}):")

    # Add admin verification buttons
    markup = telebot.types.InlineKeyboardMarkup()
    verify_button = telebot.types.InlineKeyboardButton("✅ Verify User", callback_data=f"verify_{user_id}")
    invalid_button = telebot.types.InlineKeyboardButton("❌ Invalid Payment", callback_data=f"invalid_{user_id}")
    markup.add(verify_button, invalid_button)
    bot.send_message(ADMIN_CHAT_ID, "Please verify the payment from the user:", reply_markup=markup)

# Handle admin verification actions
@bot.callback_query_handler(func=lambda call: call.data.startswith('verify_') or call.data.startswith('invalid_'))
def handle_admin_response(call):
    user_id = int(call.data.split('_')[1])

    if user_id not in pending_verifications:
        bot.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")
        bot.answer_callback_query(call.id)  # Close the callback button
        return

    if call.data.startswith('verify_'):
        user_details = pending_verifications.pop(user_id)
        user_data[user_id] = user_details  # Store verified user data
        bot.send_message(user_id, """
✅ Your payment has been verified!

Thank you for completing the payment. Please note:
We are currently in the registration phase and will start providing services once the registration process is complete.

In the meantime, please join our Telegram bot using the link below to stay updated and register for services you want to use:""")
        
         # Create an inline keyboard with the channel link
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("please click this link to use our services", url="https://t.me/EasyGate_Official_Bot") # Add the channel link
        markup.add(button)

        # Send Telegram channel link
        bot.send_message(
            user_id,
            "Click below to join our Telegram channel for updates and news:",
            reply_markup=markup
        )

        bot.send_message(ADMIN_CHAT_ID, f"Payment verified for {user_details['user_name']} ({user_id}).")
    elif call.data.startswith('invalid_'):
        pending_verifications.pop(user_id)
        bot.send_message(user_id, "❌ Your payment could not be verified. Please contact support.")
        bot.send_message(ADMIN_CHAT_ID, f"Payment invalid for user ID {user_id}. User has been notified.")

    bot.answer_callback_query(call.id)  # Close the callback button




def main_menu_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = telebot.types.KeyboardButton('About Us')
    btn2 = telebot.types.KeyboardButton('Our Services')
    btn3 = telebot.types.KeyboardButton('Continue to Register')
    btn4 = telebot.types.KeyboardButton('Feedback')
    btn5 = telebot.types.KeyboardButton('Already Registered?')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup
def register_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Google Form')
    btn2 = telebot.types.KeyboardButton('Bot Registration')
    btn3 = telebot.types.KeyboardButton('Directly on Telegram')
    btn4 = telebot.types.KeyboardButton('main menu')
    markup.add(btn1, btn2, btn3, btn4)
    return markup
def feedback_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Google Form feedback')
    btn2 = telebot.types.KeyboardButton('Directly to Admin')
    btn3 = telebot.types.KeyboardButton('main menu')
    markup.add(btn1, btn2, btn3)
    return markup
def payment_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Bank Transfer')
    btn2 = telebot.types.KeyboardButton('Telebirr')
    btn3 = telebot.types.KeyboardButton('Other')
    btn4 = telebot.types.KeyboardButton('Already Paid? (Submit receipt)')
    btn5 = telebot.types.KeyboardButton('Choose Different Payment Method')
    btn6 = telebot.types.KeyboardButton('main menu')
    btn7 = telebot.types.KeyboardButton('Feedback')
    btn8 = telebot.types.KeyboardButton('back')
    markup.add(btn1, btn2, btn3, btn4, btn5,btn6, btn7, btn8)
    return markup


# Start the bot
bot.polling(none_stop=True) # i am using webhook so i commented this
print(f"Flask app running on port: {port}")


# using long polling 
# if __name__ == "__main__":
#     print("Bot is polling...")
#     bot.infinity_polling()