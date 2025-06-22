from flask import Flask, request, redirect, url_for, send_from_directory, jsonify, render_template_string
import os

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML template for GUI with progress bar
HTML_TEMPLATE = """
<!doctype html>
<html>
    <head>
        <title>File Upload Server</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
            }
            header {
                background-color: #6200ea;
                color: white;
                padding: 1rem 0;
                text-align: center;
            }
            main {
                padding: 2rem;
                max-width: 800px;
                margin: auto;
            }
            h1, h2 {
                color: #6200ea;
            }
            form {
                margin-bottom: 2rem;
                background: #fff;
                padding: 1rem;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            input[type="file"] {
                margin-bottom: 1rem;
            }
            button {
                background-color: #6200ea;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 3px;
                cursor: pointer;
            }
            button:hover {
                background-color: #3700b3;
            }
            .progress {
                width: 100%;
                background-color: #ddd;
                border-radius: 5px;
                overflow: hidden;
                margin-top: 1rem;
            }
            .progress-bar {
                height: 20px;
                width: 0;
                background-color: #6200ea;
                text-align: center;
                color: white;
                line-height: 20px;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                background: #fff;
                margin: 0.5rem 0;
                padding: 0.5rem;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            a {
                text-decoration: none;
                color: #6200ea;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>File Upload Server</h1>
        </header>
        <main>
            <h1>Upload a File</h1>
            <form id="upload-form" action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" id="file-input">
                <button type="submit">Upload</button>
                <button type="button" id="cancel-button">Cancel</button>
                <div class="progress">
                    <div class="progress-bar" id="progress-bar">0%</div>
                </div>
            </form>
            <h2>Uploaded Files</h2>
            <ul>
                {% for file in files %}
                    <li><a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a></li>
                {% endfor %}
            </ul>
        </main>
        <script>
            const form = document.getElementById('upload-form');
            const progressBar = document.getElementById('progress-bar');
            const cancelButton = document.getElementById('cancel-button');
            let xhr;

            form.addEventListener('submit', function(e) {
                e.preventDefault();

                const fileInput = document.getElementById('file-input');
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);

                xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload', true);

                xhr.upload.onprogress = function(event) {
                    if (event.lengthComputable) {
                        const percentComplete = Math.round((event.loaded / event.total) * 100);
                        progressBar.style.width = percentComplete + '%';
                        progressBar.textContent = percentComplete + '%';
                    }
                };

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        window.location.reload();
                    } else {
                        alert('File upload failed!');
                    }
                };

                xhr.send(formData);
            });

            cancelButton.addEventListener('click', function() {
                if (xhr) {
                    xhr.abort();
                    progressBar.style.width = '0%';
                    progressBar.textContent = 'Upload Cancelled';
                }
            });
        </script>
    </body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return '', 200

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

