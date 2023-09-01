
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['xuH0c5mdb8a8K0iIrLm0EAjULDMQk9TFCzuYTy8INhX9BQcUBaIZPJ8KLOhYy74tGktVWAAGWE7cQT2O5CvUwCd/i9hwxtAWfNh5iR+pmdu3tYwTo5Q5AmiARLNp1S8IJ86dfnPZj0e/MHOoOLJ+hAdB04t89/1O/w1cDnyilFU='])
handler = WebhookHandler(os.environ['12e7e0f19d5d084c1423c5c165b30ea1'])

def verify_signature(request):
    # 在這裡實作驗證簽名的邏輯，我們假設這個函式可以確認簽名是否有效
    return True

def process_line_bot_message(message):
    # 在這裡實作處理 Line Bot 訊息的邏輯
    pass

@app.route('/webhook', methods=['POST'])
def webhook():
    # 驗證請求
    if not verify_signature(request):
        abort(400)  # 驗證失敗，返回狀態碼 400

    # 處理 Line Bot 訊息
    process_line_bot_message(request.json)
    
    return '', 200  # 返回狀態碼 200

if __name__ == '__main__':
    app.run()



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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

SAVE_PATH = '"D:\aaaaaa\test2\picture"'

@app.route("/callback", methods=['POST'])
def callback():
    # 取得X-Line-Signature標頭的值
    signature = request.headers['X-Line-Signature']
    
    # 取得請求的內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        # 請求的內容驗證
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 取得LineBot傳送的照片ID
    message_id = event.message.id

    # 取得照片內容
    message_content = line_bot_api.get_message_content(message_id)

    # 儲存照片到特定地方
    save_path = os.path.join(SAVE_PATH, f"{message_id}.jpg")
    with open(save_path, 'wb') as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    # 回覆使用者上傳成功訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="照片儲存成功！")
    )

if __name__ == "__main__":
    app.run()

