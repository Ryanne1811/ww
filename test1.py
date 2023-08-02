from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, ImageMessage
import os

app = Flask(__name__)

# 設定你的LineBot的Channel Access Token和Channel Secret
line_bot_api = LineBotApi('xuH0c5mdb8a8K0iIrLm0EAjULDMQk9TFCzuYTy8INhX9BQcUBaIZPJ8KLOhYy74tGktVWAAGWE7cQT2O5CvUwCd/i9hwxtAWfNh5iR+pmdu3tYwTo5Q5AmiARLNp1S8IJ86dfnPZj0e/MHOoOLJ+hAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('12e7e0f19d5d084c1423c5c165b30ea1')

# 設定你要儲存照片的特定地方路徑
SAVE_PATH = '"C:\aaaaaa\test2\picture"'

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
