#@LydiaTeam

from rubpy import Client as rClient, press
from rubpy.crypto import Crypto
import asyncio, time, telebot, ast, os, random
from telebot import types
from time import sleep
#from threading import Thread


bot = telebot.TeleBot("")
admins = [75275327, 8786745445]
information = {}
firstNames = ['turk', 'masih', 'yak', 'sara', 'zanturk', 'turkzerang', 'turkkhob']
lastNames = ['khar', 'zeba', 'khoshlebas', '8seland', 'jungle', 'bahosh', 'faheshe']

if not os.path.exists('./sessions'):
    os.mkdir('./sessions')


async def Login(phone:str, chat_id, res, authcode):
    app = rClient(session=f'./sessions/{chat_id}/{phone}')
    await app.connect()
    public_key, app._private_key = Crypto.create_keys()
    m = await app(press.authorisations.SignIn(phone_code=authcode, phone_number=phone, phone_code_hash=res.phone_code_hash, public_key=public_key))
    if m.status == "OK":
        return m
        

async def sendAuthCode(phone:str, chat_id):
    if not os.path.exists(f"./sessions/{chat_id}"):
        os.mkdir(f'./sessions/{chat_id}')
    app = rClient(session=f'./sessions/{chat_id}/{phone}')
    await app.connect()
    res = await app(press.authorisations.SendCode(phone_number=phone))
    print(res)

    return res
    

#Defs 
def phoneFinder(chat_id):
    global information
    try:
        information[chat_id]['Phone']
    except:
        information[chat_id] = {'Phone': 'None', 'Status': 'LydiaTeam'}

    return str(information[chat_id]['Phone'])


def makeKeyboard(chat_id):

    markup = types.InlineKeyboardMarkup()
    
    markup.add(types.InlineKeyboardButton(text="📞Phone :",
                                              callback_data="ohkt"),

        types.InlineKeyboardButton(text=f"{phoneFinder(chat_id)}",
                                   callback_data="selectNumber")),     
                       
    markup.add(types.InlineKeyboardButton(text="👤 addAccount",
                                              callback_data="addaccount"),

        types.InlineKeyboardButton(text="📂 accountManager",
                                   callback_data="accountmanager")),
    
    markup.add(types.InlineKeyboardButton(text="☎️ sendToContacts",
                                    callback_data="scontacts"),
                types.InlineKeyboardButton(text="👥 sendToCahts",
                                   callback_data="schats")),
    
    markup.add(types.InlineKeyboardButton(text="1️⃣ sendToSingleNumber",
                                    callback_data="sendtosinglenumber"))

    markup.add(types.InlineKeyboardButton(text="🔗 sendToAll",
                                              callback_data="sendtoall"))
  
    
    markup.add(types.InlineKeyboardButton(text="🗂addContacts",
                                              callback_data="addcontacts"),
        types.InlineKeyboardButton(text=f"🗂 removeAllContacts",
                                   callback_data="rmcontacts"))  
    
    markup.add(types.InlineKeyboardButton(text="Set Text",
                                        callback_data="settext"))
    return markup


def accountManagerButtons(chat_id):
    try:
        info = asyncio.run(getAccountInfo(chat_id))

        try:
            chats, contacts = asyncio.run(getCountOfChatsAndContacts(chat_id)) 
        except:
            chats, contacts = 0

        markup = types.InlineKeyboardMarkup()
        
        markup.add(types.InlineKeyboardButton(text="📞 Phone :",
                                                callback_data="ohkt"),
            types.InlineKeyboardButton(text=f"{phoneFinder(chat_id)}",
                                    callback_data="gdgdgdgdg")),     
                        
        markup.add(types.InlineKeyboardButton(text="👤 Name :",
                                                callback_data="hdhfdh"),
            types.InlineKeyboardButton(text=f"{info.user.first_name}",
                                    callback_data="sdfsfsdfdsf")),
        
        markup.add(types.InlineKeyboardButton(text="✏️ Bio ",
                                        callback_data="gsgsgsd"),
                    types.InlineKeyboardButton(text=f"{info.user.bio}",
                                    callback_data="gsgsgsg")),
        
        markup.add(types.InlineKeyboardButton(text="🗳 Guid",
                                                callback_data="sgsffsf"),
            types.InlineKeyboardButton(text=f"{info.user.user_guid}",
                                    callback_data="sfsdfdsf"))  
        
        markup.add(types.InlineKeyboardButton(text="👥☎️Chats & Contacts :",
                                                callback_data="sgsffsf"),
                    types.InlineKeyboardButton(text=f"{chats} | {contacts}",
                                                callback_data="sfsdfdsf"))  
        
        
        markup.add(types.InlineKeyboardButton(text="🌄 Change Profile",
                                            callback_data="settings"))
        
        markup.add(types.InlineKeyboardButton(text="🔌TerminateAllSessions",
                                            callback_data="settings"))
        
        markup.add(types.InlineKeyboardButton(text="Back",
                                                        callback_data="back")) 

        return markup
    
    except: 
        pass

