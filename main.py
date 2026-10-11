import streamlit as st
import pickle 
import warnings
warnings.filterwarnings("ignore")

st.title("Weather Prediction!!")
ppt=st.number_input("Enter Precipitation : ")
maxt=st.number_input("Enter maximum temperature: ")
mint=st.number_input("Enter minimum temperature: ")
wind=st.number_input("Enter wind speed: ")
btn=st.button("Predict!!")
if btn:
    wp=pickle.load(open("wp.pkl","rb"))
    res=wp.predict([[ppt,maxt,mint,wind]])[0]
    st.success(f"Expected Weather : {res}")
    