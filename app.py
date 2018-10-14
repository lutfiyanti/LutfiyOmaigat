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
line_bot_api = LineBotApi('w3scpD6SKPEamgZPLSSAVZjPhP1C12+PXgXDdkrlEtCIAPoICgPdaHdlMwJV8ykiqDM9Y9i/X9UvhfGu13D2gI4J55LtiRUDnrHJ/OsJ/riStdx+rkSvrdFZCHiiCc6ekKJYZ5kXi+TSHGPaBAqiSAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('89fda4e9bbd8c74be8079f3069fe24e4')
#===========[ NOTE SAVER ]=======================
notes = {}

#REQUEST DATA MHS
def caribuku(aidi):
    URLmhs = "http://www.aditmasih.tk/api-lutfyh/show.php?aidi=" + aidi
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        aidi = data['data_buku'][0]['aidi']
        judul = data['data_buku'][0]['judul']
        penerbit = data['data_buku'][0]['penerbit']
        tahun= data['data_buku'][0]['tahun']

        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= "Id : "+aidi+"\nJudul : "+judul+"\n Penerbit : "+penerbit+"\n Tahun :"+tahun
        return data
        # return all_data

    elif(flag == "0"):
        return err

#INPUT DATA MHS
def inputbuku(aidi, judul, penerbit, tahun):
    r = requests.post("http://www.aditmasih.tk/api-lutfyh/insert.php", data={'aidi': aidi, 'judul': judul, 'penerbit': penerbit, 'tahun':tahun})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+judul+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def allbuku():
    r = requests.post("http://www.aditmasih.tk/api-lutfyh/all.php")
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        hasil = ""
        for i in range(0,len(data['data_buku'])):
            aidi = data['data_buku'][int(i)][0]
            judul = data['data_buku'][int(i)][2]
            penerbit = data['data_buku'][int(i)][4]
            tahun = data['data_buku'][int(i)][6]
            hasil=hasil+str(i+1)
            hasil=hasil+".\nId : "
            hasil=hasil+aidi
            hasil=hasil+"\nJudul : "
            hasil=hasil+judul
            hasil=hasil+"\nPenerbit : "
            hasil=hasil+penerbit
            hasil=hasil+"\nTahun : "
            hasil=hasil+tahun
            hasil=hasil+"\n"
        return hasil
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'


#DELETE DATA MHS
def hapusbuku(aidi):
    r = requests.post("http://www.aditmasih.tk/api-lutfyh.php", data={'aidi': aidi})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+aidi+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

def updatebuku(aidiLama,aidi,judul,penerbit, tahun):
    URLmhs = "http://www.aditmasih.tk/api-lutfyh/show.php?nrp=" + aidiLama
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    aidi_lama=aidiLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api-lutfyh/update.php", data={'aidi': aidi, 'judul': judul, 'penerbit': penerbit, 'tahun' : tahun 'aidi_lama':aidi_lama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data '+aidi_lama+'berhasil diupdate\n'
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
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=caribuku(data[1])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputbuku(data[1],data[2],data[3], data[4])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusbuku(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatebuku(data[1],data[2],data[3],data[4], data[5])))
    elif(data[0]=='semua'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=allbuku()))
    elif(data[0]=='menu'):
        menu = "1. lihat-[Id]\n2. tambah-[Id]-[judul]-[penerbit]-[tahun]\n3. hapus-[Id]\n4. ganti-[Id lama]-[Id baru]-[judul baru]-[penerbit baru]-[tahun baru]\n5. semua"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
