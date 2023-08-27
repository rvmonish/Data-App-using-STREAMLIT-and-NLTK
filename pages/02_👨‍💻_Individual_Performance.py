import pandas as pd
import requests
import warnings as w
w.filterwarnings("ignore")

import streamlit as st
from streamlit_lottie import st_lottie,st_lottie_spinner

#------------------------------------page setup----------------------------------
st.set_page_config(page_title= "👨‍💻 Individual Report",page_icon=":bar_chart:",layout="wide")
page_layout =st.session_state["page_layout"]
sidebar_style = """
<style>
    [data-testid="stSidebar"]{
        background-color : rgb(0,0,0);
    }
</style>
"""
st.markdown(page_layout,unsafe_allow_html= True)
st.markdown(sidebar_style,unsafe_allow_html= True)

#-----------------------------------loading resources ----------------------------------#
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_chart = load_lottieurl("https://assets4.lottiefiles.com/temp/lf20_TOE9MF.json")


#--------------------------------import data from st.session----------------------------------------
final_df = st.session_state['df1']


#------------------------------ streamlit main page--------------------------------------#

# main heading 
st.title("Agent Performance Dashboard :bar_chart:")

# create sidebar for filters 
st.sidebar.header("Filter Here")
agent_id = st.sidebar.selectbox("Search Agent ID :",final_df["User_Id"].sort_values().unique())
 # creating streamlit dropdown for agents

#--------------------------------calculation--------------------------------------------------#

score = round(final_df.query('User_Id == @agent_id')["Voc_score"].unique().item(),2)
if pd.isna(score):
    score = 0

stars = ":star:"* int(score) # add stars

#retrieve Agent's full name with user_id
combined_agent_name = final_df.query('User_Id == @agent_id')['Combined_User_Id'].unique().item()

# calculation for total inc cases 

total_inc = int(final_df.query('User_Id == @agent_id')["Incident_Number"].sum())

# calculation for toatl ast cases

total_ast = int(final_df.query('User_Id == @agent_id')["PC_Asset_Task_Number"].sum())

#calculation for toatl sc_task

total_sc = int(final_df.query('User_Id == @agent_id')["SC_Task_Number"].sum())

#--------------------------------end of calculations-----------------------------------------#


button_css = f"""
    <button style ="background:#009578; border:none; outline:none; border-radius:5px; font-size:16px">
        <span style="align-items:center; height:100%;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-rolodex" viewBox="0 0 16 16">
            <path d="M8 9.05a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z"/>
            <path d="M1 1a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h.5a.5.5 0 0 0 .5-.5.5.5 0 0 1 1 0 .5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5.5.5 0 0 1 1 0 .5.5 0 0 0 .5.5h.5a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1H6.707L6 1.293A1 1 0 0 0 5.293 1H1Zm0 1h4.293L6 2.707A1 1 0 0 0 6.707 3H15v10h-.085a1.5 1.5 0 0 0-2.4-.63C11.885 11.223 10.554 10 8 10c-2.555 0-3.886 1.224-4.514 2.37a1.5 1.5 0 0 0-2.4.63H1V2Z"/>
            </svg> Info
        </span>
    </button>
"""
st.markdown(f"""
### {combined_agent_name} {stars}
[{button_css}](https://directory.cisco.com/dir/reports/{agent_id})
""" 
, unsafe_allow_html= True)

st.markdown("---")

with st.container():
    # layer 1 create three columns for agent voc score on the left and performance on the right
    col_1,col_2,col_3,col_4,col_5,col_6 = st.columns([1,1,1,1,1,3])

    with col_1:
        st.markdown("#")
        st.markdown("#")
        st.metric(label="Voc Score", value= score)

    with col_2:
        st.markdown("#")
        st.markdown("#")
        st.metric(label="INC resolved", value= total_inc)
        
    with col_3:
        st.markdown("#")
        st.markdown("#")
        st.metric(label="Total AST", value= total_ast)

    with col_4:
        st.markdown("#")
        st.markdown("#")
        st.metric(label="Total SC Task", value= total_sc)
    
    with col_5:
        st.markdown("#")
        st.markdown("#")
        st.metric(label="Total cases", value= sum([total_inc,total_ast,total_sc]))
    
    with col_6:
        st_lottie(lottie_chart, key="chart_animation",height= 250)

st.markdown("---")
        
    