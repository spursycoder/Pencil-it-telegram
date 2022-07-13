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
    Here are the commands:
/start-> to begin
/help-> to list commands
/about-> details about the bot
/donate->details for donation
/contact->developer details for contacting
No need to give any command for the image conversion,
just upload the image and watch the magic happen
    ''')

def text_handler(update,context):
    update.message.reply_text('''
    Please send an image to generate a sketch
or use /help command for help
    ''')

def donate(update,context):
    update.message.reply_text('''
    I know it's difficult times which is why I have made the bot free, but the bot also does have running costs which incase a certain quota exceeds, I have to pay.
If you think you can make a contibution, it would go a long way in helping me and motivating me to do more projects like this.
You can donate via the following links:
Buy me a coffee-> https://www.buymeacoffee.com/dev.stephno
Paypal-> https://paypal.me/aastlestephno
For Indian users:
UPI ID-> dev.stephno@apl
Thank you :)
    ''')

def contact(update,context):
    update.message.reply_text('''
    You can contact me via the username @gl1tch1e in telegram
Or hit me up via twitter-> https://twitter.com/dev_stephno
    ''')

def about(update,context):
    update.message.reply_text('''
    This bot is built using python. It is absolutely free to use, however you can consider to /donate to help me cover the running costs.
For better results please provide a high resolution image. If you want to fine tune your image, you can go to your local editor and increase the contrast while decreasing the brightness. It has proved to provide a more pencil-esque effect.
If you encounter any bugs or have any suggestions, feel free to /contact me.
    ''')

def doc_handler(update,context):
    update.message.reply_text('''
    Please send your image as a photo and not a document.
Refer to the below image for better understanding.
    ''')
    context.bot.send_photo(chat_id=update.message.chat.id,photo=open("demo.png","rb"))



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
    disp.add_handler(CommandHandler("about",about))
    disp.add_handler(CommandHandler("contact",contact))
    disp.add_handler(CommandHandler("donate",donate))
    disp.add_handler(MessageHandler(Filters.photo,photo_handler))
    disp.add_handler(MessageHandler(Filters.text,text_handler))
    disp.add_handler(MessageHandler(Filters.document,doc_handler))

    updater.start_polling()
    updater.idle()
    

if __name__=='__main__':
    main()


