from flask import Flask, render_template, request
import csv
import os
from os.path import join, dirname, realpath
import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
import numpy as np
import datetime
# from datetime import datetime
from flask.helpers import url_for

app = Flask(__name__)

# def saveFile(uploaded_file):
#     UPLOAD_FOLDER = 'static'
#     app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#     uploaded_file.save(file_path)

def generateDictArray(csvFile):
    data = []
    with open(f'static/{csvFile}.csv', 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:

                Start = datetime.datetime.fromisoformat(row['Start'])
                End = datetime.datetime.fromisoformat(row['End'])

                row['Start'] = Start            
                row['End'] = End

                duration = End - Start
                seconds = int(duration. total_seconds())
                row['Duration'] = seconds 

                data.append(row)

                # duration = row['start_time'] - row['end_time']
                # data.append(row)
    return data

def filterData(data, min='', max='', recordDate='', mobileNo=''):

    filteredData = []

    if min=='':
        min = 0
    else:
        min = int(min)

    if max=='':
        max=100000  #change with INT MAX
    else:
        max = int(max)

    if recordDate == '':
        recordDate=datetime.date.today()
        print(recordDate, type(recordDate))
    else:
        recordDate = datetime.datetime.strptime(recordDate, '%Y-%m-%d').date()
        print(recordDate, type(recordDate))
    

    for dict in data:
        # , dict['Start'].date() == recordDate, dict['PHONE'] == mobileNo 
        # print(dict['Duration']>min, dict['Duration']<=max)

        # and dict['Start'].date() == recordDate and dict['PHONE'] == mobileNo
        #not working if no date is selected
        if dict['Duration']>=min and dict['Duration']<=max and dict['Start'].date() < recordDate:
            if mobileNo == '': 
                filteredData.append(dict)
            elif dict['PHONE'] == mobileNo: 
                filteredData.append(dict)

    print(filteredData, len(filteredData))

    if len(filteredData)==0:
        return 'No Records Found'
    else:
        return filteredData

        
            
@app.route('/',methods=["POST", "GET"])
def home():
    if request.method == "POST":

        formData= request.form
        print(formData)
        print(request.files['file'])

        csvFile = request.form['selected']
        min = request.form['min']
        max = request.form['max']
        recordDate = request.form['date']
        mobileNo = request.form['number']

        print(min, max, recordDate, type(recordDate), mobileNo, type(mobileNo))

        # if csvFile == 'uploaded':
        #     uploaded_file = request.files['file']
        #     saveFile(uploaded_file)
        #     csvFile = request.form['file']

        data = generateDictArray(csvFile)

        filteredData = filterData(data, min, max, recordDate, mobileNo)

        display = 'display: block'
       

        # stream = io.TextIOWrapper(f.stream._file, "UTF8", newline=None)
        # csv_input = csv.reader(stream)
        
        # data = sample,
        return render_template("index.html",  display = display, filteredData=filteredData )
    else:
        display = 'display: none'
        return render_template("index.html", display = display)

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

    sample1 = generateDictArray('Sample1')
    sample2 = generateDictArray('Sample2')
    sample3 = generateDictArray('Sample3')
    return render_template("sample.html",Sample1 = sample1, Sample2 = sample2, Sample3 = sample3 )

# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
#     return send_from_directory(directory=uploads, filename=filename)


if __name__ == "__main__":
    app.run(debug=True)
