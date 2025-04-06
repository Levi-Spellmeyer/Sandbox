from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pyotp
import qrcode

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Secret Key for TOTP
key = "GeeksforGeeksIsBestForEverything"

# Route to serve the QR code
@app.route('/qr-image', methods=['GET'])
def serve_qr():
    uri = pyotp.TOTP(key).provisioning_uri(
        name='User',
        issuer_name='YourApp'
    )
    qr = qrcode.make(uri)
    qr.save("qr.png")
    return send_file("qr.png", mimetype='image/png')

# Route to verify the 2FA code
@app.route('/verify', methods=['POST'])
def verify_code():
    data = request.json
    code = data.get('code')
    totp = pyotp.TOTP(key)
    if totp.verify(code):
        return jsonify({"success": True, "message": "Code verified!"})
    else:
        return jsonify({"success": False, "message": "Invalid code!"})

if __name__ == '__main__':
    app.run(debug=True)
