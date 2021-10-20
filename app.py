from flask import Flask, render_template, request, jsonify
import io
import csv
import os
import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
import numpy as np
import datetime
# from datetime import datetime
from flask.helpers import url_for
import openpyxl

app = Flask(__name__)

# def saveFile(uploaded_file):
#     UPLOAD_FOLDER = 'static'
#     app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#     uploaded_file.save(file_path)

def duration(start_value, end_value):

    Start = datetime.datetime.fromisoformat(start_value)
    End = datetime.datetime.fromisoformat(end_value)

    start_value = Start            
    end_value = End

    duration = End - Start
    seconds = int(duration. total_seconds())

    return seconds, Start, End

def generateDictArray(csvFile):
    data = []
    with open(f'static/{csvFile}.csv', 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                
                para = duration(row['Start'], row['End'])
                
                row['Duration'] = para[0] 
                row['Start'] = para[1] 
                row['End'] = para[2]
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
        # print(recordDate, type(recordDate))
    else:
        recordDate = datetime.datetime.strptime(recordDate, '%Y-%m-%d').date()
        # print(recordDate, type(recordDate))
    

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

    # print(filteredData, len(filteredData))

    if len(filteredData)==0:
        return 'No Records Found'
    else:
        return filteredData

        
            
@app.route('/',methods=["POST", "GET"])
def home():
    if request.method == "POST":
        
        data=[]
        formData= request.form
        # print(formData)
        # print(type(request.files['file']))

        csvFile = request.form['selected']
        min = request.form['min']
        max = request.form['max']
        recordDate = request.form['date']
        mobileNo = request.form['number']
        f = request.files['file']
        name = f.filename
        print(min, max, recordDate, mobileNo, type(min), type(max), type(recordDate), type(mobileNo))
        # print(type(f))

        # print(min, max, recordDate, type(recordDate), mobileNo, type(mobileNo))

        if name == '':
            data = generateDictArray(csvFile)
            
            # print(data)

                # uploaded_file = request.files['file']
                # saveFile(uploaded_file)
                # csvFile = request.form['file']
                # print(csv_input)
                # for row in csv_input:
                #     print(row)
            # else:
            #     print(jsonify({"result": request.get_array(field_name='file')}))

        elif 'csv' in name:
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_file = csv.DictReader(stream)
            for row in csv_file:
                
                para = duration(row['Start'], row['End'])
                row['Duration'] = para[0]
                row['Start'] = para[1] 
                row['End'] = para[2]

                data.append(row)

        elif 'xlsx' in name:
            data_xls = pd.read_excel(f)
            file = data_xls.to_csv ('static/target.csv', index = None, header=True)
            csvFile = 'target'
            data = generateDictArray(csvFile)

        if min == '' and max == '' and recordDate == '' and mobileNo == '':
            filteredData = data
        else:
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
