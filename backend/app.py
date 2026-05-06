from flask import Flask, request, jsonify
from analyzer import analyze_image
from verilog_generator import generate_verilog
from diagram_generator import generate_diagram
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return '', 204

    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    image_bytes = file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    circuit_json = analyze_image(image_base64)
    verilog_code = generate_verilog(circuit_json)
    diagram_svg = generate_diagram(circuit_json)

    return jsonify({
        "json": circuit_json,
        "verilog": verilog_code,
        "diagram": diagram_svg
    })

if __name__ == "__main__":
    app.run(debug=True)