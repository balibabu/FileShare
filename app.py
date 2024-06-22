from flask import Flask,render_template,send_file,request,redirect,jsonify
import os,io
import socket
import qrcode
import qrcode.image.svg
import webbrowser

app = Flask(__name__)
DIRECTORY = "C:\\Users\\Lappy\\Desktop"
PORT = 8000
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

@app.route("/qrcode")
def show_QR_CODE():
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(url, image_factory=factory)
    output = io.BytesIO()
    img.save(output)
    svg_data = output.getvalue().decode()
    return svg_data

if __name__ == '__main__':
    webbrowser.open(url+'/qrcode')
    app.run(host='0.0.0.0', port=PORT)
