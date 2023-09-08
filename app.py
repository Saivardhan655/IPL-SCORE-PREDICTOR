import pickle
from flask import Flask,request,jsonify,render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


app=Flask(__name__)
reg_model=pickle.load(open('ipl_reg.pkl','rb'))
#scaler_model=pickle.load(open('scaler.pkl','rb'))

#route for homepage
@app.route('/')
def index():
     return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
     if request.method=='POST':
        bat=request.form.get('Batting team')
        bowl=request.form.get('Bowling team')
        run=int(request.form.get('enter no of runs scored by team'))
        wicket=int(request.form.get('Enter no Wickets'))
        over=float(request.form.get("enter no of overs completed"))
        run_5=int(request.form.get('Enter no of runs scored in last 5 overs'))
        wick_5=int(request.form.get('Enter no of wickets in last 5 overs'))
        perm_teams={'Royal Challengers Bangalore':0, 'Kings XI Punjab':1,
       'Delhi Daredevils':2, 'Kolkata Knight Riders':3, 'Rajasthan Royals':4,
       'Mumbai Indians':5, 'Chennai Super Kings':6, 'Sunrisers Hyderabad':7}
        def score_predictor():
          score = []
          n = perm_teams[bat]
          m = perm_teams[bowl]
          score.extend(one(n))
          score.extend(one(m))
          score.extend([run, wicket, over, run_5, wick_5])
          arr = np.array([score])
          y_pred4 = reg_model.predict(arr)
          return y_pred4
        def one(i):
            list1=[0]*8
            for j in range(7):
               if j==i:
                   list1[j]=1
               else:
                   list1[j]=0
            return list1
        result=score_predictor()
        if result is not None:
            return render_template('home.html', result=result[0])
        else:
            return render_template('error.html')
     else:
         return render_template('home.html')
     





if __name__=='__main__':
     app.run(host="0.0.0.0")