from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile
import requests
import re
import requests, json

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('N+2Dyafq9MU7670K9Tu6TPdxzdTmCI6DW2zk/2GFHEpqzU76krjB8FqSdsOQPxsK8yk/W5LZMtgMKSNMuzCU7PtY2oj/2lYCl2+5J/IXtXRmXAeYt5TndqaDm7fFYOmeb4QmeHGd6q1A7txOpP7ZoAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('acd0a3afda7cfff11db1ef4a0c81e498')
#===========[ NOTE SAVER ]=======================
notes = {}

#input mencari
def cariproduk(nama_produk):
    URLproduk = "http://api.agusadiyanto.net/halal/?menu=nama_produk&query=" + nama_produk
    r = requests.get(URLproduk)
    produk = r.json()
    err = "Produk tidak ada di database kami, ada beberapa kemungkinan antara lain :\n1. Sertifikasi halal sudah tidak valid.\n2. Produk masih dalam proses untuk mendapatkan sertifikasi halal.\n3. Anda salah mengetik nama produk.\nApabila anda masih ingin memastikan silahkan cek di web resmi MUI ilang.in/ProdukHalal\nTerimakasih :)"
    
    status = produk['status']
    if(status == "success"):
        data = ''
        # for i in produk['data']:
        for i in range(0, len(produk['data'])):
            nama_produk = produk['data'][i]['nama_produk']
            nomor_sertifikat = produk['data'][i]['nomor_sertifikat']
            nama_produsen = produk['data'][i]['nama_produsen']
            berlaku_hingga = produk['data'][i]['berlaku_hingga']
        

            # munculin semua, ga rapi, ada 'u' nya
            # all_data = data['teman'][0]
            data= data + "\nNama Produk : "+nama_produk+"\nNomor Sertifikat : "+nomor_sertifikat+"\nNama Produsen : "+nama_produsen+"\nBerlaku Hingga : "+berlaku_hingga+"\n"
            # return all_data
        return (data)

    elif(status == "error"):
        return (err)
import requests, json

def cariproduk(nama_produsen):
    URLproduk = "http://api.agusadiyanto.net/halal/?menu=nama_produsen&query=" + nama_produsen
    r = requests.get(URLproduk)
    produk = r.json()
    err = "Mungkin nama produsen yang anda masukan salah atau produk dari produsen tersebut belum terdaftar.\nJika anda masih ragu, silahkan cek ilang.in/ProdukHalal \nTerimaksih :)"
    
    status = produk['status']
    if(status == "success"):
        data = ''
        # for i in produk['data']:
        for i in range(0, len(produk['data'])):
            nama_produk = produk['data'][i]['nama_produk']
            nomor_sertifikat = produk['data'][i]['nomor_sertifikat']
            nama_produsen = produk['data'][i]['nama_produsen']
            berlaku_hingga = produk['data'][i]['berlaku_hingga']
        

            # munculin semua, ga rapi, ada 'u' nya
            # all_data = data['teman'][0]
            data= data + "\nNama Produk : "+nama_produk+"\nNomor Sertifikat : "+nomor_sertifikat+"\nNama Produsen : "+nama_produsen+"\nBerlaku Hingga : "+berlaku_hingga+"\n"
            # return all_data
        return (data)

    elif(status == "error"):
        return (err)


cariproduk ("KAO")
    

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receive message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)

    produk=text.split('-')
    if(produk[0]=='produk'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Halo "+profile.display_name+", berikut adalah produk bersertifikasi halal dari hasil pecarian "+event.message.text+"\n"+text=cariproduk(produk[1])))
    elif(produk[0]=='produsen'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Halo "+profile.display_name+", berikut adalah produk bersertifikasi halal dari hasil pecarian "+event.message.text+"\n"+cariprodusen(produk[1])))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "Coba pakai keyword yang bener deh, ada dua menu :\n1. produk-(nama produk)\n2. produsen-(nama produsen)"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
