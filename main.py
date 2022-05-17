
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os



#Buddha-Bot
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

sbert = SentenceTransformer('Buddha-Bot/sbert_stair')
print("sbert OK!")

def similarity(id1, id2):
    return cosine_similarity([vectors[id2idx[id1]]], [vectors[id2idx[id2]]])[0][0]

with open('Buddha-Bot/Butta_dict.binaryfile', 'rb') as bf:
    Butta_dict = pickle.load(bf)
    
with open('Buddha-Bot/Yahoo_dict.binaryfile', 'rb') as yf:
    Yahoo_dict = pickle.load(yf)


def Origin(input_Q):
    return input_Q+"momomo"

#質問を入力すると回答が表示されます
def Buddha(input_Q):
    Buddha_cos = {}
    for key in Butta_dict:
        Buddha_cos[key] = cosine_similarity([Butta_dict[key]],[sbert.encode(input_Q)])
        
    max_k = max(Buddha_cos, key=Buddha_cos.get)
    return max_k


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=Origin(event.message.text)))





if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
