from flask import Flask, render_template, request
import csv
import os
from os.path import join, dirname, realpath

app = Flask(__name__)

def saveFile(uploaded_file):
    UPLOAD_FOLDER = 'static/files'
    app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(file_path)

def csv_reader(csvFile):
    with open(f'/static/files{csvFile}.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

            
@app.route('/',methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        sample = request.form['sample']
        uploaded_file = request.files['file']
        saveFile(uploaded_file)

        # stream = io.TextIOWrapper(f.stream._file, "UTF8", newline=None)
        # csv_input = csv.reader(stream)
        
        return render_template("index.html", data = sample )
    else:
        return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/how-to-use')
def howToUse():
    return render_template("howToUse.html")

@app.route('/project-details')
def projectDetails():
    return render_template("projectDetails.html")

@app.route('/samples')
def samples():
    return render_template("sample.html")

# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
#     return send_from_directory(directory=uploads, filename=filename)


if __name__ == "__main__":
    app.run(debug=True)
