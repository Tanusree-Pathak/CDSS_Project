from distutils.log import debug
from fileinput import filename
from flask import *
import numpy as np
import csv
import tensorflow as tf
from tabulate import tabulate
import pickle
from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import csv
from collections import defaultdict


app = Flask(__name__)
@app.route('/')
def main():
    return render_template("index.html")




 
# adding configuration for using a sqlite database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
app.app_context().push()

# Settings for migrations
migrate = Migrate(app, db)
 
# Models
class Profile(db.Model):
    inde = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.String, nullable=False)
    hr = db.Column(db.Float, unique=False, nullable=False)
    resp = db.Column(db.Float, unique=False, nullable=False)
    spo2 = db.Column(db.Float, unique=False, nullable=False)
    temp = db.Column(db.Float, unique=False, nullable=False)
    pred = db.Column(db.String, unique=False, nullable=False)
    suggestion = db.Column(db.String, unique=False, nullable=False)
 
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"ID : {self.inde}, First_Name : {self.first_name}, Last_Name : {self.last_name}, Age: {self.age}, Heart_rate : {self.hr}, Respiration : {self.resp}, SpO2 : {self.spo2}, Temperature : {self.temp}, Prediction : {self.pred}, Suggestion : {self.pred}"
'''
# function to render database page
@app.route('/view')
def view():
    profiles = Profile.query.all()
    print("line 60000000")
    print(profiles)
    return render_template('database.html', profiles=profiles)
'''
@app.route('/success',methods = ['POST'])
def success():
    if request.method == 'POST':
        icu = request.form["icuBed"]
        print("line 19")
        print(icu)
        gen = request.form["genBed"]
        print("line 22")
        print(gen)
        f = request.files['file']
        f.save(f.filename)
        nameFile = f.filename
        print(nameFile)
        print("++++++++")
        
        columns = defaultdict(list) # each value in each column is appended to a list

        with open(nameFile, "r") as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            with open("output.csv", "w") as result:
                writer = csv.writer(result)
                for r in reader:
                    # Use CSV Index to remove a column from CSV
		            #r[3] = r['year']
                    writer.writerow((r['HR(BPM)'], r['RESP(BPM)'], r['SpO2(%)'], r['TEMP(C)']))
            #for row in reader: # read a row as {column1: value1, column2: value2,...}
                    for (k,v) in r.items(): # go over each column name and value 
                        columns[k].append(v) # append the value into the appropriate list
                                         # based on column name k

        print(columns)
        global ind
        ind = columns['Index']
        global fn
        fn = columns['FirstName']
        global ln
        ln = columns['LastName']
        global age
        age =  columns['Age']
        print(ind)
        print(fn)
        print(ln)
        print(age)
        rows = []
        with open('output.csv', 'r') as file:
                    csvreader = csv.reader(file,quoting=csv.QUOTE_NONNUMERIC)
                    #header = next(csvreader)
                    for row in csvreader:
                        if len(row) != 0:
                            rows.append(row)
                #print(header)    
        print(rows)
        r = np.array(rows)
        #print(header)    
        print(rows)
        r = np.array(rows)
        print("RRRRRRRRRR")
        print(r)
        loaded_model = pickle.load(open('file.sav','rb'))
        print("New Modellllllllll")
        global requiredAction
        requiredAction = []
        global final
        final = []
        table = [['Index','Prediction', 'Required Action']]
        #background-image: url("https://www.healthcareitnews.com/sites/hitn/files/clinical-decision-imaging-getty-712.jpg");
        global hrate
        hrate = []
        global respLevel
        respLevel = []
        global spo2Level
        spo2Level = []
        global tempLevel
        tempLevel = []
        global pred
        pred = []

        # Check its architecture
        index = 1
        icucnt = icu
        gencnt = gen
        for z in r:
            action = []
            print(z)
            print("Vital signs")
            heartRate = z[0]
            respiration = z[1]
            SPO2 = z[2]
            temperature = z[3]
            hrate.append(heartRate)
            respLevel.append(respiration)
            spo2Level.append(SPO2)
            tempLevel.append(temperature)
            print(heartRate)
            if heartRate>100 or heartRate<60:
                act = "Check the heart rate"
                action.append(act)
            elif respiration>26 or respiration<15:
                act = "Maintain a proper respiration rate depending on patient's age"
                action.append(act)
            elif SPO2>98 or SPO2<95:
                act = "Please check the SPO2 Level"
                action.append(act)
            elif temperature<35 or temperature>37.2:
                act = "Temperature is not in normal range"
                action.append(act)
            else:
                act = "NONE"
                action.append(act)
            print(action)
            print("==========")
            z = z.reshape(1,-1)
            Z_pred = loaded_model.predict(z)
            pred.append(Z_pred)
            print(Z_pred)
            print("Final")
            print(Z_pred)
            finalwithIndex = []
            finalwithIndex.append(index)
            if Z_pred == 0:
                Z_pred = 'Patient needs to be admitted in ICU'
                icucnt = int(icucnt) - 1
            elif Z_pred == 1:
                Z_pred = 'Patient can be shifted in General Ward'
                gencnt = int(gencnt) - 1
            finalwithIndex.append(Z_pred)
            final.append(finalwithIndex)
            table.append(finalwithIndex)
            requiredAction.append(action)
            index = index + 1
        tableh1 = table[0][0]
        print(tableh1)
        tableh2 = table[0][1]
        print(tableh2)
        tableh3 = table[0][2]
        print(tableh3)
        print(requiredAction)

        print("Length of final")
        print(len(final))
        global length
        length = len(final)
        
        num = 0
        for num in range(0,length):
               print(ind[num])
               print(fn[num])
               print("Line 213")
               print(final[num][1])
               for i in requiredAction[num]:
                   sugg = i
                   print(sugg)
               indexUnique = int(ind[num])
               print(indexUnique)
               print(type(indexUnique))
               p = Profile(inde = indexUnique, first_name = fn[num], last_name = ln[num], 
                       age = age[num], hr = hrate[num], resp = respLevel[num], spo2 = spo2Level[num], 
                       temp = tempLevel[num], pred = final[num][1], suggestion = sugg)
               print("Line 221")
               print(p)

               db.session.add(p)
               db.session.commit()
               
        return render_template("Acknowledgement.html",name = nameFile, len = len(final), tableheader1 = tableh1, 
                               tableheader2 = tableh2, tableheader3 = tableh3, predictedValues = final, reqAct = requiredAction,
                                icuBed = icucnt, genBed = gencnt)
    

