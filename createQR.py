import qrcode
import os
import uuid

otuputDir = 'qr_codes'
if not os.path.exists(otuputDir):
    os.makedirs(otuputDir)

values = [200, 100, 50, 20, 10]


def generateQR():
    for value in values:
        qr_id = str(uuid.uuid4())
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
        )
        
        qr.add_data(f'http://192.168.50.197:5000/add_balance?qr_value={value}&id={qr_id}')
        img = qr.make_image(fill_color="black", back_color="white")
        
        img.save(os.path.join(otuputDir, f'qr_{value}_{qr_id}.png'))
        
    print("QR kodlar başarıyla oluşturuldu ve kaydedildi.")

if __name__ == '__main__':
    generateQR()