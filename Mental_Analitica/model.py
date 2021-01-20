
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector as sql
import pickle

db = sql.connect(
    host="bdpmye8dyhwt4hdqhgcp-mysql.services.clever-cloud.com",
    user="upk3pjsosofutpwj",
    passwd="CBl9dLCyWcsvG3wFSGov",
    database="bdpmye8dyhwt4hdqhgcp"
)
print(db)
cursor = db.cursor()
cursor.execute('SELECT resultado FROM DEncuesta')
r = cursor.fetchall()
cursor.execute('SELECT valoracion FROM DEncuesta')
v = cursor.fetchall()
print(r)
print(v)
db.close()


X_adr = r
X_adr = np.array(X_adr)
X_adr = X_adr.reshape(-1,1)

y_adr=v
print(X_adr)
print(y_adr)



X_month = np.array(X_adr.shape)
X_monthF = X_month[0]/30


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_adr,y_adr,test_size=0.2)

from sklearn.ensemble import RandomForestRegressor

#Defina el algoritmo a utilizar
adr = RandomForestRegressor(n_estimators =300,max_depth = 8)

#entrenar el modelo
adr.fit(X_train,y_train)
#realizo una prediccion
Y_pred = adr.predict(X_test)
#score en porcentaje
scorepor = adr.score(X_train,y_train)*100

pickle.dump(adr,open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))
#print(model.predict([[4, 300, 500]]))



