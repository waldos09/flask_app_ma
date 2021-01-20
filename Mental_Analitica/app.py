import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from flask_mysqldb import MySQL
import os
import io
import pandas as pd
import matplotlib.pyplot as plt


app = Flask(__name__)
app.config['MYSQL_HOST']='bdpmye8dyhwt4hdqhgcp-mysql.services.clever-cloud.com'
app.config['MYSQL_USER']='upk3pjsosofutpwj'
app.config['MYSQL_PASSWORD']='CBl9dLCyWcsvG3wFSGov'
app.config['MYSQL_DB']='bdpmye8dyhwt4hdqhgcp'
mysql = MySQL(app)



#model = pickle.load(open('model.pkl','rb'))

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

    
@app.route('/result',methods=['POST'])
def resultados():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        
        #luisdavidecheverrzasad@gmail.com
        params=[email]
        cursor = mysql.connection.cursor()
        #se obtienen los datos completos
        cursor.execute("SELECT * FROM MDatos WHERE correo=%s",params)
        r = cursor.fetchall()
        cursor.execute("SELECT nombre FROM MDatos WHERE correo=%s",params)
        nombre = cursor.fetchall()
        #se obtiene solo la id 
        i=cursor.execute("SELECT Id_datos FROM MDatos WHERE correo=%s",params)
        i = cursor.fetchall()
        print(i)
        cursor.execute("SELECT resultado FROM DEncuesta WHERE Id_usuario=%s",i)
        resultados = cursor.fetchall()
        print(resultados)
        cursor.execute("SELECT valoracion FROM DEncuesta WHERE Id_usuario=%s",i)
        valoracion = cursor.fetchall()
        print(valoracion)

        X_adr = resultados
        #X_adr = np.array(X_adr)
        #X_adr = X_adr.reshape(-1,1)
        y_adr= valoracion
        print(X_adr)
        print(y_adr)
        from sklearn.model_selection import train_test_split
        X_train,X_test,y_train,y_test = train_test_split(X_adr,y_adr,test_size=0.2)

        from sklearn.ensemble import RandomForestRegressor

        #Defina el algoritmo a utilizar
        adr = RandomForestRegressor(n_estimators =300,max_depth = 8)

        #entrenar el modelo
        adr.fit(X_train,y_train)
        #realizo una prediccion
        Y_pred = adr.predict(X_test)

        img = io.BytesIO()
        plt.title("la grafica de:" + nombre)
        X_grid = np.arange(min(X_test),max(X_test),0.1)
        X_grid = X_grid.reshape((len(X_grid),1))
        plt.scatter(X_test,y_test)
        plt.plot(X_grid,adr.predict(X_grid),color='red',linewidth=3)
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('resultado.html', infos = r ,imagen={ 'imagen': plot_url })


if __name__ == "__main__":
    app.run(port=3000,debug=True)    