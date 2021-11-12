import datetime
import pandas as pd
from datetime import datetime
import numpy as np

def readfiles(df):
    i=0
    while(i<100):
        if(type(df.iloc[i,0])==str)and (type(df.iloc[i,1])==str) :
            if(('Call' not in df.iloc[i,0]) or ('Call' not in df.iloc[i,1])):
                i=i+1
            else:
                break
        else:
            i=i+1
    df.columns=df.iloc[i]
    df.drop(index=i,inplace=True)
    df.dropna(inplace=True)
    return df


def common(field,array):
    #field='IMEI1'
    #array=['sample1.csv','sample2.csv','sample3.csv']
    df=pd.read_excel(f"static/uploads/{array[0]}")
    common=set(df[field])
    for i in array[1:]:
        df=pd.read_excel(f"static/uploads/{i}")
        common=set(common&set(df[field]))
    return common

def filterdatetime(df,starttime='',endtime='',startdate='',enddate='',mindur=0,maxdur=50000):
    try:
        cpdf=df
        df.index=np.arange(0,df.shape[0])
        ti=[]
        dt=[]
        dur=[]
        for i in range(df.shape[0]):
            timespace=df['TIME'][i].replace("'","")
            ti.append(datetime.strptime(timespace,"%H:%M:%S"))
            datespace=df['DATE'][i].replace("'","")
            if(len(df['DATE'][i].replace("'",""))==9):
                dt.append(datetime.strptime(datespace,"%d-%b-%y"))
            else:
                dt.append(datetime.strptime(datespace,"%d-%m-%Y"))
            if(type(df['DURATION']==str)):
                dur.append(int(df['DURATION'][i].replace("'","")))
            else :
                dur.append(df['DURATION'][i])
        df['TIME']=ti
        df['DURATION']=dur
        df['DATE']=dt
        if(startdate!=''):
            df=df[df['DATE']>startdate]
        if(enddate!=''):
            df=df[df['DATE']<enddate]
        if(starttime!=''):
            df=df[df['TIME']>starttime]
        if(endtime!=''):
            df=df[df['TIME']<endtime]
        df=df[df['DURATION']>mindur]
        df=df[df['DURATION']<maxdur]
        return df
    except:
        return cpdf

def convert(df):
    l=list(df.columns)
    for i in range(len(l)):
        l[i] = l[i].upper()
        if 'CALLING' in l[i]:
            l[i] = 'CALLING PARTY'
        elif 'CALLED' in l[i]:
            l[i] = 'CALLED PARTY'
        elif 'DATE' in l[i]:
            l[i] = 'DATE'
        elif 'TIME' in l[i]:
            l[i] = 'TIME'
        elif 'DUR' in l[i]:
            l[i] = 'DURATION'
        elif ('FIRST CELL' in l[i] or 'CELL1' in l[i]):
            l[i] = 'CELL1'
        elif ('LAST CELL' in l[i] or 'CELL2' in l[i]):
            l[i] = 'CELL2'
        elif  'CALL TYPE' in l[i]:
            l[i] = 'CALL TYPE'
        elif 'IMEI' in l[i]:
            l[i] = 'IMEI'
        elif 'IMSI' in l[i]:
            l[i] = 'IMSI'
        elif 'ROAM' in l[i]:
            l[i] = 'ROAM'
    df.columns=l
        

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

def findfiles(field,values,files):
    ans=[]
    for file in files:
        df=pd.read_excel(f"static/uploads/{file}")
        df=readfiles(df)
        convert(df)
        if(ispresent(df,field,values)):
            ans.extend(file)
        return ans

def ispresent(df,field,value):
    for i in df[field]:
        if(i==value):
            return True
    return False


def common_phone(array):
    df=pd.read_excel(f"static/uploads/{array[0]}")
    df=readfiles(df)
    convert(df)
    common=set(df['CALLING PARTY'])or(df['CALLED PARTY'])
    for i in array[1:]:
        df=pd.read_excel(f"static/uploads/{i}")
        df=readfiles(df)
        convert(df)
        setc=set(df['CALLING PARTY'])or(df['CALLED PARTY'])
        common=set(common&setc)
    return common

def common(field,array):
    df=pd.read_excel(f"static/uploads/{array[0]}")
    df=readfiles(df)
    convert(df)
    common=set(df[field])
    for i in array[1:]:
        df=pd.read_excel(f"static/uploads/{i}")
        df=readfiles(df)
        convert(df)
        common=set(common&set(df[field]))
    return common

def filterdata(df,date='',typecall='',imei='',imsi='',phone=''):
    print(imei)
    if(imei!=''):
        df=df[df['IMEI']==imei]
    if(imsi!=''):
        df=df[df['IMSI']==imsi]
    if(typecall!=''):
        df=df[df['CALL TYPE']==typecall]
    if(phone!=''):
        df=df[df['PHONE']==phone]
    if(date!=''):
        df=df[df['DATE']==date]
    return df

# def filterData(data, min=0, max='', recordDate='', mobileNo='', Type=''):
