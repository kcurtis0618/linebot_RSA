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
line_bot_api = LineBotApi('Your Channel Access Token')
# 必須放上自己的Channel Secret
handler = WebhookHandler('7e9f7a1238765524eaeedab37d6e534c')

#主動推播
line_bot_api.push_message('Udd9d677bacb9d89bb80323b5c1c9a46a', TextSendMessage(text='歡迎大家來到iLearn_數位簽章，\n已經加入聊天的各位，\n看來是很喜歡數位簽章呢～\n\n接下來請輸入「嗨」，\n開始學習數位簽章吧～\n'))

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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)