def confirmCode(message, msgid, res, number):
   try:
        chat_id = message.chat.id
        authcode = message.text
        if message.text.isdigit():

            bot.delete_message(chat_id, msgid)
            response = asyncio.run(Login(str(number), chat_id, res, authcode))
            if response.status == "OK":
                print(response)

                msg = f'''

✅ New account has been seccussfully added .
📞 Phone : {number}
👤 Name : {response.first_name}
🗳 Guid : {response.user_guid}

/check_09125869_100&200
/login_{number}
    '''
                
                if not os.path.isfile(f'./sessions/{chat_id}/numbers.lst'):
                    open(f'./sessions/{chat_id}/numbers.lst', 'w').write("1\n")

                open(f'./sessions/{chat_id}/numbers.lst', 'a').write(f"{number}\n")
                information[chat_id]['Phone'] = number

                bot.send_message(chat_id, msg)

            else:
                os.remove(f'{number}.rbs')
                bot.send_message(chat_id, 'Invalid Auth Code :/')

        else:
            bot.send_message(chat_id, 'invalid data :/')
   except:
        bot.send_message(chat_id, 'invalid data :/')
        os.remove(f'{number}.rbs')

def addAccount(message, msgid):
   #try:
        chat_id = message.chat.id
        number = message.text
        if message.text.isdigit():

            bot.delete_message(chat_id, msgid)
            response = asyncio.run(sendAuthCode(str(number), chat_id))
            input_text_auth = bot.send_message(chat_id, f'🪜 i have sent authCode for {number} check it out and give it to me :')
            bot.register_next_step_handler(input_text_auth, confirmCode, input_text_auth.message_id, response, number)

        else:
            bot.send_message(chat_id, 'invalid data :/')
   #except:
        #bot.send_message(chat_id, 'invalid data :/')    
    
def checknumbers(num:list):

    for number in num:
        listnumber = list(number)

        if not number.isdigit():
            result = False
            break

        elif not number.startswith("09"):
            result = False
            break

        elif not len(listnumber) == 11: 
            result = False
            break

        elif number.isdigit():
            result = True
    
    return result

async def importContact(chat_id, phone, fName, lName):
    try:
        app = rClient(session=f'./sessions/{chat_id}/{phoneFinder(chat_id)}')
        await app.connect()
        insertContact = await app.add_address_book(phone, fName, lName)
        return insertContact
    except:
        print('importContact')
    
def addContacts(message, chat_id, msgid):
    bot.delete_message(chat_id, msgid)

    try:

        if message.text:

            numbers = message.text.splitlines()

            if checknumbers(numbers):

                msg1 = bot.send_message(chat_id, "⏰ Loading ...")


                existence = []
                failure = []

                for number in numbers:
                    newnum = number.replace('09', '989')
                    response = asyncio.run(importContact(chat_id, newnum, f"{random.choice(firstNames)}{random.randint(0, 10000)}", f"{random.choice(lastNames)}"))
                    if response.user_exist:
                        existence.append(newnum)
                    else:
                        failure.append(newnum)

                bot.edit_message_text(f"✅ import action finished successfully.\n🔎 Existence : {len(existence)}\n❌ Failure : {len(failure)} ", chat_id, msg1.message_id)

            else:
                bot.send_message(chat_id, 'invalid numbers :/')
    except:
        print('addContacts')

async def deleteAllContacts(chat_id):
    try:
        msg1 = bot.send_message(chat_id, "⏰ Loading ...")

        app = rClient(session=f'./sessions/{chat_id}/{phoneFinder(chat_id)}')
        await app.connect()

        contactss = await app.get_contacts()
        if contactss.users:
            total = len(contactss.users)
            print(total)

            for index, contact in enumerate(contactss.users, start=1):
                try:
                    #u can call index and get position 
                    removal = await app.delete_contact(str(contact.user_guid))        
                except Exception:
                    pass

            bot.edit_message_text(f"✅ Removal action finished successfully\n{total}.", chat_id, msg1.message_id)
    except:
        pass

