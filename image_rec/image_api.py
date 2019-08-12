from flask import Flask, request, jsonify
from google_vision_service import get_image_labels

app = Flask(__name__)

@app.route("/google_vision", methods=['POST'])
def classify_image():
    image_uri = request.json['image_uri']
    labels = get_image_labels(image_uri)
    print(labels)	
    return jsonify(labels=labels), 200

if __name__ == "__main__":
    app.debug = True;
    app.run(port=5050)
