#載入LineBot所需要的套件
from flask import Flask, request, abort
import re
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('xkPqDD5FciQ02xBdohNw9E+VDOdaJP7QAAfj4A0XVsQU9v34C5rpZ2Zgb0UyJr+9nTqAdiET9R77wSVhBzML5BdFERXyYX8Mv0JeHEJrx9HmVkaQkPiuEeCmw8avTb45PNdu0HsojRaZxrInUK0OAQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('7e9f7a1238765524eaeedab37d6e534c')
your_id = 'Udd9d677bacb9d89bb80323b5c1c9a46a'
#主動推播
line_bot_api.push_message(your_id, TextSendMessage(text='歡迎大家來到iLearn_數位簽章，\n已經加入聊天的各位，\n看來是很喜歡數位簽章呢～\n\n接下來請輸入「嗨」，\n開始學習數位簽章吧～\n'))

#使用者狀態
user_state = {}

#確認按鈕
confirm_template_message = TemplateSendMessage(
        alt_text='確認開始學習',
        template=ConfirmTemplate(
            text='確認開始學習嗎？',
            actions=[
                MessageAction(label='是',text='開始填寫'),
                PostbackAction(label='不是',data='action=取消')
            ]
        )
    )

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message = event.message.text
    reply_message = []

    if user_id not in user_state:
        user_state[user_id] = {"state": "Normal", "workflow": 0}

    if user_state[user_id]["state"] == "Normal":
        if re.match('嗨',message) or re.match('我想繼續學習',message):
            button_template_message = TemplateSendMessage(
                alt_text='Start talk flow, multiselection button',
                template=ButtonsTemplate(
                    title='開始學習囉',
                    text='請點選下方功能，成為下方角色',
                    actions=[
                        PostbackAction(label='加密者', text='我想當加密者',data='action=encrpytion'),
                        PostbackAction(label='憑證機構', text='我想當憑證公司的上帝視角',data='action=veracation'),
                        PostbackAction(label='解密者', text='我想當解密者',data='action=decryption'),
                    ]
                )
            )
            line_bot_api.reply_message(your_id, button_template_message)
        #加密者
        # elif user_state[user_id]['state'] == "Encryter":
        #     if user_state[user_id]["workflow"] == 0:
        #     if user_state[user_id]["workflow"] == 0:
        #     if user_state[user_id]["workflow"] == 0:
        #憑證
        #解密者
        #未在任何workflow中
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage('抱歉我不太懂你的意思喔～'))
            
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)
    
#利用postback按鈕可以設計一些當按下按鈕後的動作
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    reply_messages = []

    if data == 'action=encrpytion':
        user_state[user_id]["state"] = "Encrypter"
        line_bot_api.reply_message(event.reply_token, confirm_template_message)

    elif data == 'action=veracation':
        user_state[user_id]["state"] = "Veracation"
        line_bot_api.reply_message(event.reply_token, confirm_template_message)

    elif data == 'action=decrpytion':
        user_state[user_id]["state"] = "Decryter"
        line_bot_api.reply_message(event.reply_token, confirm_template_message)
    elif data == 'action=取消':
        user_state[user_id]["state"] = "Normal"
        line_bot_api.reply_message(event.reply_token,TextSendMessage('否'))


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)