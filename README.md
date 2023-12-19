# LineBot_New

::: spoiler langchain工具-flowise
## langchain
## Flowise

參考連結
https://youtu.be/Q7_dKkosJY4

## 安裝步驟
1. 進入官網，開啟flowise Github
![](https://hackmd.io/_uploads/r1Hep4JQa.jpg)

3. 依照自己版本下載Nodejs
![](https://hackmd.io/_uploads/BJM38T0f6.png)

2. 下載flowise
```bash
npm install -g flowise
```
3. 啟動他
```bash
npx flowise start
```
4. 開網頁輸入下方網址就開啟了
http://localhost:3000
![](https://hackmd.io/_uploads/H18I_6RMT.png)


5. 關掉terminal就結束flowise了

:::spoiler 報錯的解決方法
* ios用超級使用者
>如果出現這個畫面，使用以下command
```bash
sudo npm install -g flowise
```
```bash
sudo npx flowise start
```
![截圖 2023-11-14 上午9.50.07](https://hackmd.io/_uploads/SJ3AfIe4a.png)
### 範例1
![截圖 2023-11-14 上午9.56.41](https://hackmd.io/_uploads/rJEm4IgNp.jpg)


:::
[TOC]
## Line_Bot用Render就串接Python
### 1. 註冊帳號
1. Render
2. Line Developer
3. GitHub

### 2. 執行以下步驟
#### 1. 創立一個資料夾準備兩個個檔案
* app.py
```python=
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
handler = WebhookHandler('Your Channel Sercret')

#主動推播
line_bot_api.push_message('Your User ID', TextSendMessage(text='你可以開始了'))

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
```  
* requirements.txt
>以下是內文
```
line-bot-sdk 
bs4 
flask 
pymongo 
datetime 
pandas 
SnowNLP 
emoji 
pyshorteners 
scipy
```
#### 2. 上傳GitHub，網路上是建議開README比較知道在幹嘛
> 建議可以使用git bash，可以參考這個連結
> [git bash](/S4vieed-QaKWdtXTOh-xgw)

![截圖 2023-11-23 上午12.48.08](https://hackmd.io/_uploads/SJSoN3iE6.png)

#### 3. 部署Render
:::info
1. 創建一個project，選擇**Web Service**
2. 填寫以下資料
![截圖 2023-11-23 上午12.51.21](https://hackmd.io/_uploads/SyF3Nhj4T.png)
![截圖 2023-11-23 上午12.51.44](https://hackmd.io/_uploads/BJxaNnjE6.png)
![截圖 2023-11-23 上午12.54.01](https://hackmd.io/_uploads/HyQeBno4p.png)
![截圖 2023-11-23 上午12.55.46](https://hackmd.io/_uploads/HkAbS3sNa.png)
![截圖 2023-11-23 上午12.59.12](https://hackmd.io/_uploads/SkF7r3oN6.png)
![截圖 2023-11-23 上午1.00.43](https://hackmd.io/_uploads/HkV4rniNp.png)

### 這樣就成功了喔～
:::
#### 4. 布署完後，記得將這串網址複製
![截圖 2023-11-23 上午1.01.18](https://hackmd.io/_uploads/H1DcBnoVT.png)
#### 5. 到Line Developer的Webhook URL 按下 Edit 把他貼上
:::danger
** 記得傳上去後要記得在網址後面加上/callback
:::
![截圖 2023-11-23 上午1.10.27](https://hackmd.io/_uploads/r1V882sEa.png)
#### 6. 做一些設定，如下圖
![截圖 2023-11-23 上午1.13.52](https://hackmd.io/_uploads/r1c-D3oNp.png)

## [line Chat Bot 程式碼撰寫](https://hackmd.io/@72QCJMP8QyuBuaQZ0u5pbA/ryo0UAEHT)
:::spoiler 參考資料
1. [行銷搬進大程式](https://marketingliveincode.com/classification/lineBot/43)
2. [在 Render 搭建 Line Bot
](https://rnnnnn.medium.com/%E5%9C%A8-render-%E6%90%AD%E5%BB%BA-line-bot-92b35bedb24e)
:::

