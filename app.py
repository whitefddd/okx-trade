import requests
import json
import hmac
import hashlib
import base64
from datetime import datetime, timezone

# 设置你的API密钥和秘密
api_key = '4db9b5de-741d-4522-ba25-d4b63a142f8b'
secret_key = '756E535F7E9E1A97B45CE739F974F9AE'
passphrase = 'Aa123456.'

# 生成OKX API签名
def generate_signature(timestamp, method, request_path, body, secret_key):
    message = f'{timestamp}{method}{request_path}{body}'
    hmac_key = base64.b64decode(secret_key)
    signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

# 获取当前UTC时间戳，格式为：2024-06-04T16:38:56Z
def get_iso_timestamp():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# 下单函数
def place_order():
    url = 'https://www.okx.com'
    endpoint = '/api/v5/trade/order-algo'
    request_path = endpoint

    body = {
        "instId": "ETH-USDT-SWAP",
        "side": "sell",
        "tdMode": "cross",
        "posSide": "net",
        "sz": "1",
        "ordType": "trigger",
        "triggerPx": "4100",
        "triggerPxType": "last",
        "orderPx": "-1",
        "attachAlgoOrds": [{
            "attachAlgoClOrdId": "",
            "slTriggerPx": "4300",
            "slOrdPx": "4300",
            "tpTriggerPx": "3800",
            "tpOrdPx": "3800"
        }]
    }

    # 获取当前UTC时间戳
    timestamp = get_iso_timestamp()
    print("Timestamp for request:", timestamp)

    # 生成签名
    signature = generate_signature(timestamp, 'POST', request_path, json.dumps(body), secret_key)
    print("Signature:", signature)

    headers = {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json',
    }

    print("Headers:", headers)

    # 发送请求
    response = requests.post(url + endpoint, headers=headers, data=json.dumps(body))
    print("Request body:", json.dumps(body, indent=4))
    return response.json()

# 测试下单
if __name__ == '__main__':
    response = place_order()
    print("Response:", response)
