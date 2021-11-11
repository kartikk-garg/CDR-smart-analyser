import datetime

def saveFile(uploaded_file, filename):
    # UPLOAD_FOLDER = 'static'
    # app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
    # file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.xlsx')
    file_path = f'static/{filename}'
    uploaded_file.save(file_path)

def duration(start_value, end_value):

    Start = datetime.datetime.fromisoformat(start_value)
    End = datetime.datetime.fromisoformat(end_value)

    start_value = Start            
    end_value = End

    duration = End - Start
    seconds = int(duration. total_seconds())

    return seconds, Start, End

def filterData(data, min='', max='', recordDate='', mobileNo='', Type=''):
    
    filteredData = []

    if min=='':
        min = 0
    else:
        min = int(min)

    if max=='':
        max=1000000  #change with INT MAX
    else:
        max = int(max)

    if recordDate == '':
        recordDate=datetime.date.today()
        # print(recordDate, type(recordDate))
    else:
        recordDate = datetime.datetime.strptime(recordDate, '%Y-%m-%d').date()
        # print(recordDate, type(recordDate))
    
    if Type == 'ALL':
    
        for dict in data:
           
            if dict['DURATION']>=min and dict['DURATION']<=max and dict['START'].date() < recordDate :
                if mobileNo == '': 
                    filteredData.append(dict)
                elif dict['PHONE'] == mobileNo: 
                    filteredData.append(dict)
    else:
        for dict in data:
        
            if dict['DURATION']>=min and dict['DURATION']<=max and dict['START'].date() < recordDate and dict['TYPE'] == Type:
                if mobileNo == '': 
                    filteredData.append(dict)
                elif dict['PHONE'] == mobileNo: 
                    filteredData.append(dict)


    # print(filteredData, len(filteredData))

    if len(filteredData)==0:
        return 'No Records Found'
    else:
        return filteredData

def generateDictArray(csvFile):
    data = []

    global df
    
    with open(f'static/{csvFile}.csv', 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                # print(row)
                para = duration(row['START'], row['END'])
                
                row['DURATION'] = para[0] 
                row['START'] = para[1] 
                row['END'] = para[2]
                data.append(row)

                # duration = row['start_time'] - row['end_time']
                # data.append(row)
                
    df = pd.read_csv(f'static/{csvFile}.csv')
    return data