async def sendToAllContacts(chat_id):
        
    app = rClient(session=f'./sessions/{chat_id}/{phoneFinder(chat_id)}')
    await app.connect()
    

    msg1 = bot.send_message(chat_id, "⏰ Loading ...")

    existence = []
    failure = []


    try:
        information[chat_id]['Text']
    except:
        information[chat_id]['Text'] = 'Default'
    
    
    contactss = await app.get_contacts()
    if contactss.users:
        total = len(contactss.users)
        for index, contact in enumerate(contactss.users, start=1):
            print(str(contact.user_guid))
            if round(int(time.time()) - int(contact.last_online)) <= 86400:
                try:
                    res = await app.send_message(str(contact.user_guid), str(information[chat_id]['Text']))
                    await app.delete_user_chat(str(contact.user_guid), str(res.message_update.message_id))
                    existence.append(contact.user_guid)
                except:
                    failure.append(contact.user_guid)
            else:
                failure.append(contact.user_guid)

        
        bot.edit_message_text(f"✅ sendToAllContacts action finished successfully.\n🔎 Existence : {len(existence)}\n❌ Failure : {len(failure)}\n📂 Total : {total} ", chat_id, msg1.message_id)

async def sendToAllChats(chat_id):

    app = rClient(session=f'./sessions/{chat_id}/{phoneFinder(chat_id)}')
    await app.connect()

    msg1 = bot.send_message(chat_id, "⏰ Loading ...")

    existence = []
    failure = []

    try:
        information[chat_id]['Text']
    except:
        information[chat_id]['Text'] = 'Default'
    
    chats = await app.get_chats(start_id=None)
    if chats.chats:
        total = len(chats.chats)
        for index, chat in enumerate(chats.chats, start=1):
            try:
                res = await app.send_message(str(chat.object_guid), str(information[chat_id]['Text']))
                await app.delete_user_chat(str(chat.object_guid), str(res.message_update.message_id))
                existence.append(chat.object_guid)
            except:
                failure.append(chat.object_guid)

        bot.edit_message_text(f"✅ sendToAllChats action finished successfully.\n🔎 Existence : {len(existence)}\n❌ Failure : {len(failure)}\n📂 Total : {total} ", chat_id, msg1.message_id)

async def getCountOfChatsAndContacts(chat_id):
    app = rClient(session=f'./sessions/{chat_id}/{phoneFinder(chat_id)}')
    await app.connect()

    chats = await app.get_chats(start_id=None)
    contactss = await app.get_contacts()

    return len(chats.chats), len(contactss.users)


def loginToPhone(message):
    Text = message.text.split('_')
    Chatid = message.chat.id
    if message.text:
        information[Chatid]['Phone'] = Text[1]
        bot.send_message(chat_id=message.chat.id,
            text="~ @LydiaTeam",
            reply_markup=makeKeyboard(message.chat.id),
            parse_mode='HTML')


async def sendToSingleNumber(chat_id, Guid:str):
    try:
        information[chat_id]['Text']
    except:
        information[chat_id]['Text'] = 'Default'

    app = rClient(session=f'./sessions/{chat_id}/{phoneFinder(chat_id)}')
    await app.connect()

    res = await app.send_message(str(Guid), str(information[chat_id]['Text']))
    await app.delete_user_chat(str(Guid), str(res.message_update.message_id)) 

def sendToSingle(message, msgid):
    try:
        if message.text:
            Chatid = message.chat.id
            PhoneNumber = message.text
            bot.delete_message(Chatid, msgid)

            response = asyncio.run(importContact(Chatid, PhoneNumber, random.choice(firstNames), random.choice(lastNames)))
            if response.user_exist:
                res = asyncio.run(sendToSingleNumber(Chatid, str(response.user.user_guid)))
                print(res)
                bot.send_message(Chatid, f"✅ message successfully sent to {PhoneNumber}")
            else:
                bot.send_message(Chatid, "❌ number doesnt exist")
    except:
        pass

async def getAccountInfo(chat_id):

    app = rClient(session=f'./sessions/{chat_id}/{phoneFinder(chat_id)}')
    await app.connect()

    return await app.get_me()

async def getAccountSessions(chat_id):
    app = rClient(session=f'./sessions/{chat_id}/{phoneFinder(chat_id)}')
    await app.connect()

    return await app.get_my_sessions()

def settext(message, msgid):
    if message.text:
        Chatid = message.chat.id
        bot.delete_message(Chatid, msgid)
        information[Chatid]['Text'] = str(message.text)
        bot.send_message(Chatid, "The text has been set successfully.")


