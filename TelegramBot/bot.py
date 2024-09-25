from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, filters
import json
import logging
from io import BytesIO
import qrcode
from datetime import datetime
import mysql.connector
from mysql.connector import Error



API_TOKEN = '<ENTER TOKEN HERE>'

LOG_FILE = 'log.json'
LOST_AND_FOUND_FILE = 'lost_and_found.json'
FEEDBACK_FILE = 'feedback.json'
TICKET_INFO_FILE = 'ticket_info.json'
REPORT_FOUND_FILE = 'report_found.json'

# Function to load translation files
def load_language(language_code):
    with open(f'{language_code}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# MySQL database connection
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='<USERNAME>',
            password='<PASSWORD>',
            database='main'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

'''
# Helper Functions for saving and loading logs
def save_logs(logs):
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Prepare an SQL query with placeholders for data
    insert_query = """
        INSERT INTO log (user_id, username, first_name, last_name, chat_id, message_id, timestamp, phone_number, location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert each log entry into the database
    for log in logs:
        cursor.execute(insert_query, (log["user_id"], log["username"], log["first_name"], log["last_name"],
                                      log["chat_id"], log["message_id"], log["timestamp"], log["phone_number"], log["location"]))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def load_logs():
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Execute a SQL query to fetch all log entries
    select_query = "SELECT * FROM log"
    cursor.execute(select_query)

    # Fetch all rows from the result set
    logs = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Convert the fetched rows into a list of dictionaries
    logs_data = []
    for row in logs:
        log_dict = {
            "system_id": row[0],            # Fetch system_id from index 0
            "user_id": row[1],              # Assuming user_id is at index 1
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "chat_id": row[5],
            "message_id": row[6],
            "timestamp": row[7],
            "phone_number": row[8],
            "location": row[9]
        }
        logs_data.append(log_dict)

    return logs_data
'''
def save_lost_and_found(lost_and_found):
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Prepare an SQL query with placeholders for data
    insert_query = """
        INSERT INTO mainpage_lostandfound_telegram (user_id, username, first_name, last_name, chat_id, message_id, description, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert each lost and found entry into the database
    for item in lost_and_found:
        cursor.execute(insert_query, (item["user_id"], item["username"], item["first_name"], item["last_name"],
                                      item["chat_id"], item["message_id"], item["description"], item["timestamp"]))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def load_lost_and_found():
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Execute a SQL query to fetch all lost and found entries
    select_query = "SELECT * FROM lost_and_found"
    cursor.execute(select_query)

    # Fetch all rows from the result set
    lost_and_found = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Convert the fetched rows into a list of dictionaries
    lost_and_found_data = []
    for row in lost_and_found:
        item_dict = {
            "system_id": row[0],            # Fetch system_id from index 0
            "user_id": row[1],              # Assuming user_id is at index 1
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "chat_id": row[5],
            "message_id": row[6],
            "description": row[7],
            "timestamp": row[8]
        }
        lost_and_found_data.append(item_dict)

    return lost_and_found_data

def save_feedback(feedback):
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Prepare an SQL query with placeholders for data
    insert_query = """
        INSERT INTO mainpage_feedback_telegram  (user_id, username, first_name, last_name, chat_id, message_id, feedback, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert each feedback entry into the database
    for item in feedback:
        cursor.execute(insert_query, (item["user_id"], item["username"], item["first_name"], item["last_name"],
                                      item["chat_id"], item["message_id"], item["feedback"], item["timestamp"]))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def load_feedback():
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Execute a SQL query to fetch all feedback entries
    select_query = "SELECT * FROM feedback"
    cursor.execute(select_query)

    # Fetch all rows from the result set
    feedback = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Convert the fetched rows into a list of dictionaries
    feedback_data = []
    for row in feedback:
        item_dict = {
            "system_id": row[0],            # Fetch system_id from index 0
            "user_id": row[1],              # Assuming user_id is at index 1
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "chat_id": row[5],
            "message_id": row[6],
            "feedback": row[7],
            "timestamp": row[8]
        }
        feedback_data.append(item_dict)

    return feedback_data

def save_ticket_info(ticket_info):
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Prepare an SQL query with placeholders for data
    insert_query = """
        INSERT INTO mainpage_ticketinfo_telegram (user_id, username, first_name, last_name, chat_id, message_id, place, quantity, ticket_cost, total_cost, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert each ticket info entry into the database
    for item in ticket_info:
        cursor.execute(insert_query, (item["user_id"], item["username"], item["first_name"], item["last_name"],
                                      item["chat_id"], item["message_id"], item["place"], item["quantity"], item["ticket_cost"], item["total_cost"], item["timestamp"]))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def load_ticket_info():
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Execute a SQL query to fetch all ticket info entries
    select_query = "SELECT * FROM ticket_info"
    cursor.execute(select_query)

    # Fetch all rows from the result set
    ticket_info = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Convert the fetched rows into a list of dictionaries
    ticket_info_data = []
    for row in ticket_info:
        item_dict = {
            "system_id": row[0],            # Fetch system_id from index 0
            "user_id": row[1],              # Assuming user_id is at index 1
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "chat_id": row[5],
            "message_id": row[6],
            "place": row[7],
            "quantity": row[8],
            "ticket_cost": row[9],
            "total_cost": row[10],
            "timestamp": row[11]
        }
        ticket_info_data.append(item_dict)

    return ticket_info_data

def save_report_found(report_info):
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Prepare an SQL query with placeholders for data
    insert_query = """
        INSERT INTO mainpage_reportfound_telegram (user_id, username, first_name, last_name, chat_id, message_id, report_item_description, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert each report found entry into the database
    for item in report_info:
        cursor.execute(insert_query, (item["user_id"], item["username"], item["first_name"], item["last_name"],
                                      item["chat_id"], item["message_id"], item["report_item_description"], item["timestamp"]))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def load_report_found():
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database for loading logs.")
        return []
    cursor = connection.cursor()

    # Execute a SQL query to fetch all report found entries
    select_query = "SELECT * FROM report_found"
    cursor.execute(select_query)

    # Fetch all rows from the result set
    report_found = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Convert the fetched rows into a list of dictionaries
    report_found_data = []
    for row in report_found:
        item_dict = {
            "system_id": row[0],            # Fetch system_id from index 0
            "user_id": row[1],              # Assuming user_id is at index 1
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "chat_id": row[5],
            "message_id": row[6],
            "report_item_description": row[7],
            "timestamp": row[8]
        }
        report_found_data.append(item_dict)

    return report_found_data

# Start command to ask for language selection
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if phone number is available (this will require the user to have shared it)
    phone_number = None
    if update.message.contact:
        phone_number = update.message.contact.phone_number

    # Check if location is available (this will require the user to have shared it)
    location = None
    if update.message.location:
        location = {
            'latitude': update.message.location.latitude,
            'longitude': update.message.location.longitude
        }

    # Create user info dictionary
    user_info = {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'chat_id': chat_id,
        'message_id': message_id,
        'timestamp': timestamp,
        'phone_number': phone_number,
        'location': location
    }

    # Load existing logs, append new data, and save
    #logs = load_logs()
    #logs.append(user_info)
    #save_logs(logs)

    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("हिन्दी", callback_data='lang_hi')],
        [InlineKeyboardButton("தமிழ்", callback_data='lang_ta')],
        [InlineKeyboardButton("മലയാളം", callback_data='lang_ml')],
        [InlineKeyboardButton("ಕನ್ನಡ", callback_data='lang_kn')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select your language:", reply_markup=reply_markup)

# Button handler for language selection
async def language_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'lang_en':
        context.user_data['language'] = 'en'
    elif query.data == 'lang_hi':
        context.user_data['language'] = 'hindi'
    elif query.data == 'lang_ta':
        context.user_data['language'] = 'tamil'
    elif query.data == 'lang_ml':
        context.user_data['language'] = 'malayalam'
    elif query.data == 'lang_kn':
        context.user_data['language'] = 'kannada'

    # Load the selected language file
    lang = load_language(context.user_data['language'])

    # Proceed with bot functionalities after language selection
    keyboard = [
        [InlineKeyboardButton(lang["book_ticket"], callback_data='book')],
        [InlineKeyboardButton(lang["visit_website"], url='https://your-website.com')],
        [InlineKeyboardButton(lang["lost_and_found"], callback_data='lost_found')],
        [InlineKeyboardButton(lang["feedback"], callback_data='feedback')],
        [InlineKeyboardButton(lang["report_found"], callback_data='report_found')],
        [InlineKeyboardButton(lang['child_helpline'], callback_data='child_helpline')],
        [InlineKeyboardButton(lang['emergency_helpline'], callback_data='emergency_helpline')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=lang['start_message'], reply_markup=reply_markup)

# Function to load translated messages dynamically
def get_message(context, key):
    lang_code = context.user_data.get('language', 'en')
    lang = load_language(lang_code)
    return lang.get(key, key)  # Default to key if translation not found

# Book Ticket handler
async def book_ticket(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    lang = load_language(context.user_data['language'])
    places =  ["Egyptian Gallery", "Gandhara Gallery", "Long Archaeology Gallery", "This Minor Art Gallery", "Varanda 1st Floor"]
    ticket_prices = [10, 15, 20, 25, 30]

    # Create an inline keyboard with buttons stacked vertically
    keyboard = [[InlineKeyboardButton(f"{places[i]} - ₹{ticket_prices[i]}", callback_data=f'place_{i}')] for i in range(len(places))]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=lang['select_place'], reply_markup=reply_markup)

# Lost and Found Handler

async def lost_and_found(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    lang = load_language(context.user_data['language'])

    await query.edit_message_text(text=lang['lost_found_prompt'])
    context.user_data['state'] = 'lost_and_found_input'

# Feedback handler
async def feedback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    lang = load_language(context.user_data['language'])

    await query.edit_message_text(text=lang['feedback_prompt'])
    context.user_data['state'] = 'feedback_input'

# Handle Report Found Item
async def report_found_item(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    lang = load_language(context.user_data['language'])

    await query.edit_message_text(text=lang['report_found_prompt'])
    context.user_data['state'] = 'report_found_input'

# Handle Child Helpline
async def child_helpline(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    lang = load_language(context.user_data['language'])

    # Send a message with the contact details for the child helpline
    await query.message.reply_text(lang['contact_message_child'])

    # Maintain the inline keyboard with the same buttons

    keyboard = [
        [InlineKeyboardButton(lang['child_helpline'], callback_data='child_helpline')],
        [InlineKeyboardButton(lang['emergency_helpline'], callback_data='emergency_helpline')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup)

# Handle Emergency Helpline
async def emergency_helpline(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    lang = load_language(context.user_data['language'])
    await query.message.reply_text(lang['contact_message'])

    # Maintain the inline keyboard with the same buttons

    keyboard = [
        [InlineKeyboardButton(lang['child_helpline'], callback_data='child_helpline')],
        [InlineKeyboardButton(lang['emergency_helpline'], callback_data='emergency_helpline')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup)

# Handle the message input for different states
async def handle_message(update: Update, context: CallbackContext) -> None:
    lang = load_language(context.user_data['language'])

    if context.user_data.get('state') == 'lost_and_found_input':
        # Store the lost and found data in the database

        user = update.message.from_user
        chat_id = update.effective_chat.id
        message_id = update.message.message_id

        connection = create_db_connection()
        cursor = connection.cursor()

        # Prepare an SQL query with placeholders for data
        insert_query = """
            INSERT INTO mainpage_lostandfound_telegram (user_id, username, first_name, last_name, chat_id, message_id, description, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (user.id, user.username, user.first_name, user.last_name,
                                      chat_id, message_id, update.message.text, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        connection.commit()
        cursor.close()
        connection.close()

        await update.message.reply_text(lang['lost_found_confirmation'])
        context.user_data['state'] = None

    elif context.user_data.get('state') == 'feedback_input':
        # Store the feedback data in the database

        user = update.message.from_user
        chat_id = update.effective_chat.id
        message_id = update.message.message_id

        connection = create_db_connection()
        cursor = connection.cursor()

        # Prepare an SQL query with placeholders for data
        insert_query = """
            INSERT INTO mainpage_feedback_telegram (user_id, username, first_name, last_name, chat_id, message_id, feedback, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (user.id, user.username, user.first_name, user.last_name,
                                      chat_id, message_id, update.message.text, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        connection.commit()
        cursor.close()
        connection.close()

        await update.message.reply_text(lang['feedback_confirmation'])
        context.user_data['state'] = None

    elif context.user_data.get('state') == 'report_found_input':
        # Store the found report data in the database

        user = update.message.from_user
        chat_id = update.effective_chat.id
        message_id = update.message.message_id

        connection = create_db_connection()
        cursor = connection.cursor()

        # Prepare an SQL query with placeholders for data
        insert_query = """
            INSERT INTO mainpage_reportfound_telegram (user_id, username, first_name, last_name, chat_id, message_id, report_item_description, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (user.id, user.username, user.first_name, user.last_name,
                                      chat_id, message_id, update.message.text, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        connection.commit()
        cursor.close()
        connection.close()

        await update.message.reply_text(lang['report_item_confirmation'])
        context.user_data['state'] = None

    elif context.user_data.get('state') == 'ticket_quantity':
        await handle_ticket_quantity(update, context)

# Handler for ticket place selection and quantity
async def place_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    lang = load_language(context.user_data['language'])
    places =  ["Egyptian Gallery", "Gandhara Gallery", "Long Archaeology Gallery", "This Minor Art Gallery", "Varanda 1st Floor"]
    ticket_prices = [10, 15, 20, 25, 30]

    # Extract place index from callback data
    selected_place = int(query.data.split('_')[1])
    context.user_data['selected_place'] = selected_place

    place = places[selected_place]
    price = ticket_prices[selected_place]
    context.user_data['price'] = price

    await query.edit_message_text(text=lang['ticket_selection_prompt'].format(place=place, price=price))
    context.user_data['state'] = 'ticket_quantity'

# Handle the ticket quantity input
async def handle_ticket_quantity(update: Update, context: CallbackContext) -> None:
    lang = load_language(context.user_data['language'])
    places =  ["Egyptian Gallery", "Gandhara Gallery", "Long Archaeology Gallery", "This Minor Art Gallery", "Varanda 1st Floor"]

    try:
        quantity = int(update.message.text)
        if quantity <= 0 or quantity > 10:
            raise ValueError("Invalid ticket count")
    except ValueError:
        await update.message.reply_text(lang['enter_valid_number'])
        return

    # Ensure 'selected_place' and 'price' are in user_data
    if 'selected_place' not in context.user_data or 'price' not in context.user_data:
        await update.message.reply_text(lang['no_place_selected'])
        return

    # Retrieve stored place and price information
    place = places[context.user_data['selected_place']]
    price = context.user_data['price']
    total_cost = price * quantity

    # Generate QR Code
    qr_data = f"Tickets: {quantity}, Place: {place}, Total Cost: ₹{total_cost}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    bio = BytesIO()
    bio.name = 'ticket.png'
    img.save(bio)
    bio.seek(0)

    # Send the QR code as an image
    await update.message.reply_photo(photo=bio, caption=f"Your ticket(s) for {place}. \nTotal Cost: ₹{total_cost}.")

    user = update.message.from_user
    chat_id = update.effective_chat.id
    message_id = update.message.message_id

    # Store the booking information in the database
    connection = create_db_connection()
    cursor = connection.cursor()

    # Prepare an SQL query with placeholders for data
    insert_query = """
        INSERT INTO mainpage_ticketinfo_telegram (user_id, username, first_name, last_name, chat_id, message_id, place, quantity, ticket_cost, total_cost, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (user.id, user.username, user.first_name, user.last_name,
                                  chat_id, message_id, place, quantity, price, total_cost, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    connection.commit()
    cursor.close()
    connection.close()

    # Clear the state after successful processing
    context.user_data['state'] = None

# Main function to run the bot
def main() -> None:
    application = Application.builder().token(API_TOKEN).build()

    # Add command and callback handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_selection,pattern='^lang_'))
    application.add_handler(CallbackQueryHandler(book_ticket, pattern='^book'))
    application.add_handler(CallbackQueryHandler(lost_and_found, pattern='^lost_found'))
    application.add_handler(CallbackQueryHandler(feedback, pattern='^feedback'))
    application.add_handler(CallbackQueryHandler(report_found_item, pattern='^report_found'))
    application.add_handler(CallbackQueryHandler(child_helpline, pattern='child_helpline'))
    application.add_handler(CallbackQueryHandler(emergency_helpline, pattern='emergency_helpline'))
    application.add_handler(CallbackQueryHandler(place_selection, pattern='^place_'))

    # Register a single message handler that delegates to the correct function based on state
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until interrupted
    application.run_polling()

if __name__ == '__main__':
    main()
