import requests
import os

def lineNotifyMessage(msg, img_path=None):
    headers = {
        "Authorization": "Bearer " + os.getenv('LINE_AUTHORIZATION'),
        # "Content-Type" : "application/x-www-form-urlencoded"
        }
    data={"message":msg,}
    files={"imageFile":open(img_path, "rb"),} if img_path != None else None
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, data=data, files=files)
    print(r.text)

# lineNotifyMessage('Python2Line : 啟動')