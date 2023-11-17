import qrcode
from MyBaleCloud.balecloud import BaleCloud
import os 

token = ""

global qr
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

app = BaleCloud(
    token
)

msgLis = []

while 1:
    for msg in app.getUpdates():
        
        text = str(msg.text)
        chat = msg.chat_id
        msg_id = msg.message_id
        
        if not msg_id in msgLis:
            msgLis.append(msg_id)
            print(text)
            
            if text == "/start":
                app.sendMessage('/qr #<data>\n\n/qr hello world', chat, msg_id)
                
            elif text.startswith('/qr'):
                data = text.replace('/qr ', '')
                app.sendMessage('wait', chat, msg_id)
                
                try:
                    qr.add_data(data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color='black', back_color='white')
                    img.save(f'{data}.png')
                    app.sendLocalPhoto(f"{data}.png", chat, data, msg_id)
                    os.system(f'del "{data}.png"')
                    
                except Exception as E:
                    app.sendMessage('Faild', chat, msg_id)
                    print(E)
                    
            
        else:
            msgLis.append(msg_id)


