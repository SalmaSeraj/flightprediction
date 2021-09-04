from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
from sklearn.preprocessing  import MinMaxScaler
import pickle
import pandas as pd
#from Flight_Price_Prediction import part_of_day
from ipynb.fs.full.Flight_Price_Prediction import part_of_day, get_addinfo_mean_encode, get_dep_mean_encode, get_arr_mean_encode


app = Flask(__name__)
model= pickle.load(open('Flight_Price_Prediction.pkl',"rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("Home.html")

@app.route("/predict", methods=["GET","post"])
@cross_origin()
def predict():
    if request.method == "POST":
    # Total Stops
        Total_Stops=request.form["stops"]

        #Day, Month & weekday of Journey
        date_dep = request.form["Dep_Time"]
        date_arr = request.form["Arrival_Time"]

        Day_of_Journey =int(pd.to_datetime(date_dep).day)
        Month_of_Journey= int(pd.to_datetime(date_dep).month)
        Weekday_of_Journey = int(pd.to_datetime(date_dep).dayofweek)

        Dep_hr = int(pd.to_datetime(date_dep).hour)
        Dep_min = int(pd.to_datetime(date_dep).minute)
        Arr_hr = int(pd.to_datetime(date_arr).hour)
        Arr_min = int(pd.to_datetime(date_arr).minute)

        # part of the day
        Dep_pod = part_of_day(Dep_hr)
        Dep_partofday = get_dep_mean_encode(Dep_pod)

        Arr_pod =part_of_day(Arr_hr)
        Arrival_partofday = get_arr_mean_encode(Arr_pod)

        # Duration
        dur_hour = abs(Arr_hr - Dep_hr)
        dur_min = abs(Arr_min - Dep_min)
        Duration_mins=(dur_hour*60)+dur_min

        # Airline
        # Fore Air ASIA(droped column) set all values to zer
        Airline = request.form['Airline']
        if (Airline == 'Air India'):
            Air_India = 1
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet	 = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0


        elif (Airline == 'GoAir'):
            Air_India = 0
            GoAir = 1
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (Airline == 'IndiGo'):
            Air_India = 0
            GoAir = 0
            IndiGo = 1
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (Airline == 'Jet Airways'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 1
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (Airline == 'Jet Airways Business'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 1
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (Airline == 'Multiple carriers'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 1
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (Airline == 'Multiple carriers Premium economy'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 1
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (Airline == 'SpiceJet'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 1
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (Airline == 'Trujet'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 1
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (Airline == 'Vistara'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 1
            Vistara_Premium_economy = 0

        elif (Airline == 'Vistara Premium economy'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 1

        else:
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        # Source
        # Banglore = 0 (not in column)
        Source = request.form["Source"]
        if (Source == 'Chennai'):
            src_Chennai = 1
            src_Delhi = 0
            src_Kolkata = 0
            src_Mumbai = 0


        elif (Source == 'Delhi'):
            src_Chennai = 0
            src_Delhi = 1
            src_Kolkata = 0
            src_Mumbai = 0

        elif (Source == 'Kolkata'):
            src_Chennai = 0
            src_Delhi = 0
            src_Kolkata = 1
            src_Mumbai = 0

        elif (Source == 'Mumbai'):
            src_Chennai = 1
            src_Delhi = 0
            src_Kolkata = 0
            src_Mumbai = 1

        else:
            src_Chennai = 0
            src_Delhi = 0
            src_Kolkata = 0
            src_Mumbai = 0

     # Destination
        # Banglore = 0 (not in column)
        dst = request.form["Destination"]
        if (dst == 'Cochin'):
            dst_Cochin = 1
            dst_Delhi = 0
            dst_Hyderabad = 0
            dst_Kolkata = 0
            dst_New_Delhi = 0

        elif (dst == 'Delhi'):
            dst_Cochin = 0
            dst_Delhi = 1
            dst_Hyderabad = 0
            dst_Kolkata = 0
            dst_New_Delhi = 0

        elif (dst == 'New Delhi'):
            dst_Cochin = 0
            dst_Delhi = 0
            dst_Hyderabad = 0
            dst_Kolkata = 0
            dst_New_Delhi = 1

        elif (dst == 'Hyderabad'):
            dst_Cochin = 0
            dst_Delhi = 0
            dst_Hyderabad = 1
            dst_Kolkata = 0
            dst_New_Delhi = 0

        elif (dst == 'Kolkata'):
            dst_Cochin = 0
            dst_Delhi = 0
            dst_Hyderabad = 0
            dst_Kolkata = 1
            dst_New_Delhi = 0

        else:
            dst_Cochin = 0
            dst_Delhi = 0
            dst_Hyderabad = 0
            dst_Kolkata = 0
            dst_New_Delhi = 0

        #Additinal Info
        Add_Info = request.form['Additional_Info']
        Additional_Info= get_addinfo_mean_encode(Add_Info)

        scale = MinMaxScaler()
        X=pd.DataFrame([[Total_Stops,Additional_Info,Day_of_Journey,Month_of_Journey,Weekday_of_Journey,Dep_partofday,Arrival_partofday,Duration_mins,Air_India,GoAir,IndiGo,Jet_Airways,Jet_Airways_Business,Multiple_carriers,Multiple_carriers_Premium_economy,SpiceJet,Trujet,Vistara,Vistara_Premium_economy,src_Chennai,src_Delhi,src_Kolkata,src_Mumbai,dst_Cochin,dst_Delhi,dst_Hyderabad,dst_Kolkata,dst_New_Delhi]])
        #Sprint(X)
        X[X.columns] = scale.fit_transform(X)
        #print("AI {f1}".format(f1=Add_Info))
        #print("TS-- {f2}".format(f2=Total_Stops))
        #print("DOJ {f4}".format(f4=Day_of_Journey))
        #print("moj  {f5}".format(f5=Month_of_Journey))
        #print("wdj  {f6}".format(f6=Weekday_of_Journey))
        #print("dpartday  {f7}".format(f7=Dep_partofday))
        #print("apartday   {f8}".format(f8=Arrival_partofday))
        #print("dmins  {f9}".format(f9=Duration_mins))
        prediction=model.predict(X)
        output=round(prediction[0],2)

        return render_template('Home.html',prediction_text="Your Flight price is Rs. {}".format(output))
    return render_template("Home.html")

if __name__ == "__main__":
    app.run(debug=True)