@bot.message_handler(commands=['start'])
def handle_command_adminwindow(message):
    if message.chat.id in admins:
        chat_id = message.chat.id

        bot.send_message(chat_id=message.chat.id,
                        text="~ @LydiaTeam",
                        reply_markup=makeKeyboard(message.chat.id),
                        parse_mode='HTML')
        

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        global appdata, loadingProccess
        chat_id = call.message.chat.id
        if call.message.chat.id in admins:
            if (call.data.startswith("['value'")):
                pass

            if (call.data == "addaccount"):
                input_text = bot.send_message(chat_id, '📞 Please send me your number (9125982416) :')
                bot.register_next_step_handler(input_text, addAccount, input_text.message_id)
            

            elif (call.data == "selectNumber"):
                if not os.path.isfile(f'./sessions/{chat_id}/numbers.lst'):
                    bot.answer_callback_query(callback_query_id=call.id,
                        show_alert=True,
                        text=f"❌ u have to fist add account")
                else:
                    numberLists = open(f'./sessions/{chat_id}/numbers.lst', 'r').read().splitlines()
                    markup = types.InlineKeyboardMarkup()
                    for number in numberLists:
                        markup.add(types.InlineKeyboardButton(text=number,
                                                    callback_data=f"number_{number}"),
                            types.InlineKeyboardButton(text=f"❌",
                                                    callback_data=f"remove_{number}"))     

                    markup.add(types.InlineKeyboardButton(text="Back",
                                                          callback_data="back"))
                    bot.edit_message_text(chat_id=chat_id,
                        message_id=call.message.message_id,
                        text=f"~ @LydiaTeam\nNumbers :",
                        reply_markup=markup,
                        parse_mode='HTML')
                    
            elif (call.data.startswith("number_")):
                numberFromCallBack = call.data.split('_')
                information[chat_id]['Phone'] = numberFromCallBack[1]
                bot.edit_message_text(chat_id=chat_id,
                    message_id=call.message.message_id,
                    text=f"~ @LydiaTeam\nNumbers :",
                    reply_markup=makeKeyboard(call.message.chat.id),
                    parse_mode='HTML')
                    
            elif (call.data == "back"):
                bot.edit_message_text(chat_id=chat_id,
                    message_id=call.message.message_id,
                    text=f"~ @LydiaTeam\nNumbers :",
                    reply_markup=makeKeyboard(call.message.chat.id),
                    parse_mode='HTML')
                
            elif (call.data == "addcontacts"):
                input_text = bot.send_message(chat_id, '📞 Please send me your numbers :  \n09125698321\n09124789632')
                bot.register_next_step_handler(input_text, addContacts, chat_id, input_text.message_id)   

            elif (call.data == "settext"):
                input_text = bot.send_message(chat_id, 'Text :')
                bot.register_next_step_handler(input_text, settext, input_text.message_id)   

            elif (call.data == "rmcontacts"):
                markup = types.InlineKeyboardMarkup()  
                markup.add(types.InlineKeyboardButton(text="✅",
                                                          callback_data="confirmRemoval"))
                markup.add(types.InlineKeyboardButton(text="Back",
                                                        callback_data="back")) 
                bot.edit_message_text(chat_id=chat_id,
                        message_id=call.message.message_id,
                        text=f"Are u sure u want to remove all your contacts ?",
                        reply_markup=markup,
                        parse_mode='HTML')
              
            elif (call.data == "confirmRemoval"):
                asyncio.run(deleteAllContacts(chat_id))

            elif (call.data == "scontacts"):
                asyncio.run(sendToAllContacts(chat_id))

            elif (call.data == "schats"):
                asyncio.run(sendToAllChats(chat_id))
            
            elif (call.data == "sendtoall"):
                asyncio.run(sendToAllContacts(chat_id))
                sleep(30)
                asyncio.run(sendToAllChats(chat_id))
                


            elif (call.data == "sendtosinglenumber"):
                input_text = bot.send_message(chat_id, '📞 Please send me your number (989124329426):')
                bot.register_next_step_handler(input_text, sendToSingle, input_text.message_id) 

            elif (call.data == "accountmanager"):
                if not os.path.isfile(f'./sessions/{chat_id}/numbers.lst'):
                    bot.answer_callback_query(callback_query_id=call.id,
                        show_alert=True,
                        text=f"❌ u have to fist add account")
                else:
                    bot.answer_callback_query(callback_query_id=call.id,
                        show_alert=True,
                        text=f"Loading ...")
                    
                    bot.edit_message_text(chat_id=chat_id,
                        message_id=call.message.message_id,
                        text=f"AccountManager :",
                        reply_markup=accountManagerButtons(chat_id),
                        parse_mode='HTML')
                    

    except:
        pass


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.content_type == "text":
        if message.chat.id in admins:
            if message.text.startswith("/login_"):
                loginToPhone(message)

            elif message.text.startswith("/check_"):
                if not os.path.isfile(f'./sessions/{message.chat.id}/numbers.lst'):
                    bot.send_message(message.chat.id, "❌ did u forget to select an account dumbass ?")
                else:
                    pass
                    #organize_numbers(message)

bot.infinity_polling()
#@LydiaTeam
