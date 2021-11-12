from flask import Flask, render_template, request, jsonify, Response
import io
import csv
import os
import flask
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly.express as px
import pandas as pd
import numpy as np
import datetime
import operator
from flask.helpers import url_for
from werkzeug.utils import secure_filename
# import openpyxl
import utility


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
    # app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
    # file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.xlsx')
# def saveFile(uploaded_file, filetype):
    
#     file_path = f'static/temp.{filetype}'
#     uploaded_file.save(file_path)

# def duration(start_value, end_value):

#     Start = datetime.datetime.fromisoformat(start_value)
#     End = datetime.datetime.fromisoformat(end_value)

#     start_value = Start            
#     end_value = End

#     duration = End - Start
#     seconds = int(duration. total_seconds())

#     return seconds, Start, End

# def generateDictArray(csvFile):
#     data = []

#     global df
    
#     with open(f'static/{csvFile}.csv', 'r') as file:
#             csv_file = csv.DictReader(file)
#             for row in csv_file:
#                 # print(row)
#                 para = utility.duration(row['START'], row['END'])
                
#                 row['DURATION'] = para[0] 
#                 row['START'] = para[1] 
#                 row['END'] = para[2]
#                 data.append(row)

#                 # duration = row['start_time'] - row['end_time']
#                 # data.append(row)
                
#     df = pd.read_csv(f'static/{csvFile}.csv')
#     return data


# @app.route('/duration.png')
# def plot_duration():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     duration=[]
#     for i in range(len(df)): 
#         if  type(df['START'][i]) == 'str':
#             start=datetime.datetime.strptime(df['START'][i],'%Y-%m-%d %H:%M:%S')
#             end=datetime.datetime.strptime(df['END'][i],'%Y-%m-%d %H:%M:%S')

#         else:
#             start = df['START'][i]
#             end = df['END'][i]
#         duration.append((end-start).total_seconds())
#         callee_duration={}
#     for i in range(df.shape[0]):
#         if(str(df['PHONE'][i]) in callee_duration):
#             callee_duration[str(df['PHONE'][i])]+=duration[i]
#         else:
#             callee_duration[str(df['PHONE'][i])]=duration[i]
#     # print(callee_duration)
    
#     callee_duration= dict( sorted(callee_duration.items(), key=operator.itemgetter(1),reverse=True))

#     axis.bar(callee_duration.keys(),callee_duration.values())
#     #axis.set_xticks(callee_duration.keys())
    
#     axis.set_xticklabels(callee_duration.keys(),rotation=40)    
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/frequency.png')
# def plot_frequency():
    
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     numbers=df['PHONE'].astype('str').value_counts().head(10).index
#     freq=df['PHONE'].value_counts().head(10)
#     axis.bar(numbers,freq)
#     axis.set_xticks(numbers)
#     axis.set_xticklabels(numbers,rotation=40)
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/type.png')
# def plot_type():
 
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     axis.bar(df['TYPE'].value_counts().index,df['TYPE'].value_counts())
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/imei.png')
# def plot_imei():
    
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     imei=[]
#     for i in df['IMEI1']:
#         imei.append(i)
#     uniq,count=np.unique(imei,return_counts=True)
#     unique=[]
#     for i in uniq:
#         unique.append(str(i))
#     axis.bar(unique,count)
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')


@app.route('/',methods=["POST", "GET"])
def home():
    
    if request.method == "POST":
        formData = request.form
        recType = formData['type']
        minDuration = formData['min']
        maxDuration = formData['max']
        recNumber = formData['number']
        recIMEI = formData['IMEI']
        recIMSI = formData['IMSI']
        fromTime = formData['fromTime']
        toTime = formData['toTime']
        fromDate = formData['fromDate']
        toDate = formData['toDate']
        f = request.files['file']

        # print(recType, minDuration, maxDuration, recType, fromDate, toDate,fromTime, toTime)
        
        utility.saveFile(f, 'temp.xlsx')
        df = pd.read_excel('static/temp.xlsx')
        df = utility.readfiles(df)
        utility.convert(df)
        LIST = df.to_dict('records')
        # print(recType, minDuration, maxDuration, recType, fromDate, toDate,fromTime, toTime)

        if fromDate!='':
            fromDate = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
        if toDate!='':
            fromDate = datetime.datetime.strptime(toDate, '%Y-%m-%d')
        

        # print('starts here/\n\n')
        # print('')
        # print(toTime)
        
        # print(fromTime)
        # print('')
        # print('starts here/\\n')

        if fromTime!='':
            fromTime = datetime.datetime.strptime(fromTime, '%H:%M')
        if toTime!='':
            toTime = datetime.datetime.strptime(toTime, '%H:%M')

        filteredData = utility.filterdata(df=df,  phone = recNumber, imei = recIMEI, imsi = recIMSI)
        filteredData = utility.filterdatetime(df = filteredData,  starttime=fromTime, endtime = toTime, mindur = minDuration, maxdur =  maxDuration)


        return render_template('index.html', filteredData = LIST )
    else:
        return render_template('index.html', filteredData = [[]])

    #     print(f)
    #     name = f.filename
    #     print(name)


@app.route('/analyse-multiple', methods=["POST", "GET"])
def uploadMultiple():
    if request.method == "POST":
        filenames = []
        formData = request.form
        IMEI = formData['IMEI']
        number = formData['number']
        uploaded_files = flask.request.files.getlist("file")
        
        for upload in uploaded_files:
            filename = upload.filename.rsplit("/")[0]
            filenames.append(filename)
            destination = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            upload.save(destination)

      

        
        filenames_with_IMEI = utility.findfiles('IMEI', IMEI, filenames)
        filenames_with_number = utility.findfiles('CALLING PARTY', number, filenames)

        if len(filenames_with_IMEI)==0:
            filenames_with_IMEI = filenames_with_IMEI.append('No Files')
        
        
        numbers_common_in_all = utility.common_phone(filenames)
        
        
        IMEIs_common_in_all = utility.common('IMEI', filenames)

        if len(IMEIs_common_in_all)==0:
            IMEIs_common_in_all.add('No Common IMEIs')

        if len(numbers_common_in_all)==0:
            numbers_common_in_all.add('No Common IMEIs')

        if len(filenames_with_number)==0:
            filenames_with_number.append('No Common Phone Numbers')

        # field = 'IMEI'
        # utility.common()
        
        
        return render_template("analyseMultiple.html", display = 'Block', IMEIs_common_in_all=IMEIs_common_in_all, numbers_common_in_all=numbers_common_in_all, filenames_with_IMEI=filenames_with_IMEI, filenames_with_number=filenames_with_number)
    else:
        return render_template("analyseMultiple.html", display = 'none')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/how-to-use')
def howToUse():
    return render_template("howToUse.html")

@app.route('/project-details')
def projectDetails():
    return render_template("projectDetails.html")





# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
#     return send_from_directory(directory=uploads, filename=filename)


if __name__ == "__main__":
    app.run(debug=True)