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
                MessageAction(label='是',text="開始學習囉～"),
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

    #中斷學習
    if message == "我不想學習了！":
        user_state[user_id]["state"] = "Normal"
        user_state[user_id]["workflow"] = 0
        line_bot_api.reply_message(event.reply_token, TextSendMessage("已結束學習，若想重新開始學習，按下圖文選單即可"))
        
    elif user_state[user_id]["state"] == "Normal":
        if re.match('嗨',message) or re.match('了解',message):
            button_template_message = TemplateSendMessage(
                alt_text='Start talk flow, multiselection button',
                template=ButtonsTemplate(
                    title='開始學習囉',
                    text='請點選下方功能，成為下方角色',
                    actions=[
                        PostbackAction(label='加密者',data='action=encrpytion'),
                        PostbackAction(label='憑證機構',data='action=veracation'),
                        PostbackAction(label='解密者',data='action=decryption'),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, button_template_message)
        #Branch 1
        #加密者
    elif user_state[user_id]["state"] == "Encrypter":
        if user_state[user_id]["workflow"] == 0:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("小明資訊：\n公鑰（public key）：iLoveYou\n發送訊息內容：我想認識你\n\n請遵循上述進行以下任務\n\n請輸入欲發送訊息！！！"))
            user_state[user_id]["workflow"] += 1
            
        elif user_state[user_id]["workflow"] == 1:
            if message == '我想認識你':
                line_bot_api.reply_message(event.reply_token, TextSendMessage("成功輸入訊息👍\n\n請輸入使用公鑰："))
                user_state[user_id]["workflow"] += 1
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入訊息失敗，請輸入正確訊息"))
                    
        elif user_state[user_id]["workflow"] == 2:
            if message == 'iLoveYou':
                user_state[user_id]["workflow"] = 0
                user_state[user_id]["state"] = "Normal"
                line_bot_api.reply_message(event.reply_token, TextSendMessage("您已成功輸入公鑰👍\n\n您加密的文字為：\nd3j3kj348fkr9rj3o2j2ke3j4ldn32\n\n如要繼續進行請輸入「了解」，若想中斷學習可以點選下方圖文選單"))
                
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入公鑰失敗，請輸入正確鑰匙"))


        #憑證
    elif user_state[user_id]["state"] == "Veracation":
        if user_state[user_id]["workflow"] == 0:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("先來學習憑證授權單位 (CA) ：\n憑證授權單位是類似公證處的單位。 憑證授權單位 (CA)：該單位會發出數位憑證、簽章憑證以驗證有效性，以及追蹤哪些憑證已遭撤銷或已過期。\n\n為保障簽署的合法性，憑證需以下幾點：\n1. 有效公鑰\n2. 簽章憑證：須包含憑證機構、發送者（加密者）、時間戳記\n\n這樣憑證機構才可以將能夠成功保證簽章合法喔～\n學會了請回覆「ok」，進行測驗！"))
            user_state[user_id]["workflow"] += 1
            
        elif user_state[user_id]["workflow"] == 1:
            if message == 'ok':
                confirm_template = ConfirmTemplate(
                    text="以下用戶跟您申請過鑰匙，下列為姓名及公鑰：\n小丑：CrazyRabbit \n小雞：ToBeContinue \n小明：iLoveYou \n小巴：iLoveXiaoMing\n\n底下是剛剛發送的簽章憑證：\n發送者：小雞\n簽發機構：NCNU\n發送時間：2023.12.26\n\n請問是底下簽章憑證是否合法？",
                    actions=[
                        MessageAction(label="是", text="是"),
                        MessageAction(label="否", text="否")
                    ]
                )
                template_message = TemplateSendMessage(alt_text="簽章憑證確認", template=confirm_template)
                line_bot_api.reply_message(event.reply_token, template_message)
                user_state[user_id]["workflow"] += 1
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("看來你不太了解，請仔細閱讀，閱讀完成後可以再次輸入「ok」"))
                    
        elif user_state[user_id]["workflow"] == 2:
            if message == "是":
                user_state[user_id]["workflow"] = 0
                user_state[user_id]["state"] = "Normal"
                line_bot_api.reply_message(event.reply_token, TextSendMessage("100分，看來對你來說太簡單了🤔\n\n如要繼續進行請輸入「了解」，若想中斷學習可以點選下方圖文選單"))
                
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("思考一下，再輸入一次"))


    #解密者
    elif user_state[user_id]["state"] == "Decryter":
        if user_state[user_id]["workflow"] == 0 or message == "ok":
            line_bot_api.reply_message(event.reply_token, TextSendMessage("您收到一則加密訊息：d3j3kj348fkr9rj3o2j2ke3j4ldn32\n\n請選擇鑰匙："))
            confirm_template = ConfirmTemplate(
                text="小明您好，\n您收到一則加密訊息：d3j3kj348fkr9rj3o2j2ke3j4ldn32\n\n請選擇鑰匙：",
                actions=[
                    MessageAction(label="公鑰", text="iLoveYou"),
                    MessageAction(label="私鑰", text="HandsomeXiaoMing")
                ]
            )
            template_message = TemplateSendMessage(alt_text="解密選擇題", template=confirm_template)
            line_bot_api.reply_message(event.reply_token, template_message)
            user_state[user_id]["workflow"] += 1

        elif user_state[user_id]["workflow"] == 1:
            if message == "iLoveYou":
                line_bot_api.reply_message(event.reply_token, TextSendMessage("恭喜你成功解密🎉，您的訊息為：\n\n我想認識你\n\n如要繼續進行請輸入「了解」，若想中斷學習可以點選下方圖文選單"))
                user_state[user_id]["workflow"] = 0
                user_state[user_id]["state"] = "Normal"
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("您選錯了！😡，解密鑰匙如果是用公鑰解大家不就看光了嗎？\n\n了解之後請輸入「ok」，重新回答！"))
                    


    #未在任何workflow中
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage('抱歉我不太懂你的意思喔～'))
            
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token,message)
    
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