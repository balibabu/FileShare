from flask import Flask,render_template,send_file,request,jsonify
import os
import socket
import qrcode

app = Flask(__name__)
PORT = 8000
DIRECTORY=''


if os.path.exists('path.txt'):
    file=open('path.txt')
    DIRECTORY=file.read()
else:
    upath=input('enter a path or help: ')
    if upath=='help':
        input('1. Give empty value for desktop location \n2. Create a path.txt file and paste a valid path in it\npress enter to exit')
        exit()
    elif upath=='':
        DIRECTORY = os.path.join(os.path.expanduser("~"), "Desktop")
    else:
        DIRECTORY=upath
        
ipv4_address = socket.gethostbyname(socket.gethostname())
url = f'http://{ipv4_address}:{PORT}'


@app.route("/")
def get_files():
    files =[f for f in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, f))]
    return render_template('index.html', files=files)

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(DIRECTORY, filename)
    return send_file(file_path, as_attachment=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    file.save(os.path.join(DIRECTORY, file.filename))
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

def show_qr_terminal(value):
    qr = qrcode.QRCode(1,qrcode.constants.ERROR_CORRECT_L,  10,  4)
    qr.add_data(value)
    qr.make(fit=True)
    qr_matrix = qr.get_matrix()
    for row in qr_matrix:
        for col in row:
            print('\u2588'*2,end='') if col else print('  ',end='')
        print()

if __name__ == '__main__':
    show_qr_terminal(url)
    app.run(host='0.0.0.0', port=PORT)