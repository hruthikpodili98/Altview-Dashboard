import json
import numpy as np
from flask import Flask, render_template,request,redirect, url_for
import pandas as pd
import requests


app = Flask(__name__)
SYMBOL = 'BA'
flag = 0
logged = 0
companies = []
symbols = []
    
def fetch_companies():
    resp = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=17ZNKSR4QPDOFBVJ')
    x1 = resp.json()['bestMatches']
    global companies
    global symbols

    for i in x1:
      companies = companies + [i['2. name']]
      symbols = symbols + [i['1. symbol']]
    
@app.route("/", methods=['GET', 'POST'])
def index():
    '''
    #df = pd.read_csv('data.csv')
    df = pd.read_csv('C:/Altview/intraday_5min_MSFT.csv')
    Open = list(df['Open'])[-1]
    close = list(df['close'])[0]
    high = np.max(np.array(df['high']))
    low = np.min(np.array(df['low']))
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data,indent = 2)
    data = {'chart_data': chart_data}
    return render_template("index.html", data=data, Open = Open, close = close, high = high, low = low )
    '''
    global logged
    logged = 0
    return render_template("indexToIndex.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged
    name = request.form['name']
    pwd = request.form['pwd']
    data = pd.read_csv('login_csv_file.csv')
    for i in range(0,data.shape[0]):
        if(name == data.iloc[i][0] and pwd == data.iloc[i][1]):
            logged = 1 
            return redirect(url_for('index1'))
    return render_template('err.html')

@app.route('/redirect_to_watchlist', methods = ['GET', 'POST'])
def watchlist():
    data = pd.read_csv('company_csv_file.csv')
    global companies
    global symbols
    companyName = []
    for i in range(0,data.shape[0]):
        companyName = companyName + [data.iloc[i][0]]
    '''
    resp = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=17ZNKSR4QPDOFBVJ')
    x1 = resp.json()['bestMatches']
    companies = []
    symbols = []
    for i in x1:
      companies = companies + [i['2. name']]
      symbols = symbols + [i['1. symbol']]
    '''
    return render_template('AddToWatch.html', companies = companies, lent = len(companies), companyName = companyName,lent1 = len(companyName))

@app.route('/addToWatch', methods=['GET', 'POST'])
def add():
    f = request.get_json()
    data = pd.read_csv('company_csv_file.csv')
    if f not in list(data['companyName']):
        data = data.append({'companyName' : f}, ignore_index = True)
    data.to_csv(r'company_csv_file.csv',index = False)
    return redirect(url_for('watchlist'))

@app.route('/removeFromWatch', methods=['GET', 'POST']) 
def red_watch():
    f = request.get_json()
    data = pd.read_csv('company_csv_file.csv')
    if f in list(data['companyName']):
        data.drop(data[data['companyName'] == f].index, inplace = True)
    data.to_csv(r'company_csv_file.csv',index = False)
    return redirect(url_for('watchlist'))

@app.route('/directToSignup')
def re_signup():
    return render_template('signUp.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    name = request.form['name']
    pwd = request.form['pwd']
    data = pd.read_csv('login_csv_file.csv')
    data = data.append({'name' : name, 'pwd' : pwd}, ignore_index = True)
    data.to_csv(r'login_csv_file.csv',index = False)
    return render_template('indexToIndex.html')
    
@app.route("/intraday", methods=['GET', 'POST'])
def index1():
    global SYMBOL
    global flag
    global logged
    
    global companies
    global symbols
    
    flag = flag + 1
    if request.method == 'POST':
        f = request.get_json()
        global SYMBOL
        SYMBOL = f
        print("This is",f)
    ''' 
    
    print("changed symbol is", SYMBOL)
    resp = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=17ZNKSR4QPDOFBVJ')
    x1 = resp.json()['bestMatches']
    companies = []
    symbols = []
    for i in x1:
      companies = companies + [i['2. name']]
      symbols = symbols + [i['1. symbol']]
    '''
    for i in range(0,len(symbols)):
        if symbols[i] == SYMBOL:
            break
    
    name = companies[i]
    #print('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+SYMBOL+'&interval=5min&apikey=17ZNKSR4QPDOFBVJ')
    resp = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+SYMBOL+'&interval=5min&apikey=17ZNKSR4QPDOFBVJ')
    #print(resp.json())
    x = list((resp.json())['Time Series (5min)'].keys())    
    y = ((resp.json())['Time Series (5min)'])
    for i in x:
      y[i]['timestamp'] = i
    data = []
    for i in y:
      data = data + [y[i]]
      
    opn = []
    high = []
    low = []
    close = []
    for i in x:
      opn = opn + [float(y[i]['1. open'])]
    for i in x:
      high = high + [ float(y[i]['2. high']) ]
    for i in x:
      low = low + [ float(y[i]['3. low']) ]
    for i in x:
      close = close + [ float(y[i]['4. close']) ] 
     
    for i in data:
        i['open'] = i.pop('1. open')
    
    opn = opn[0]
    close = close[len(close) - 1]
    high = np.max(np.array(high))
    low = np.min(np.array(low))
    
    #print(data)
    data = json.dumps(data,indent = 2)
    data = {'chart_data' : data}
    
    return render_template("index.html", data=data, Open = opn, close = close, high = high, low = low,inde = 1, symbols = symbols, companies = companies, lent = len(companies), SYMBOL = name ,flag = flag,mode = 'intraday')

@app.route("/week")
def index2():
    global SYMBOL
    global companies
    global symbols
    
    '''
    resp = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=17ZNKSR4QPDOFBVJ')
    x1 = resp.json()['bestMatches']
    companies = []
    symbols = []
    for i in x1:
      companies = companies + [i['2. name']]
      symbols = symbols + [i['1. symbol']]
    '''
    for i in range(0,len(symbols)):
        if symbols[i] == SYMBOL:
            break
    
    name = companies[i]  
    resp = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+SYMBOL+'&apikey=17ZNKSR4QPDOFBVJ')
    x = list((resp.json())['Weekly Time Series'].keys())    
    y = ((resp.json())['Weekly Time Series'])
    for i in x:
      y[i]['timestamp'] = i
    data = []
    for i in y:
      data = data + [y[i]]
      
    opn = []
    high = []
    low = []
    close = []
    for i in x:
      opn = opn + [float(y[i]['1. open'])]
    for i in x:
      high = high + [ float(y[i]['2. high']) ]
    for i in x:
      low = low + [ float(y[i]['3. low']) ]
    for i in x:
      close = close + [ float(y[i]['4. close']) ] 
     
    for i in data:
        i['open'] = i.pop('1. open')
    #print(data)
    
    opn = opn[0]
    close = close[len(close) - 1]
    high = np.max(np.array(high))
    low = np.min(np.array(low))
    
    data = json.dumps(data,indent = 2)
    data = {'chart_data' : data}
    
    return render_template("index.html", data=data, Open = opn, close = close, high = high, low = low,inde = 2, symbols = symbols, companies = companies, lent = len(companies), SYMBOL = name ,flag = flag,mode = 'week')

   
