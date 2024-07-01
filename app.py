from flask import Flask, request, jsonify, send_file
from bs4 import BeautifulSoup
import os
from datasets import predict_html_template
from flask_cors import CORS
from template_extraction import process_html_file


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Welcome to the API!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        html_content = file.read()
        template = predict_html_template(html_content)
        
        return jsonify({"header": template})
    

@app.route('/download', methods=['POST'])
def download_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        html_content = file.read()
        file_path = process_html_file(html_content)
        # try:
        #     with open(file_path, 'rb') as f:
        #         file_data = f.read()
        #     return file_data, 200, {
        #     'Content-Disposition': f'attachment; filename={file_path}'
        # }
        return send_file(file_path, as_attachment=True)
        # except FileNotFoundError:
        #     return "File not found", 404
        
if __name__ == '__main__':
    app.run(debug=True)
