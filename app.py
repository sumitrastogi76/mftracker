import sqlite3
import datetime
import time
from flask import Flask, request, redirect, url_for, render_template, abort, flash, session
from six.moves.urllib.request import urlopen
app = Flask(__name__)

def connect_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        #print("database open")
        return conn
    except:
        flash("ERROR : database open")

def update_value(conn,row,value,key):
    try:
        conn.execute("UPDATE MF_table set %s = %f where MF_ID = '%s';"%(row,value,key))
        conn.commit()
        #print("Record Updated Successfully")
    except:
        flash("ERROR : Record Not Updated")

def read_value(conn,table_name):
    try:
        cursor = conn.execute("SELECT * from %s"%table_name)
        return cursor
    except:
        flash("ERROR : DB Cursor not created")

@app.route('/login',methods = ['POST', 'GET'])
def login():
   error = None
   if request.method == 'POST':
      username = request.form['username']
      pswd = request.form['password']
      error = 'Invalid username or password. Please try again!'
      if pswd == "qwe123R$" and username == 'admin':
          #flash('Welcome %s, You were successfully logged in'%username)
          session['logged_in'] = True
          return redirect(url_for('home'))
      else:
          return render_template('login.html',error = error)

@app.route('/')
def index():
   return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in']=False
    return render_template('login.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/update', methods = ['POST','GET'])
def update():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            conn = connect_db('MF.db')
            update_value(conn,"UNIT",float(request.form['1MSB079']),"MSB079")
            update_value(conn,"COST",float(request.form['2MSB079']),"MSB079")
            update_value(conn,"UNIT",float(request.form['1MBS291']),"MBS291")
            update_value(conn,"COST",float(request.form['2MBS291']),"MBS291")
            update_value(conn,"UNIT",float(request.form['1MTE117']),"MTE117")
            update_value(conn,"COST",float(request.form['2MTE117']),"MTE117")
            update_value(conn,"UNIT",float(request.form['1MKP002']),"MKP002")
            update_value(conn,"COST",float(request.form['2MKP002']),"MKP002")
            update_value(conn,"UNIT",float(request.form['1MPI1116']),"MPI1116")
            update_value(conn,"COST",float(request.form['2MPI1116']),"MPI1116")
            update_value(conn,"UNIT",float(request.form['1MKM311']),"MKM311")
            update_value(conn,"COST",float(request.form['2MKM311']),"MKM311")
            update_value(conn,"UNIT",float(request.form['1MMA100']),"MMA100")
            update_value(conn,"COST",float(request.form['2MMA100']),"MMA100")
        flash('Database Updated Successfully')
        return redirect(url_for('home'))

@app.route('/showdb', methods = ['POST','GET'])
def show_db():
    conn = connect_db('MF.db')
    return render_template('update.html', cursor = read_value(conn,'MF_table'))

@app.route('/report', methods = ['POST','GET'])
def report():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        NAV = read_nav_from_internet()
        #save_nav_in_db(NAV)
        conn = connect_db('MF.db')
        value = []
        cost = []
        name = []
        unit = []
        data = []
        cursor_mf_table = read_value(conn,'MF_table')
        mf_data = cursor_mf_table.fetchall()
        for index in range(len(mf_data)):
            name.append(mf_data[index][0])
            unit.append(mf_data[index][2])
            value.append(mf_data[index][2]*NAV[index+1])
            cost.append(mf_data[index][3])
        for i in range(len(name)):
            if NAV[i+1] == 0:
                data.append([name[i],"ERROR",unit[i],round(cost[i],2),0,0])
            else:
                data.append([name[i].upper(),NAV[i+1],unit[i],round(cost[i],2),round(value[i],2),round(value[i]-cost[i],2)])
        data.append(['','','TOTAL',round(sum(cost),2),round(sum(value),2),round(sum(value)-sum(cost),2)])
        data.append(round((sum(value)-sum(cost))*100/sum(cost),2))
        return render_template('report.html',mf_data=data)

def save_nav_in_db(NAV):
    conn = connect_db('MF.db')
    conn.execute("INSERT INTO MF_RECORD (DATE, MF1, MF2, MF3, MF4, MF5, MF6, MF7) VALUES(?,?,?,?,?,?,?,?)",tuple(NAV))
    conn.commit()
    conn.close()

def read_nav_from_internet():
    MF_NAV = [str(datetime.datetime.now())]
    MF_DICT = {
                 'MSB079': r'https://www.moneycontrol.com/mutual-funds/nav/sbi-blue-chip-fund/MSB079',
                 'MBS291': r'https://www.moneycontrol.com/mutual-funds/nav/birla-sun-life-tax-relief-96/MBS291',
                 'MTE117': r'https://www.moneycontrol.com/mutual-funds/nav/franklin-india-high-growth-companies-fund/MTE117', 
                 'MKP002' : r'https://www.moneycontrol.com/mutual-funds/nav/franklin-india-prima-fund/MKP002', 
                 'MPI1116' : r'https://www.moneycontrol.com/mutual-funds/nav/icici-prudential-value-discovery-fund-direct-plan/MPI1116', 
                 'MKM311' : r'https://www.moneycontrol.com/mutual-funds/nav/kotak-select-focus-fund-regular-plan/MKM311', 
                 'MMA100' : r'https://www.moneycontrol.com/mutual-funds/nav/mirae-asset-emerging-bluechip-fund-direct-plan/MMA100'}
    
    for MF in MF_DICT:
        tmp = ""
        try:
            response = urlopen(MF_DICT[MF])
            myfile = str(response.read())
            tmp = (myfile.split('[')[1].split(']')[0].strip())
            MF_NAV.append(float(myfile.split('[')[1].split(']')[0].strip()))
        except:
            flash("Error during capturing NAV of %s-->"%MF_DICT[MF][46:-7]+tmp+"<--")
            MF_NAV.append(0)
    return MF_NAV

if __name__ == '__main__':
    app.secret_key = "r47yfauefyew8h9f83wht94yrtf9"
    app.run(debug = False)