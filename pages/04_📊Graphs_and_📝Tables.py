import plotly.express as px
import pandas as pd
import requests
import warnings as w
w.filterwarnings("ignore")

import streamlit as st

#--------------------------------------page setup------------------------------------------------
st.set_page_config(page_title= "Graphs and Tables",page_icon=":part_alternation_mark:",layout="wide")

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

#--------------------------------import data from st.session----------------------------------------
df = st.session_state['df1']

#fill nan with 0 and  change data types of few columns from float to int 
final_df = df.fillna(0).astype({"Incident_Number":'int64',"PC_Asset_Task_Number":'int64',"SC_Task_Number":'int64',"Number_of_surveys":'int64'})

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_table = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_OhozL4.json")

#-------------------------------------- streamlit--------------------------------------------------

region = st.sidebar.multiselect("Select Region:",options=final_df["Region"].sort_values().unique(),help="You can select one or more regions")

team = st.sidebar.multiselect("Select Team:",options=final_df.query("Region == @region")["Team"].sort_values().unique(),help="You can select one or more Teams")

final_selection = final_df.query("Region == @region & Team == @team")



with st.container():

    left,right = st.columns([1,1])

    with right:
        st.markdown(f"<h1 style='text-align: right;'> 📈Graphs/Charts <br>and <br>📝Table</h1>", unsafe_allow_html=True)

        
        
st.markdown("-------")   

tab1, tab2 = st.tabs(["📈Charts","📊Tabular Data",])
if final_selection.empty:
            st.markdown(f"<h2 style='text-align: center;'>  ⚠️ Please select a region and corresponding team from the filters in the sidebar </h2>", unsafe_allow_html=True)
else:
    with tab1:
        data = final_selection.groupby(by=["Team"]).sum().iloc[:,:3]
        chart = px.bar(data,
                    title="Team wise case Split",
                    orientation="h",
                    template="plotly_dark",
                    width= 1000
                    )
        chart.update_layout(plot_bgcolor= "rgba(0,0,0,0)",showlegend=False)
        st.plotly_chart(chart)

    with tab2:
        st.dataframe(final_selection.sort_values(by=["Combined_User_Id"]).reset_index(drop=True))




        
