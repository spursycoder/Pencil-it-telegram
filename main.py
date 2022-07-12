from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler ,MessageHandler
from telegram.ext import MessageHandler, Filters
import cv2
from io import BytesIO
import numpy as np

def start(update,context):

    update.message.reply_text('''
    Hello !
Welcome to Pencil-it bot!
I'm a bot that converts your images into pencil art :)
Use /help for commands or 
just go ahead and send an image to the bot 
and get a sketch as a reply.

    ''')
    

def help(update,context):
    update.message.reply_text('''
    nothing much to say for now
just send an image and 
get the sketched version of it
    ''')

def text_handler(update,context):
    update.message.reply_text('''
    Kindly send an image to generate a sketch
    ''')

def darken(update,context):
    pass

def lighten(update,context):
    pass

def premium_check(update,context):
    pass



def photo_handler(update,context):
    print('Photo received')
    file = context.bot.get_file(update.message.photo[-1].file_id)
    print(type(file))
    f=BytesIO(file.download_as_bytearray())
    file_bytes=np.asarray(bytearray(f.read()),dtype=np.uint8)
    img=cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)    
    cnvrt=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(cnvrt)
    blur=cv2.GaussianBlur(invert,(21,21),0)
    invertedblur=cv2.bitwise_not(blur)
    sketch=cv2.divide(cnvrt,invertedblur,scale=230.0)
    cv2.imwrite("s.png",sketch)
    context.bot.send_photo(chat_id=update.message.chat.id,photo=open("s.png","rb"))

    

def main():
    TOKEN='5433195086:AAFR7DyUoR9z_4bor-lHGGeHHY3HqDUKo3Q'
    updater=Updater(TOKEN,use_context=True)
    disp=updater.dispatcher
    disp.add_handler(CommandHandler("start",start))
    disp.add_handler(CommandHandler("help",help))
    disp.add_handler(MessageHandler(Filters.photo,photo_handler))
    disp.add_handler(MessageHandler(Filters.text,text_handler))
    updater.start_polling()
    updater.idle()
    

if __name__=='__main__':
    main()


