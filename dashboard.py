# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 16:36:41 2022

@author: Arpita
"""
import streamlit as st
import pandas as pd
import joblib



def predict(data1,data2):
    feelings_data = pd.read_csv('feelings_food_labelled.csv')
    
    cat=feelings_data['food'].value_counts().index.tolist()
    num_cat=feelings_data['food_coded'].value_counts().index.tolist()

    d = {}
    for a, b in zip(num_cat,cat):
        d[a] = b

    model = joblib.load(open("model.pkl",'rb'))
    predict = model.predict([[data1,data2]])
    
    return d[predict[0]]

def get_mood():
    dic = {'Select an option':0,'Fatigued':1,'Sleepy':2,'Hungry':3,'Angry':4,'Lonely':5,'Sad':6,'Happy':7,'Bored':8,\
      'Overweight':9,'Underweight':9,'High Glucose':11,'Headache':12}
    feel = []
    for i in dic.keys():
        feel.append(i)
    return feel,dic

def process_mood(mood):
    
    _,di=get_mood()
    return di[mood]

# front end elements of the web page 
html_temp = """ 
    <div style  = margin:0px;
    font-family: "Times New Roman", Times, serif;
    left: auto;">
     
    
    <h2 <p style ="color:#DDC150;
    marginTop:-25pt;
    padding:2px;
    font-weight: bold;
    text-align:center;">
    <em>Place Your Order</em>
    </p></h2><br>
    
    
    <h3  <p style ="color:#E3984C;
    marginTop:-25pt;
    font-weight:bold; 
    padding:2px;
    text-align:left,">
    How do You Feel Today?
    </p></h3> <br>
    
    
    <p style ="color:#E3984C;
    font-weight:bold; 
    marginTop:-25pt;
    text-align:left;
    font-family:OCR A Std;
    font-size: 18px;
    paddingBottom:20px;
    border-bottom: 2px solid #F3CBA3;">
    Let Us Know How You Feel and We can Make a Menu Suggestion Just For You :)
    </p> <br>
    
    
    <p style ="color:black;
    font-weight:light; 
    marginTop:-25pt;
    text-align:left;
    font-family:sans-serif;
    font-size: 15px;">
    <em>Let's take a quick survey about yourself first 👇</em>
    </p> <br>
    
  </div>
"""

st.write(html_temp, unsafe_allow_html=True)

#st.markdown("<h4 style= 'color: black;marginLeft: -150pt;'>{st.text_input("Enter details here",key="name1")}</h4>")
col=st.columns(2)
with col[0]:
        st.markdown("<h5 style= 'color: black;'>How old are you? </h5>", unsafe_allow_html=True)
        age = st.number_input("Enter your age here ",min_value=0,max_value=100,step=1)
with col[1]:
        st.markdown("<h5 style= 'color: black;'>How are you feeling today ?</h5>", unsafe_allow_html=True)
        mood_list,_=get_mood()
        inp =st.selectbox("Enter here... ", mood_list)
        mood = process_mood(inp)

button = st.button("Submit")

if(button):
    if(age>0 and mood>0):
        msg1= predict(age,mood)
        st.markdown(f'<p style="color:black;font-weight: bold;font-size:18px;">Here’s what we suggest: {msg1}</p>', unsafe_allow_html=True)
    else:
        msg2='Required Data are missing, Please key in all the data.'
        st.markdown(f'<p style="color:red;font-weight: bold;font-size:18px; border-radius:2%;">{msg2}</p>', unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
def get_data():
    return []

@st.cache(allow_output_mutation=True)
def show_data():
    return []

pre= predict(age,mood)
#if st.button("Add row"):
#    if(age>0 and mood>0):
#        get_data().append({"Age": age, "Mood": mood, "Suggested Food": pre})
 #       
#    else:
 #      msg2='Required Data are missing, Please key in all the data.'
  #     st.markdown(f'<p style="color:red;font-weight: bold;font-size:18px; border-radius:2%;">{msg2}</p>', unsafe_allow_html=True)
        

@st.cache
def convert_df():
    get_data().append({"Age": age, "Mood": mood, "Suggested Food": pre})
    df=pd.DataFrame(get_data())
    
    return df.to_csv(index=False).encode('utf-8')


if(st.button("Show Data")):
    if(age>0 and mood>0):
        show_data().append({"Age": age, "Mood": mood, "Suggested Food": pre})
        st.write(pd.DataFrame(show_data()))
        csv = convert_df()
        #st.write()
        st.download_button(
            "Download Data",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )
    else:
        st.write("There is no data to show!")




