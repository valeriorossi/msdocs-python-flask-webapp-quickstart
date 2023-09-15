import os
import urllib
import time
import requests
from datetime import datetime, timedelta
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.get("/items/")
def read_item(ticker: str = '0', startDate: str = '2023-01-01', endDate: str = '2023-01-01', period: str ='1d', events: str='history'):
    date_format = '%Y-%m-%d'
    strD = request.args.get('startDate')
    endD= request.args.get('endDate')
    tkr = request.args.get('ticker')
    prd = request.args.get('period')
    evt = request.args.get('events')
    start_date_obj = datetime.strptime(strD, date_format)
    end_date_obj = datetime.strptime(endD, date_format)
    unixStartDate = int(start_date_obj.timestamp())
    unixEndDate = int(end_date_obj.timestamp())
    
    yahooURL = 'https://query1.finance.yahoo.com/v7/finance/download/' + tkr + '?period1='+ str(unixStartDate) + '&period2=' +  str(unixEndDate) + '&interval=' + prd + '&events=' + evt + '&includeAdjustedClose=true'
    try:
        testfile = urllib.request.URLopener()
        fileName = tkr + '_' + evt + '_' + strD + '_' + endD + '.csv'
        testfile.retrieve(yahooURL, fileName)
        #return  {"item_id": ticker, "firstDate": unixStartDate, "endDate": unixEndDate, "events": events, "period": period}
        return  {"yahooURL": yahooURL, "item_id": ticker,"firstDate": unixStartDate, "endDate": unixEndDate, "events": events, "period": period}
    except Exception as e :
       print(str(e))



if __name__ == '__main__':
   app.run()
