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
def carikamar(nomor):
    URLkamar = "http://www.aditmasih.tk/api_lutfyh/show.php?nomor=" + nomor
    r = requests.get(URLkamar)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        nomor = data['kamar'][0]['nomor']
        status = data['kamar'][0]['status']
        tipe = data['kamar'][0]['tipe']
        harga = data['kamar'][0]['harga']
        atas_nama = data['kamar'][0]['atas_nama']
        hp = data['kamar'][0]['hp']
        

        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['teman'][0]
        data= "Nomor kamar: "+nomor+"\nStatus : "+status+"\nTipe kamar: "+tipe+"\nHarga kamar : "+harga+"\nPemilik "+atas_nama+"\n Nomor Hp :" +hp
        return data
        # return all_data

    elif(flag == "0"):
        return err

#INPUT DATA teman
def inputkamar(nomor,status,tipe,harga,atas_nama,hp):
    r = requests.post("http://www.aditmasih.tk/api_lutfyh/insert.php", data={'nomor': nomor, 'status': status, 'tipe': tipe, 'harga': harga, 'atas_nama':atas_nama, 'hp':hp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'


#DELETE DATA teman
def hapuskamar(nomor):
    r = requests.post("http://www.aditmasih.tk/api_lutfyh/delete.php", data={'nomor': nomor})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data kamar nomor '+nomor+'atas nama'+atas_nama+' dengan kontak '+hp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

def updatekamar(hp_lama,nomor,status,tipe,harga,atas_nama,hp):
    URLteman = "http://www.aditmasih.tk/api_lutfyh/show.php?hp=" + hp_lama
    r = requests.get(URLkamar)
    data = r.json()
    err = "data tidak ditemukan"
    hpLama=hp_lama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api_lutfyh/update.php", data={'nomor': nomor, 'status': status, 'tipe': tipe, 'harga': harga, 'atas_nama':atas_nama, 'hp':hp, 'hpLama' :hpLama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data kamar nomor '+nomor+ 'atas nama '+atas_nama+' berhasil diupdate\n'
        elif(flag == "0"):
            return 'Data gagal diupdate\n'

    elif(flag == "0"):
        return err

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

    data=text.split('-')
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carikamar(data[1])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputkamar(data[1],data[2],data[3],data[4],data[5],data[6])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapuskamar(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatekamar(data[1],data[2],data[3],data[4],data[5],data[6],data[7])))
    elif(data[0]=='menu'):
        menu = "Bot ini digunakan untuk data apartemen di suatu apartemen\nBagaimana cara kerjanya?\n1. lihat [nomor apartemen]\n2. tambah [nomor kamar]-[status kamar(isi/kosong)]-[tipe(studio/2BR/3BR dst)]-[harga per bulan]-[pemiliknya]-[Nomor Hp Pemilik]"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = menu))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "Coba pakai keyword yang bener deh, ketik menu coba buat cek keywordnya"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