@app.route("/day")
def index3():
    global SYMBOL
    global companies
    global symbols
    '''
    resp = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=17ZNKSR4QPDOFBVJ')
    x1 = resp.json()['bestMatches']
    companies = []
    symbols = []
    for i in x1:
      companies = companies + [i['2. name']]
      symbols = symbols + [i['1. symbol']]
    '''
    for i in range(0,len(symbols)):
        if symbols[i] == SYMBOL:
            break

    name = companies[i]
    s = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+SYMBOL+'&apikey=17ZNKSR4QPDOFBVJ'
    resp = requests.get(s)

    x = list((resp.json())['Time Series (Daily)'].keys())    
    y = ((resp.json())['Time Series (Daily)'])
    for i in x:
      y[i]['timestamp'] = i
    data = []
    for i in y:
      data = data + [y[i]]
    opn = []
    high = []
    low = []
    close = []
    for i in x:
      opn = opn + [float(y[i]['1. open'])]
    for i in x:
      high = high + [ float(y[i]['2. high']) ]
    for i in x:
      low = low + [ float(y[i]['3. low']) ]
    for i in x:
      close = close + [ float(y[i]['4. close']) ] 
     
    for i in data:
        i['open'] = i.pop('1. open')
        
    data = json.dumps(data,indent = 2)
    data = {'chart_data' : data}
    
    opn = opn[0]
    close = close[len(close) - 1]
    high = np.max(np.array(high))
    low = np.min(np.array(low))
    
    return render_template("index.html", data=data, Open = opn, close = close, high = high, low = low,inde = 2, symbols = symbols, companies = companies, lent = len(companies), SYMBOL = name ,flag = flag,mode = 'day')

@app.route("/month")
def index4():
    global SYMBOL
    global companies
    global symbols
    '''
    resp = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=17ZNKSR4QPDOFBVJ')
    x1 = resp.json()['bestMatches']
    companies = []
    symbols = []
    for i in x1:
      companies = companies + [i['2. name']]
      symbols = symbols + [i['1. symbol']]
    '''
    for i in range(0,len(symbols)):
        if symbols[i] == SYMBOL:
            break
    
    name = companies[i]
    resp = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+SYMBOL+'&apikey=17ZNKSR4QPDOFBVJ')
    x = list((resp.json())['Monthly Time Series'].keys())    
    y = ((resp.json())['Monthly Time Series'])
    for i in x:
      y[i]['timestamp'] = i
    data = []
    for i in y:
      data = data + [y[i]]
    opn = []
    high = []
    low = []
    close = []
    for i in x:
      opn = opn + [float(y[i]['1. open'])]
    for i in x:
      high = high + [ float(y[i]['2. high']) ]
    for i in x:
      low = low + [ float(y[i]['3. low']) ]
    for i in x:
      close = close + [ float(y[i]['4. close']) ] 
     
    for i in data:
        i['open'] = i.pop('1. open')
        
    data = json.dumps(data,indent = 2)
    data = {'chart_data' : data}
    
    opn = opn[0]
    close = close[len(close) - 1]
    high = np.max(np.array(high))
    low = np.min(np.array(low))
    
    return render_template("index.html", data=data, Open = opn, close = close, high = high, low = low,inde = 2, symbols = symbols, companies = companies, lent = len(companies), SYMBOL = name ,flag = flag,mode = 'Month')

  
if __name__ == "__main__":
    fetch_companies()
    app.run()