@app.route('/view', methods=["GET"])
def view():
     print("Line 235")
     print(request.method)
     if request.method == "GET":
        profiles = Profile.query.all()
        print("line 239")
        print(profiles)
        return render_template('database.html', profiles=profiles)
        '''
        print(ind)
        print(fn)
        print(ln)
        print(pred)
        num = 0
        for num in range(0,length):
               print(ind[num])
               print(fn[num])
               print("Line 244")
               print(final[num][1])
               for i in requiredAction[num]:
                   sugg = i
                   print(sugg)
               indexUnique = int(ind[num])
               print(indexUnique)
               print(type(indexUnique))
               p = Profile(inde = indexUnique, first_name = fn[num], last_name = ln[num], 
                       age = age[num], hr = hrate[num], resp = respLevel[num], spo2 = spo2Level[num], 
                       temp = tempLevel[num], pred = final[num][1], suggestion = sugg)

               db.session.add(p)
               db.session.commit()
               import time
               time.sleep(10)
               '''
               
           
            
      

@app.route('/delete/<int:inde>')
def delete(inde):
     print(inde)
     print("Line 275")
     print(request.method)
     print("line 275")
    # deletes the data on the basis of unique id and
    # directs to home page
     data = Profile.query.get(inde)
     print(data)
     db.session.delete(data)
     db.session.commit()
     return redirect('/')
 
if __name__ == '__main__':
    app.run(debug=False)
