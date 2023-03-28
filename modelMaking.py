import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import VotingClassifier

import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import confusion_matrix

# load the dataset

df = pd.read_csv("PatientData.csv")

del df['Index']

df.replace(np.nan,0)

# split the data into features and target

X = df.iloc[0:,:-1].values

y = df.iloc[:,-1].values

np.nan_to_num(X,
copy=False)

np.nan_to_num(y,copy=False)

labelencoder_y = LabelEncoder()

y = labelencoder_y.fit_transform(y)

X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size=0.20,random_state=0)

print("X_test")

print(X_test)

#  the logistic regression model

logisticReg = LogisticRegression(random_state=95,max_iter=95)



#  the decision tree model

decisionTrClf = DecisionTreeClassifier(random_state=90)



#  ensemble model using both logistic regression and decision tree

ensemble = VotingClassifier(estimators=[('lr',logisticReg), ('dt',decisionTrClf)], voting='soft')



# fit the ensemble model to the data

ensemble.fit(X_train,y_train)



# evaluate the model using k-fold cross-validation

from sklearn.model_selection import cross_val_score

scores = cross_val_score(ensemble,X_test, y_test, cv=5)



print("Accuracy:%0.2f (+/-%0.2f)" % (scores.mean(),scores.std() * 2))



def confusionMatrix(y_true,y_pred):



  y_pred = np.round(abs(y_pred))



  tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()



  accuracy=(tp+tn)/(tp+fp+fn+tn)



  specificity = tn/(tn+fp)



  sensitivity=tp/(tp+fn)



  print("Accuracy:",accuracy*100)



  print("Sensitivity:",sensitivity*100)



  print("Specificity:",specificity*100)



y_pred = ensemble.predict(X_test)

confusionMatrix(y_test,y_pred)



import pickle

filename = 'file.sav'

pickle.dump(ensemble,open(filename,'wb'))

# load the model from disk

loaded_model = pickle.load(open(filename,'rb'))

result = loaded_model.score(X_test, y_test)

print("Loaded model")

print(result)



Z = [94,26,97,29],[94,25,97,42],[110,16,97,45],[142,10,97,45],[110,16,98,31]



Z = np.array(Z)



#Z = Z.reshape(-1,1)

print("ZZZZZZZZZZZZz")

print(Z)



#Z_pred = new_model.predict(Z)



#print(Z_pred)



Num = 1



for z in Z:



    print(z)



    z = z.reshape(1,-1)



    #Z1_pred = model.predict(z)



    #print('Z1predddd')



    #print(Z1_pred)



    Z_pred = loaded_model.predict(z)



    print("line 265")



    print(Z_pred)

