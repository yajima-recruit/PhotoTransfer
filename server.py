from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import socket
import qrcode
import os

contextRoot = os.path.basename(os.getcwd())

app = Flask(__name__)
SAVE_FOLDER_PATH = f"D:\webServer\{contextRoot}\save"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(SAVE_FOLDER_PATH, filename))
        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(SAVE_FOLDER_PATH, filename)

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    url = f'http://{ip}:8000/'

    # QRコードを生成する
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 画像を生成する
    img = qr.make_image(fill_color="black", back_color="white")

    # 画像を表示する
    img.show()

    app.run(debug=True, host='0.0.0.0', port=8000)
