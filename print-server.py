from flask import Flask, request
from escpos.printer import Usb

app = Flask(__name__)

# Usa tu VID y PID
printer = Usb(idVendor=0x0FE6, idProduct=0x811E)
@app.route('/print', methods=['POST'])
def print_text():
    content = request.form.get("text", "")
    if content:
        printer.text(content + "\n")
        printer.cut()
        return "Impresión enviada", 200
    return "Texto vacío", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)